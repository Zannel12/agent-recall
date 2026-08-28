from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BundleManifest:
    """A declared bundle boundary; it does not create or transfer an archive."""
    schema_version: str
    coverage: tuple[str, ...]
    source_ids: tuple[str, ...]
    complete: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "coverage": list(self.coverage),
            "source_ids": list(self.source_ids),
            "complete": self.complete,
        }

    def __post_init__(self) -> None:
        if not self.schema_version or not self.coverage or not self.source_ids:
            raise ValueError("schema_version, coverage, and source_ids are required")


@dataclass(frozen=True)
class DeletionRequest:
    """A source-linked deletion request; it cannot delete data."""
    target_id: str
    source_id: str

    def __post_init__(self) -> None:
        if not self.target_id or not self.source_id:
            raise ValueError("target_id and source_id are required")


@dataclass(frozen=True)
class RestoreRequest:
    """A restore request that remains quarantined and cannot perform I/O."""
    bundle_id: str
    quarantined: bool = True

    def __post_init__(self) -> None:
        if not self.bundle_id:
            raise ValueError("bundle_id is required")
        if not self.quarantined:
            raise ValueError("restore requests must be quarantined")
