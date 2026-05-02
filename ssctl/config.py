import tomllib
from pathlib import Path

CONFIG_PATH = Path.home() / ".ssctl.toml"


def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("""
[blocklist]
domains = []
""")
    return tomllib.loads(CONFIG_PATH.read_text())
