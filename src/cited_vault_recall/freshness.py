from __future__ import annotations

from dataclasses import dataclass
from ._compat import StrEnum
from pathlib import Path


class EvidenceStatus(StrEnum):
    CURRENT = "current"
    HISTORICAL = "historical"
    SUPERSEDED = "superseded"
    CONFLICTING = "conflicting"


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    relative_path: str
    observed_at: str
    status: EvidenceStatus

    @classmethod
    def from_dict(cls, value: dict[str, str]) -> "EvidenceRecord":
        if set(value) != {"id", "relative_path", "observed_at", "status"} or not all(isinstance(item, str) for item in value.values()):
            raise ValueError("evidence record has an invalid wire shape")
        return cls(value["id"], value["relative_path"], value["observed_at"], EvidenceStatus(value["status"]))

    def __post_init__(self) -> None:
        path = Path(self.relative_path)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("relative_path must be a contained relative path")

    def to_dict(self) -> dict[str, str]:
        return {"id": self.id, "relative_path": self.relative_path, "observed_at": self.observed_at, "status": self.status.value}


def classify_evidence(*, is_current: bool, superseded_by: str | None = None, conflicts_with: tuple[str, ...] = ()) -> EvidenceStatus:
    """Classify evidence state without inferring truth or modifying any source."""
    if conflicts_with:
        return EvidenceStatus.CONFLICTING
    if superseded_by:
        return EvidenceStatus.SUPERSEDED
    if is_current:
        return EvidenceStatus.CURRENT
    return EvidenceStatus.HISTORICAL
