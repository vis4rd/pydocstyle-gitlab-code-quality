import logging
from sys import stdin, stdout
from typing import Dict, List, TextIO


class Config:
    enable_logging: bool = False
    log_file: str = "pgcq_latest.log"
    log_level: int = logging.INFO

    code_severities: Dict[str, int] = {}
    code_severities.update({f"D1{i:02d}": 0 for i in range(0, 8)})
    code_severities.update({f"D2{i:02d}": 0 for i in range(0, 16)})
    code_severities.update({f"D3{i:02d}": 0 for i in range(0, 3)})
    code_severities.update({f"D4{i:02d}": 0 for i in range(0, 20)})

    input_sink: TextIO = stdin
    output_sinks: List[TextIO] = [stdout]
