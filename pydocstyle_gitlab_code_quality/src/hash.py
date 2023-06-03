from __future__ import annotations

from base64 import b64encode
from collections.abc import Hashable, Sequence
from sys import byteorder, hash_info


def get_hash(tpl: Sequence[Hashable]) -> str:
    return b64encode(hash(tpl).to_bytes(hash_info.width // 8, byteorder, signed=True)).decode()
