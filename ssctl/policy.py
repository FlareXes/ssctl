import fnmatch


class Policy:
    def __init__(self, config):
        self.domains = config.get("blocklist", {}).get("domains", [])

    def is_blocked(self, host: str) -> bool:
        for pattern in self.domains:
            if fnmatch.fnmatch(host, pattern):
                return True
        return False
