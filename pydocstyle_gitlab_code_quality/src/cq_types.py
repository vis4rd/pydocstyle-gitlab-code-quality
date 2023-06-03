from dataclasses import dataclass


@dataclass
class LinesStructure:
    begin: int


@dataclass
class LocationStructure:
    path: str
    lines: LinesStructure


@dataclass
class Issue:
    type: str
    check_name: str
    description: str
    categories: list
    severity: str
    location: LocationStructure
    fingerprint: str
