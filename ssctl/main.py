import tomli_w
import typer

from ssctl.config import CONFIG_PATH, load_config
from ssctl.helper import typed_config_to_dict
from ssctl.proxy import start_proxy
from ssctl.types import Action, Rule

app = typer.Typer()


@app.command()
def start():
    typer.echo("Starting ssctl...")
    start_proxy()


@app.command()
def block(domain: str):
    domain = domain.lower()  # sanitize
    config = load_config()
    domains = [r.domain for r in config.rules]

    if domain in domains:
        typer.echo(f"Already exist {domain}")
        return

    config.rules.append(Rule(action=Action.BLOCK, domain=domain))

    # convert typed → dict → TOML
    CONFIG_PATH.write_text(tomli_w.dumps(typed_config_to_dict(config)))

    typer.echo(f"Blocked {domain}")


@app.command()
def unblock():
    # Why? It's difficult to remove rules
    # if multiple rules are present under same domain
    # next step -> multi select mode or GUI
    typer.echo(f"Users have to remove the rule directly from {CONFIG_PATH}")


@app.command()
def list():
    config = load_config()
    for rule in config.rules:
        typer.echo(f"{rule.action.value} -> {rule.domain}")
        # typer.echo(f"{rule.action.value} -> {rule.domain}{rule.path or ''}")


if __name__ == "__main__":
    app()
