from ssctl.types import Config


def typed_config_to_dict(config: Config) -> dict:
    return {
        "global": {
            "default": config.global_config.default,
        },
        "rules": [
            {
                "action": rule.action.value,
                "domain": rule.domain,
                **({"path": rule.path} if rule.path else {}),
            }
            for rule in config.rules
        ],
    }
