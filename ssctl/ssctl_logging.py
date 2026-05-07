"""
Central logging configuration for ssctl.
"""

import logging
import time
from pathlib import Path

# force UTC timestamps
logging.Formatter.converter = time.gmtime

# log file path
LOG_DIR = Path.home() / ".local/share/ssctl/logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "ssctl.log"


def setup_logging() -> None:
    formatter = logging.Formatter(
        fmt=("%(asctime)s.%(msecs)03dZ | %(levelname)s | %(name)s | %(message)s"),
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # to output logs to a file
    file_handler = logging.FileHandler(LOG_FILE)

    # show logs in terminal, we don't want that
    # file_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)

    # create logger instance
    root_logger = logging.getLogger()

    root_logger.setLevel(logging.INFO)

    # prevent duplicate logs if setup_logging() runs multiple times
    root_logger.handlers.clear()

    # attach file handler
    root_logger.addHandler(file_handler)
