from __future__ import annotations

from dataclasses import dataclass
from ._compat import StrEnum

from .staging import MemoryCandidate

MAX_PRE_TURN_LIMIT = 10


class PreTurnDecision(StrEnum):
    NO_ACTION = "no_action"
    REQUEST_RECALL = "request_recall"


class PostTurnDecision(StrEnum):
    NO_ACTION = "no_action"
    STAGE_CANDIDATE = "stage_candidate"


@dataclass(frozen=True)
class PreTurnResult:
    action: PreTurnDecision
    query: str | None = None
    limit: int | None = None


@dataclass(frozen=True)
class PostTurnResult:
    action: PostTurnDecision
    candidate: MemoryCandidate | None = None


@dataclass(frozen=True)
class LifecyclePolicy:
    """Pure opt-in policy; it neither runs recall nor persists candidates."""
    pre_turn_opt_in: bool = False
    query: str | None = None
    limit: int = 5

    def __post_init__(self) -> None:
        if self.pre_turn_opt_in:
            if not self.query or not self.query.strip():
                raise ValueError("query is required for explicit pre-turn recall")
            if not 1 <= self.limit <= MAX_PRE_TURN_LIMIT:
                raise ValueError("limit must be within the bounded pre-turn range")

    def pre_turn(self) -> PreTurnResult:
        if not self.pre_turn_opt_in:
            return PreTurnResult(PreTurnDecision.NO_ACTION)
        return PreTurnResult(PreTurnDecision.REQUEST_RECALL, self.query, self.limit)

    def post_turn(self, candidate: MemoryCandidate | None = None) -> PostTurnResult:
        if candidate is None:
            return PostTurnResult(PostTurnDecision.NO_ACTION)
        if not candidate.qualifies():
            raise ValueError("post-turn staging requires an already-qualified candidate")
        return PostTurnResult(PostTurnDecision.STAGE_CANDIDATE, candidate)
