from mitmproxy import http

from ssctl.config import load_config
from ssctl.policy import Policy


# capture http and https requests
def request(flow: http.HTTPFlow):

    # hot reload config
    config = load_config()
    policy = Policy(config)

    # capture domain e.g. google.com, flarexes.com
    host = flow.request.pretty_host.lower()

    if policy.is_blocked(host):
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
