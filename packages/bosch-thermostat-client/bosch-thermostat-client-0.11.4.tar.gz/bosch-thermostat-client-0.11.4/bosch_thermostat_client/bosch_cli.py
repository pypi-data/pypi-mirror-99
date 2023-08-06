import click
import logging
from colorlog import ColoredFormatter
import aiohttp
import bosch_thermostat_client as bosch
from bosch_thermostat_client.const import XMPP
from bosch_thermostat_client.const.ivt import HTTP, IVT
from bosch_thermostat_client.const.nefit import NEFIT
import json
import asyncio
from functools import wraps

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
fmt = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
colorfmt = f"%(log_color)s{fmt}%(reset)s"
logging.getLogger().handlers[0].setFormatter(
    ColoredFormatter(
        colorfmt,
        datefmt=datefmt,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )
)


async def _scan(gateway, smallscan, output, stdout):
    _LOGGER.info("Successfully connected to gateway. Found UUID: %s", gateway.uuid)
    if smallscan:
        result = await gateway.smallscan(_type=smallscan.lower())
        out_file = output if output else f"smallscan_{gateway.uuid}.json"
    else:
        result = await gateway.rawscan()
        out_file = output if output else f"rawscan_{gateway.uuid}.json"
    if stdout:
        click.secho(json.dumps(result, indent=4), fg="green")
    else:
        with open(out_file, "w") as logfile:
            json.dump(result, logfile, indent=4)
            _LOGGER.info("Successfully saved result to file: %s", out_file)
            _LOGGER.debug("Job done.")


async def _runquery(gateway, path):
    _LOGGER.debug("Trying to connect to gateway.")
    _LOGGER.info("Query succeed: %s", path)
    result = await gateway.raw_query(path)
    click.secho(json.dumps(result, indent=4, sort_keys=True), fg="green")


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group(no_args_is_help=True)
@click.pass_context
@coro
async def cli(ctx):
    """A tool to run commands against Bosch thermostat."""

    pass


@cli.command()
@click.option(
    "--host",
    envvar="BOSCH_HOST",
    type=str,
    required=True,
    help="IP address of gateway or SERIAL for XMPP",
)
@click.option(
    "--token",
    envvar="BOSCH_ACCESS_TOKEN",
    type=str,
    required=True,
    help="Token from sticker without dashes.",
)
@click.option(
    "--password",
    envvar="BOSCH_PASSWORD",
    type=str,
    required=False,
    help="Password you set in mobile app.",
)
@click.option(
    "--protocol",
    envvar="BOSCH_PROTOCOL",
    type=click.Choice([XMPP, HTTP], case_sensitive=True),
    required=True,
    help="Bosch protocol. Either XMPP or HTTP.",
)
@click.option(
    "--device",
    envvar="BOSCH_DEVICE",
    type=click.Choice([NEFIT, IVT], case_sensitive=False),
    required=True,
    help="Bosch device type. NEFIT or IVT.",
)
@click.option(
    "-o",
    "--output",
    type=str,
    required=False,
    help="Path to output file of scan. Default to [raw/small]scan_uuid.json",
)
@click.option("--stdout", default=False, count=True, help="Print scan to stdout")
@click.option("-d", "--debug", default=False, count=True)
@click.option(
    "-s",
    "--smallscan",
    type=click.Choice(["HC", "DHW", "SENSORS", "RECORDINGS"], case_sensitive=False),
    help="Scan only single circuit of thermostat.",
)
@click.pass_context
@coro
async def scan(
    ctx,
    host: str,
    token: str,
    password: str,
    protocol: str,
    device: str,
    output: str,
    stdout: int,
    debug: int,
    smallscan: str,
):
    """Create rawscan of Bosch thermostat."""
    if debug:
        logging.basicConfig(
            colorfmt,
            datefmt=datefmt,
            level=logging.DEBUG,
            filename="out.log",
            filemode="a",
        )
        _LOGGER.info("Debug mode active")
        _LOGGER.debug(f"Lib version is {bosch.version}")
    else:
        logging.basicConfig(level=logging.INFO)
    logging.getLogger("aioxmpp").setLevel(logging.WARN)
    logging.getLogger("aioopenssl").setLevel(logging.WARN)
    logging.getLogger("aiosasl").setLevel(logging.WARN)
    logging.getLogger("asyncio").setLevel(logging.WARN)
    if device.upper() == NEFIT or device.upper() == IVT:
        BoschGateway = bosch.gateway_chooser(device_type=device)
    else:
        _LOGGER.error("Wrong device type.")
        return
    session_type = protocol.upper()
    if session_type == XMPP:
        session = asyncio.get_event_loop()
    elif session_type == HTTP and device.upper() == IVT:
        session = aiohttp.ClientSession()
    else:
        _LOGGER.error("Wrong protocol for this device")
        return
    try:
        gateway = BoschGateway(
            session=session,
            session_type=session_type,
            host=host,
            access_token=token,
            password=password,
        )

        _LOGGER.debug("Trying to connect to gateway.")
        if await gateway.check_connection():
            _LOGGER.info("Running scan")
            await _scan(gateway, smallscan, output, stdout)
        else:
            _LOGGER.error("Couldn't connect to gateway!")
    finally:
        await gateway.close()


