from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    source_id: str
    kind: str
    trust: str
    path: str
    observed_at: str


@dataclass(frozen=True)
class Citation:
    source_id: str
    chunk_id: str
    line_start: int
    line_end: int


@dataclass(frozen=True)
class Fact:
    fact_id: str
    text: str
    confidence: float
    derived_at: str
    citations: tuple[Citation, ...]
    provenance: tuple[str, ...]
    executable: bool = False



@dataclass(frozen=True)
class EvidenceItem:
    source_id: str
    path: str
    chunk_id: str
    relevance: float
    trust: str
    freshness: str
    provenance: tuple[str, ...]
    schema_version: str = "1.0"

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "source_id": self.source_id,
            "path": self.path,
            "chunk_id": self.chunk_id,
            "relevance": self.relevance,
            "trust": self.trust,
            "freshness": self.freshness,
            "provenance": list(self.provenance),
        }


def derived_fact(
    fact_id: str,
    text: str,
    confidence: float,
    derived_at: str,
    source: Source,
    citation: Citation,
) -> Fact:
    return Fact(
        fact_id=fact_id,
        text=text,
        confidence=confidence,
        derived_at=derived_at,
        citations=(citation,),
        provenance=(source.source_id,),
    )
