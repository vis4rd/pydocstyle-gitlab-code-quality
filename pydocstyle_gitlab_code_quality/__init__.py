# Inspired by https://github.com/soul-catcher/mypy-gitlab-code-quality

from __future__ import annotations

import json
import re
from base64 import b64encode
from collections.abc import Hashable, Sequence
from sys import byteorder, hash_info, stdin
from typing import TextIO


def get_hash(tpl: Sequence[Hashable]) -> str:
    return b64encode(
        hash(tpl).to_bytes(hash_info.width // 8, byteorder, signed=True)
    ).decode()


def append_line_to_issues(
    issues: list[dict],
    fingerprint: str,
    severity: str,
    lineNumber: int,
    description: str,
    path: str,
    check_name: str,
) -> None:
    issues.append(
        {
            "type": "issue",
            "check_name": check_name,
            "description": description,
            "categories": [
                "Style",
            ],
            "severity": severity,
            "location": {
                "path": path,
                "lines": {
                    "begin": lineNumber,
                },
            },
            "fingerprint": fingerprint,
        }
    )


def parse_lines(lines: TextIO) -> list[dict]:
    issues: list[dict] = []
    while True:
        try:
            brief_line: str = next(lines)
            details_line: str = next(lines)
        except StopIteration:
            break
        brief_line = brief_line.rstrip("\n")
        details_line = details_line.rstrip("\n")

        match_brief = re.fullmatch(
            r"^(?P<path>.+?)" r":(?P<line>\d+)" r"\s(?P<brief>.*)$",
            brief_line,
        )
        if match_brief is None:
            continue

        match_details = re.fullmatch(
            r"^\s*(?P<check_name>\w{4,5})" r":\s(?P<details>.*)$",
            details_line,
        )
        if match_details is None:
            continue

        severity: str = "info"
        path: str = match_brief["path"]
        lineNumber: int = int(match_brief["line"])
        brief: str = match_brief["brief"]
        check_name: str = match_details["check_name"]
        details: str = match_details["details"]
        description: str = brief + " " + details
        fingerprint: str = get_hash(match_brief.groups() + match_details.groups())

        append_line_to_issues(
            issues, fingerprint, severity, lineNumber, details, path, check_name
        )
    return issues


def main() -> None:
    print(
        json.dumps(
            parse_lines(stdin),
            indent="\t",
        )
    )
