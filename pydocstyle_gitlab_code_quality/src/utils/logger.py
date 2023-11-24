import logging

from ..config.config import Config

# from sys import stdout


def initialize_logging() -> None:
    root = logging.getLogger()
    root.setLevel(Config.log_level)
    root.disabled = not Config.enable_logging

    # stdout_handler = logging.StreamHandler(stdout)
    # stdout_handler.setLevel(Config.log_level)

    if Config.enable_logging:
        file_handler = logging.FileHandler(Config.log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(Config.log_level)

        root.addHandler(file_handler)
