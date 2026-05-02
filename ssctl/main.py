import os
import subprocess
import tomllib

import tomli_w
import typer

from ssctl.config import CONFIG_PATH, load_config
from ssctl.proxy import start_proxy

app = typer.Typer()


@app.command()
def start():
    typer.echo("Starting ssctl...")
    start_proxy()


@app.command()
def block(domain: str):
    config = load_config()
    if domain not in config["blocklist"]["domains"]:
        config["blocklist"]["domains"].append(domain)
    else:
        typer.echo(f"Already exist {domain}")

    CONFIG_PATH.write_text(tomli_w.dumps(config))
    typer.echo(f"Blocked {domain}")


@app.command()
def unblock(domain: str):
    config = load_config()
    if domain in config["blocklist"]["domains"]:
        config["blocklist"]["domains"].remove(domain)
        CONFIG_PATH.write_text(tomli_w.dumps(config))
        typer.echo(f"Unblocked {domain}")
    else:
        typer.echo(f"Doesn't exist {domain}")


@app.command()
def list():
    data = tomllib.loads(CONFIG_PATH.read_text())
    for d in data["blocklist"]["domains"]:
        print(d)


if __name__ == "__main__":
    app()
