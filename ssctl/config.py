import tomllib

from ssctl.path import CONFIG_FILE
from ssctl.types import Action, Config, GlobalConfig, Rule

DEFAULT_CONFIG = """
[global]
default = "allow"

[[rules]]
action = "block"
domain = "ssctl-example.com"
"""


def load_config() -> Config:
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(DEFAULT_CONFIG)

    data = tomllib.loads(CONFIG_FILE.read_text())

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
