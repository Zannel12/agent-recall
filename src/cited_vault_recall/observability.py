from __future__ import annotations

import time
from collections import OrderedDict
from pathlib import Path
from typing import Generic, TypeVar

from .index_integrity import index_needs_rebuild

Value = TypeVar("Value")


class BoundedCache(Generic[Value]):
    """Caller-owned in-memory LRU cache with no persistence or automatic use."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least one")
        self._capacity = capacity
        self._entries: OrderedDict[str, Value] = OrderedDict()

    def get(self, key: str) -> Value | None:
        if key not in self._entries:
            return None
        self._entries.move_to_end(key)
        return self._entries[key]

    def put(self, key: str, value: Value) -> None:
        self._entries[key] = value
        self._entries.move_to_end(key)
        if len(self._entries) > self._capacity:
            self._entries.popitem(last=False)

    def invalidate(self, key: str) -> None:
        self._entries.pop(key, None)

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)


def index_diagnostics(
    vault: Path,
    destination: Path,
    index: object,
    *,
    now_ns: int | None = None,
    latency_ms: float | None = None,
) -> dict[str, bool | float | int | str]:
    """Return aggregate local index diagnostics without paths, queries, or source text."""
    if latency_ms is not None and latency_ms < 0:
        raise ValueError("latency_ms cannot be negative")
    current_ns = time.time_ns() if now_ns is None else now_ns
    age_seconds = max(0, current_ns - destination.stat().st_mtime_ns) / 1_000_000_000
    data = index if isinstance(index, dict) else {}
    fingerprints = data.get("source_fingerprints")
    records = data.get("records")
    version = data.get("index_version")
    return {
        "age_seconds": age_seconds,
        "source_count": len(fingerprints) if isinstance(fingerprints, list) else 0,
        "record_count": len(records) if isinstance(records, list) else 0,
        "index_version": version if isinstance(version, str) else "unknown",
        "rebuild_needed": index_needs_rebuild(vault, index),
        "latency_ms": latency_ms if latency_ms is not None else 0.0,
    }
