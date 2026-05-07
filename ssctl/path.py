"""
Central filesystem paths for ssctl.

Eveything should be under ~/.local/share/ssctl/
"""

from pathlib import Path

# -----------------------------------------------------------------------------
# Base directories
# -----------------------------------------------------------------------------

HOME_DIR = Path.home()

# -----------------------------------------------------------------------------
# App directories
# -----------------------------------------------------------------------------

DATA_DIR = HOME_DIR / ".local/share/ssctl"

LOG_DIR = DATA_DIR / "logs"

# -----------------------------------------------------------------------------
# Ensure directories exist
# -----------------------------------------------------------------------------

DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------

CONFIG_FILE = DATA_DIR / "ssctl.toml"

LOG_FILE = LOG_DIR / "ssctl.log"
