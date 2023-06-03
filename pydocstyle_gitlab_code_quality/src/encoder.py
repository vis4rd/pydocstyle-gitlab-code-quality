from dataclasses import asdict, is_dataclass
from json import JSONEncoder
from typing import Any


class DataclassJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)
