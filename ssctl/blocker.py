import logging
from urllib.parse import urlsplit, urlunsplit

from mitmproxy import http

from ssctl.config import load_config
from ssctl.policy import Policy

logger = logging.getLogger(__name__)


# capture http and https requests
def request(flow: http.HTTPFlow):

    # hot reload config
    config = load_config()
    policy = Policy(config)

    # capture domain e.g. google.com, flarexes.com
    host = flow.request.pretty_host.lower()
    host = host.encode("idna").decode("ascii")

    # capture path e.g. /about, /user?id=1
    request_path = flow.request.path

    if policy.is_blocked(host, request_path):
        # capture domain + path without params for logs
        parsed = urlsplit(flow.request.pretty_url)
        url = urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                "",  # query
                "",  # fragment
            )
        )
        logger.info(f"Policy Block {url}")

        flow.response = http.Response.make(
            200,
            b"""
            <html>
              <body style="font-family:sans-serif;text-align:center;margin-top:20%">
                <h1>Blocked by ssctl</h1>
                <p>This site is restricted</p>
              </body>
            </html>
            """,
            {"Content-Type": "text/html"},
        )
