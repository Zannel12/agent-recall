from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


_ELIGIBLE_KINDS = frozenset({"decision", "preference", "project_fact", "safety_boundary"})


def is_memory_worthy(*, kind: str, durable: bool, source_id: str) -> bool:
    """Return whether explicit, sourced information may enter local staging."""
    return kind in _ELIGIBLE_KINDS and durable and bool(source_id)


@dataclass(frozen=True)
class MemoryCandidate:
    kind: str
    text: str
    source_id: str
    durable: bool

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind, "text": self.text, "source_id": self.source_id, "durable": self.durable}

    def qualifies(self) -> bool:
        return is_memory_worthy(kind=self.kind, durable=self.durable, source_id=self.source_id)


@dataclass(frozen=True)
class ReviewDecision:
    """An explicit review outcome; it does not persist or promote a candidate."""
    candidate: MemoryCandidate
    outcome: str

    def to_dict(self) -> dict[str, object]:
        return {"outcome": self.outcome, "candidate": self.candidate.to_dict()}

    def __post_init__(self) -> None:
        if self.outcome not in {"approved", "rejected"}:
            raise ValueError("outcome must be approved or rejected")


def append_candidate(destination: Path, candidate: MemoryCandidate) -> None:
    """Append one qualifying candidate to an explicit local JSONL staging file."""
    if not candidate.qualifies():
        raise ValueError("candidate is not eligible for staging")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(candidate.to_dict(), sort_keys=True) + "\n")
