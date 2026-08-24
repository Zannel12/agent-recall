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
