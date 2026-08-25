from __future__ import annotations

from dataclasses import dataclass
from ._compat import StrEnum


class LifecycleAction(StrEnum):
    CORRECT = "correct"
    INVALIDATE = "invalidate"
    EXPIRE = "expire"


@dataclass(frozen=True)
class CorrectionRequest:
    """A source-linked lifecycle request; it cannot mutate a stored record."""
    target_id: str
    action: LifecycleAction
    evidence_id: str
    replacement_value: str | None = None
    expires_at: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "target_id": self.target_id,
            "action": self.action.value,
            "evidence_id": self.evidence_id,
            "replacement_value": self.replacement_value,
            "expires_at": self.expires_at,
        }

    def __post_init__(self) -> None:
        if not self.target_id or not self.evidence_id:
            raise ValueError("target_id and evidence_id are required")
        if self.action is LifecycleAction.CORRECT and not self.replacement_value:
            raise ValueError("a correction requires a replacement_value")
        if self.action is LifecycleAction.EXPIRE and not self.expires_at:
            raise ValueError("an expiry requires an explicit expires_at")