@cli.command()
@click.option(
    "--host",
    envvar="BOSCH_HOST",
    type=str,
    required=True,
    help="IP address of gateway or SERIAL for XMPP",
    show_envvar=True,
)
@click.option(
    "--token",
    envvar="BOSCH_ACCESS_TOKEN",
    type=str,
    required=True,
    help="Token from sticker without dashes.",
)
@click.option(
    "--password",
    envvar="BOSCH_PASSWORD",
    type=str,
    required=False,
    help="Password you set in mobile app.",
)
@click.option(
    "--protocol",
    envvar="BOSCH_PROTOCOL",
    type=click.Choice([XMPP, HTTP], case_sensitive=False),
    required=True,
    help="Bosch protocol. Either XMPP or HTTP.",
)
@click.option(
    "--device",
    envvar="BOSCH_DEVICE",
    type=click.Choice([NEFIT, IVT], case_sensitive=False),
    required=True,
    help="Bosch device type. NEFIT or IVT.",
)
@click.option(
    "-d",
    "--debug",
    default=False,
    count=True,
    help="Set Debug mode. Single debug is debug of this lib. Second d is debug of aioxmpp as well.",
)
@click.option(
    "-p",
    "--path",
    type=str,
    required=True,
    help="Path to run against. Look at rawscan at possible paths. e.g. /gateway/uuid",
)
@click.pass_context
@coro
async def query(
    ctx,
    host: str,
    token: str,
    password: str,
    protocol: str,
    device: str,
    path: str,
    debug: int,
):
    """Create rawscan of Bosch thermostat."""
    if debug == 0:
        logging.basicConfig(level=logging.INFO)
    if debug > 0:
        _LOGGER.info("Debug mode active")
        _LOGGER.debug(f"Lib version is {bosch.version}")
    if debug > 1:
        logging.getLogger("aioxmpp").setLevel(logging.DEBUG)
        logging.getLogger("aioopenssl").setLevel(logging.DEBUG)
        logging.getLogger("aiosasl").setLevel(logging.DEBUG)
        logging.getLogger("asyncio").setLevel(logging.DEBUG)
    else:
        logging.getLogger("aioxmpp").setLevel(logging.WARN)
        logging.getLogger("aioopenssl").setLevel(logging.WARN)
        logging.getLogger("aiosasl").setLevel(logging.WARN)
        logging.getLogger("asyncio").setLevel(logging.WARN)
    if device.upper() == NEFIT or device.upper() == IVT:
        BoschGateway = bosch.gateway_chooser(device_type=device)
    else:
        _LOGGER.error("Wrong device type.")
        return
    session_type = protocol.upper()
    _LOGGER.info("Connecting to %s with '%s'", host, session_type)
    if session_type == XMPP:
        session = asyncio.get_event_loop()
    elif session_type == HTTP and device.upper() == IVT:
        session = aiohttp.ClientSession()
    else:
        _LOGGER.error("Wrong protocol for this device")
        return
    gateway = BoschGateway(
        session=session,
        session_type=session_type,
        host=host,
        access_token=token,
        password=password,
    )
    await _runquery(gateway, path)
    await gateway.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(cli())
