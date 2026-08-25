from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """Python 3.10-compatible string enum for explicit string values."""

    def __str__(self) -> str:
        return str(self.value)
