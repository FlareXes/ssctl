import logging
from typing import List

from ssctl.exceptions import InvalidPathError
from ssctl.helper import normalize_path, validate_path
from ssctl.types import Action, Config, Rule

logger = logging.getLogger(__name__)


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

    def match_path(self, request_path: str, rule_path: str) -> bool:
        try:
            pattern = validate_path(rule_path)
        except InvalidPathError as e:
            logger.warning(f"{e} - {rule_path}")
            return False

        request_path = normalize_path(request_path)

        if request_path == pattern:
            return True

        return False

    def is_blocked(self, host: str, request_path: str) -> bool:
        for rule in self.rules:
            if not rule.action == Action.BLOCK:
                continue

            if not self.match_host(host, rule.domain):
                continue

            if rule.path and not self.match_path(request_path, rule.path):
                continue

            return True

        return False
