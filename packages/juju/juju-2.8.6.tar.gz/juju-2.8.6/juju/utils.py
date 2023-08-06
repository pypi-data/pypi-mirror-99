import asyncio
import os
import textwrap
from collections import defaultdict
from functools import partial
from pathlib import Path
import base64
from pyasn1.type import univ, char
from pyasn1.codec.der.encoder import encode
import yaml


async def execute_process(*cmd, log=None, loop=None):
    '''
    Wrapper around asyncio.create_subprocess_exec.

    '''
    p = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        loop=loop)
    stdout, stderr = await p.communicate()
    if log:
        log.debug("Exec %s -> %d", cmd, p.returncode)
        if stdout:
            log.debug(stdout.decode('utf-8'))
        if stderr:
            log.debug(stderr.decode('utf-8'))
    return p.returncode == 0


def _read_ssh_key():
    '''
    Inner function for read_ssh_key, suitable for passing to our
    Executor.

    '''
    default_data_dir = Path(Path.home(), ".local", "share", "juju")
    juju_data = os.environ.get("JUJU_DATA", default_data_dir)
    ssh_key_path = Path(juju_data, 'ssh', 'juju_id_rsa.pub')
    with ssh_key_path.open('r') as ssh_key_file:
        ssh_key = ssh_key_file.readlines()[0].strip()
    return ssh_key


async def read_ssh_key(loop):
    '''
    Attempt to read the local juju admin's public ssh key, so that it
    can be passed on to a model.

    '''
    loop = loop or asyncio.get_event_loop()
    return await loop.run_in_executor(None, _read_ssh_key)


class IdQueue:
    """
    Wrapper around asyncio.Queue that maintains a separate queue for each ID.
    """
    def __init__(self, maxsize=0, *, loop=None):
        self._queues = defaultdict(partial(asyncio.Queue, maxsize, loop=loop))

    async def get(self, id):
        value = await self._queues[id].get()
        del self._queues[id]
        if isinstance(value, Exception):
            raise value
        return value

    async def put(self, id, value):
        await self._queues[id].put(value)

    async def put_all(self, value):
        for queue in self._queues.values():
            await queue.put(value)


async def block_until(*conditions, timeout=None, wait_period=0.5, loop=None):
    """Return only after all conditions are true.

    """
    async def _block():
        while not all(c() for c in conditions):
            await asyncio.sleep(wait_period, loop=loop)
    await asyncio.wait_for(_block(), timeout, loop=loop)


async def wait_for_bundle(model, bundle, **kwargs):
    """Helper to wait for just the apps in a specific bundle.

    Equivalent to loading the bundle, pulling out the app names, and calling::

        await model.wait_for_idle(app_names, **kwargs)
    """
    try:
        bundle_path = Path(bundle)
        if bundle_path.is_file():
            bundle = bundle_path.read_text()
        elif (bundle_path / "bundle.yaml").is_file():
            bundle = (bundle_path / "bundle.yaml")
    except OSError:
        pass
    bundle = yaml.safe_load(textwrap.dedent(bundle).strip())
    apps = list(bundle.get("applications", bundle.get("services")).keys())
    await model.wait_for_idle(apps, **kwargs)


async def run_with_interrupt(task, *events, loop=None):
    """
    Awaits a task while allowing it to be interrupted by one or more
    `asyncio.Event`s.

    If the task finishes without the events becoming set, the results of the
    task will be returned.  If the event become set, the task will be cancelled
    ``None`` will be returned.

    :param task: Task to run
    :param events: One or more `asyncio.Event`s which, if set, will interrupt
        `task` and cause it to be cancelled.
    :param loop: Optional event loop to use other than the default.
    """
    loop = loop or asyncio.get_event_loop()
    task = asyncio.ensure_future(task, loop=loop)
    event_tasks = [loop.create_task(event.wait()) for event in events]
    done, pending = await asyncio.wait([task] + event_tasks,
                                       loop=loop,
                                       return_when=asyncio.FIRST_COMPLETED)
    for f in pending:
        f.cancel()  # cancel unfinished tasks
    for f in done:
        f.exception()  # prevent "exception was not retrieved" errors
    if task in done:
        return task.result()  # may raise exception
    else:
        return None


class Addrs(univ.SequenceOf):
    componentType = char.PrintableString()


class RegistrationInfo(univ.Sequence):
    """
    ASN.1 representation of:

    type RegistrationInfo struct {
    User string

        Addrs []string

        SecretKey []byte

        ControllerName string
    }
    """
    pass


def generate_user_controller_access_token(username, controller_endpoints, secret_key, controller_name):
    """" Implement in python what is currently done in GO
    https://github.com/juju/juju/blob/a5ab92ec9b7f5da3678d9ac603fe52d45af24412/cmd/juju/user/utils.go#L16

    :param username: name of the user to register
    :param controller_endpoints: juju controller endpoints list in the format <ip>:<port>
    :param secret_key: base64 encoded string of the secret-key generated by juju
    :param controller_name: name of the controller to register to.
    """

    # Secret key is returned as base64 encoded string in:
    # https://websockets.readthedocs.io/en/stable/_modules/websockets/protocol.html#WebSocketCommonProtocol.recv
    # Deconding it before marshalling into the ASN.1 message
    secret_key = base64.b64decode(secret_key)
    addr = Addrs()
    for endpoint in controller_endpoints:
        addr.append(endpoint)

    registration_string = RegistrationInfo()
    registration_string.setComponentByPosition(0, char.PrintableString(username))
    registration_string.setComponentByPosition(1, addr)
    registration_string.setComponentByPosition(2, univ.OctetString(secret_key))
    registration_string.setComponentByPosition(3, char.PrintableString(controller_name))
    registration_string = encode(registration_string)
    remainder = len(registration_string) % 3
    registration_string += b"\0" * (3 - remainder)
    return base64.urlsafe_b64encode(registration_string)
