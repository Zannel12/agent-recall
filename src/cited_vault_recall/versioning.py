from __future__ import annotations

from dataclasses import dataclass
from ._compat import StrEnum


class Compatibility(StrEnum):
    READY = "ready"
    MIGRATION_REQUIRED = "migration_required"


class RecoveryAction(StrEnum):
    REBUILD_DERIVED = "rebuild_derived"
    STOP_AND_REPORT = "stop_and_report"


def assess_recovery(*, derived: bool, corrupt: bool) -> RecoveryAction:
    """Select a non-destructive response; never repair data silently."""
    if corrupt and derived:
        return RecoveryAction.REBUILD_DERIVED
    return RecoveryAction.STOP_AND_REPORT


@dataclass(frozen=True)
class VersionSet:
    product: str
    protocol: str
    schema: str
    index: str



@dataclass(frozen=True)
class MigrationPlan:
    """Declarative migration precondition; it cannot execute a migration."""
    from_version: str
    to_version: str
    snapshot_id: str
    rollback_target: str


def assess_compatibility(stored: VersionSet, supported: VersionSet) -> Compatibility:
    """Report compatibility only; never run migration or alter stored data."""
    return Compatibility.READY if stored == supported else Compatibility.MIGRATION_REQUIRED
