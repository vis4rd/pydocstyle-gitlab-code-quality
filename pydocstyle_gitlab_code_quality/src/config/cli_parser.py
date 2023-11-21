import argparse
import logging as log

from .config import Config


class CliParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate GitLab Code Quality report from an output of pydocstyle.",
        add_help=True,
        allow_abbrev=False,
    )

    @classmethod
    def initialize(cls) -> None:
        cls._setup_arguments()
        cls._update_config()

    @classmethod
    def _setup_arguments(cls) -> None:
        cls.parser.add_argument(
            "--minor",
            help="Error codes to be displayed with MINOR severity.",
            default=[],
            type=lambda s: s.split(","),
        )
        cls.parser.add_argument(
            "--major",
            help="Error codes to be displayed with MAJOR severity.",
            default=[],
            type=lambda s: s.split(","),
        )
        cls.parser.add_argument(
            "--critical",
            help="Error codes to be displayed with CRITICAL severity.",
            default=[],
            type=lambda s: s.split(","),
        )
        cls.parser.add_argument(
            "-i",
            "--ignore",
            help="Error codes to be omitted from Code Quality report.",
            default="",
            type=lambda s: s.split(","),
        )
        cls.parser.add_argument(
            "-f",
            "--file",
            "--input",
            help="Path to the file with pydocstyle output.",
            default="",
            type=str,
        )
        cls.parser.add_argument(
            "-o",
            "--output",
            help="Path to the file where the Code Quality report will be saved.",
            default="",
            type=str,
        )
        cls.parser.add_argument(
            "--no-stdout",
            help="Do not print the Code Quality report to stdout.",
            action="store_true",
            default=False,
        )

    @classmethod
    def _update_config(cls) -> None:
        args = vars(cls.parser.parse_args())

        if args.get("no_stdout", False):
            Config.output_sinks.pop(0)

        if filepath := args.get("output", ""):
            file = open(filepath, "w", encoding="utf-8")  # pylint: disable=consider-using-with
            Config.output_sinks.append(file)

        if filepath := args.get("file", ""):
            file = open(filepath, "r", encoding="utf-8")  # pylint: disable=consider-using-with
            Config.input_sink = file

        if codes := args.get("minor", []):
            for code in codes:
                Config.code_severities[code] = 1

        if codes := args.get("major", []):
            for code in codes:
                Config.code_severities[code] = 2

        if codes := args.get("critical", []):
            log.info(codes)
            for code in codes:
                Config.code_severities[code] = 3

        if codes := args.get("ignore", []):
            for code in codes:
                Config.code_severities[code] = -1
