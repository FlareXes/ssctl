# proxy.py

import asyncio

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from ssctl import blocker


async def _run():
    opts = Options(listen_host="127.0.0.1", listen_port=8080)

    m = DumpMaster(opts)
    m.addons.add(blocker)

    try:
        await m.run()
    except KeyboardInterrupt:
        await m.shutdown()


def start_proxy():
    asyncio.run(_run())
