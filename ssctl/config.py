import tomllib
from pathlib import Path

from ssctl.types import Action, Config, GlobalConfig, Rule

CONFIG_PATH = Path.home() / ".ssctl.toml"

DEFAULT_CONFIG = """
[global]
default = "allow"

[[rules]]
action = "block"
domain = "example.com"
"""


def load_config() -> Config:
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(DEFAULT_CONFIG)

    data = tomllib.loads(CONFIG_PATH.read_text())

    # get defualt global config
    global_cfg_default = data.get("global", {}).get("default", "allow")

    # list to store typed Rule objects
    rules = []

    for rule in data.get("rules", []):
        domain = rule.get("domain")

        if not domain:
            continue

        rule = Rule(
            # if "action" missing → default to "allow"
            action=Action(rule.get("action", "allow")),
            domain=domain.lower(),
            path=rule.get("path"),
        )

        rules.append(rule)

    return Config(global_config=GlobalConfig(default=global_cfg_default), rules=rules)
