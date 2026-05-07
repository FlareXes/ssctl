# proxy.py

import asyncio
import logging

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from ssctl import blocker

logger = logging.getLogger(__name__)


async def _run_proxy():
    opts = Options(listen_host="127.0.0.1", listen_port=8080)

    # create mitmproxy instance and disable mitmproxy terminal logging
    mitmdump = DumpMaster(opts, with_termlog=False)

    # register our addon/module
    mitmdump.addons.add(blocker)

    # logs
    logger.info("Registered blocker addon")
    logger.info("Starting ssctl proxy on 127.0.0.1:8080")

    try:
        await mitmdump.run()

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping ssctl proxy...")

        # shutdown() is not async
        mitmdump.shutdown()

        logger.info("ssctl proxy stopped")


def start_proxy():
    asyncio.run(_run_proxy())
