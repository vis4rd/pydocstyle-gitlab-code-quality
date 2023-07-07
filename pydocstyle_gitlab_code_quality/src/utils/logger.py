import logging
from sys import stdout

from ..config.config import Config


def initialize_logging() -> None:
    root = logging.getLogger()
    root.setLevel(Config.log_level)

    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.setLevel(Config.log_level)

    file_handler = logging.FileHandler("latest.log", mode="w", encoding="utf-8")
    file_handler.setLevel(Config.log_level)

    # root.addHandler(stdout_handler)
    root.addHandler(file_handler)
