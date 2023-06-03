import json
import re
from sys import stdin
from typing import Generator, TextIO

from .src.cq_types import Issue, LinesStructure, LocationStructure
from .src.encoder import DataclassJSONEncoder
from .src.hash import get_hash


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


def get_code_quality_issues() -> Generator:
    output = get_pydocstyle_output(stdin)

    for entry in output:
        yield Issue(
            type="issue",
            check_name=entry["error_code"],
            description=entry["details"],
            categories=["Style"],
            severity="info",
            location=LocationStructure(
                path=entry["path"],
                lines=LinesStructure(begin=int(entry["line"])),
            ),
            fingerprint=get_hash(tuple(entry.values())),
        )


def main() -> None:
    issues: list = list(get_code_quality_issues())
    json_output: str = json.dumps(issues, indent="\t", cls=DataclassJSONEncoder)
    print(json_output)
