import logging
from sys import stdin, stdout
from typing import TextIO


class Config:
    verbose: bool = False
    log_level: int = logging.INFO
    code_severities: dict[str, int] = (
        {f"D1{i:02d}": 0 for i in range(0, 8)}
        | {f"D2{i:02d}": 0 for i in range(0, 16)}
        | {f"D3{i:02d}": 0 for i in range(0, 3)}
        | {f"D4{i:02d}": 0 for i in range(0, 20)}
    )
    input_sink: TextIO = stdin
    output_sinks: list[TextIO] = [stdout]
