from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MutationIntent:
    """A reviewable requested action, deliberately separate from execution."""
    action: str
    target_id: str
    replacement_value: str | None = None


@dataclass(frozen=True)
class InspectableMemory:
    """Read-only view: identity, claimed value, validity state, and evidence."""
    id: str
    value: str
    status: str
    evidence_id: str

    def to_dict(self) -> dict[str, str]:
        return {"id": self.id, "value": self.value, "status": self.status, "evidence_id": self.evidence_id}
