from typing import List

from ssctl.types import Action, Config, Rule


class Policy:
    def __init__(self, config: Config):
        self.rules: List[Rule] = config.rules

    # Check if the given host matches with rule's domain pattern in config
    # e.g. host = api.flarexes.com, rule = *.flarexes.com, reture true
    def match_host(self, host: str, pattern: str) -> bool:
        # EXACT
        if "*" not in pattern:
            return host == pattern

        # MULTI LEVEL (**)
        if pattern.startswith("**."):
            base = pattern[3:]
            return host == base or host.endswith("." + base)

        # SINGLE LEVEL (*)
        if pattern.startswith("*."):
            base = pattern[2:]

            if not host.endswith("." + base):
                return False

            host_parts = host.split(".")
            base_parts = base.split(".")

            return len(host_parts) == len(base_parts) + 1

        return False

    def is_blocked(self, host: str) -> bool:
        for rule in self.rules:
            if rule.action == Action.BLOCK and self.match_host(host, rule.domain):
                return True

        return False
