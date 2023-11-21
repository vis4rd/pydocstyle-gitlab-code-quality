import json
import logging as log
import re
from hashlib import md5
from typing import Dict, Generator, List, TextIO

from .src.config.cli_parser import CliParser
from .src.config.config import Config
from .src.cq_types import Issue, LinesStructure, LocationStructure
from .src.utils.encoder import DataclassJSONEncoder
from .src.utils.logger import initialize_logging


def get_pydocstyle_output(output: TextIO) -> Generator[dict, None, None]:
    path_regex: str = r"^(?P<path>.+?)"
    line_regex: str = r":(?P<line>\d+)"
    brief_regex: str = r"\s(?P<brief>.*)$"
    error_code_regex: str = r"^\s*(?P<error_code>\w{4,5})"
    details_regex: str = r":\s(?P<details>.*)$"

    while True:
        try:
            brief_line: str = next(output)
            details_line: str = next(output)
        except StopIteration:
            return

        if not brief_line or not details_line:
            return

        brief_line = brief_line.rstrip("\n")
        details_line = details_line.rstrip("\n")

        match_brief = re.fullmatch(path_regex + line_regex + brief_regex, brief_line)
        if match_brief is None:
            continue

        match_details = re.fullmatch(error_code_regex + details_regex, details_line)
        if match_details is None:
            continue

        errors = match_brief.groupdict()
        errors.update(match_details.groupdict())

        yield errors


def get_code_quality_issues() -> Generator[Issue, None, None]:
    log.info(f"Input sink = {Config.input_sink}")
    output = get_pydocstyle_output(Config.input_sink)

    severity_mapper: Dict[int, str] = {0: "info", 1: "minor", 2: "major", 3: "critical"}

    for entry in output:
        severity_index: int = Config.code_severities[entry["error_code"]]
        if severity_index >= 0:
            yield Issue(
                type="issue",
                check_name=entry["error_code"],
                description=entry["details"],
                categories=["Style"],
                severity=severity_mapper[severity_index],
                location=LocationStructure(
                    path=entry["path"],
                    lines=LinesStructure(begin=int(entry["line"])),
                ),
                fingerprint=md5("".join(entry.values()).encode("utf-8")).hexdigest(),
            )


def main() -> None:
    CliParser.initialize()
    initialize_logging()

    issues: List[Issue] = list(get_code_quality_issues())
    json_output: str = json.dumps(issues, indent="\t", cls=DataclassJSONEncoder)

    for sink in Config.output_sinks:
        sink.write(json_output)
