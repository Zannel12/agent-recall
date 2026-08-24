from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

_WORD_RE = re.compile(r"[\w-]{2,}", re.UNICODE)


@dataclass(frozen=True)
class SearchHit:
    score: float
    score_components: dict[str, float]
    title: str
    relative_path: str
    excerpt: str


def normalize_text(text: str) -> str:
    """Normalize text for deterministic Unicode-insensitive matching."""
    return unicodedata.normalize("NFC", text).casefold()


def _words(text: str) -> set[str]:
    return set(_WORD_RE.findall(normalize_text(text)))


def _title(path: Path, body: str) -> str:
    for line in body.splitlines()[:40]:
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def _excerpt(body: str, terms: set[str], max_chars: int = 700) -> str:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
    content = [part for part in paragraphs if not re.fullmatch(r"#{1,6}\s+.+", part)]
    if not content:
        content = paragraphs
    if not content:
        return ""
    selected = max(content, key=lambda part: sum(term in normalize_text(part) for term in terms))
    compact = re.sub(r"\s+", " ", selected).strip()
    return compact if len(compact) <= max_chars else compact[: max_chars - 1].rstrip() + "…"


def _score(
    relative_path: str,
    title: str,
    counts: Counter[str],
    document_length: int,
    average_document_length: float,
    document_frequency: Counter[str],
    document_count: int,
    terms: set[str],
) -> tuple[float, dict[str, float]]:
    bm25 = 0.0
    title_boost = 0.0
    path_boost = 0.0
    normalized_title = normalize_text(title)
    normalized_path = normalize_text(relative_path)
    for term in terms:
        term_frequency = counts[term]
        if term_frequency:
            inverse_document_frequency = log(
                1 + (document_count - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5)
            )
            bm25 += inverse_document_frequency * (
                term_frequency * 2.2
            ) / (term_frequency + 1.2 * (1 - 0.75 + 0.75 * document_length / average_document_length))
        if term in normalized_title:
            title_boost += 4.0
        if term in normalized_path:
            path_boost += 2.0
    components = {
        "bm25": round(bm25, 3),
        "title_boost": title_boost,
        "path_boost": path_boost,
    }
    return round(sum(components.values()), 3), components


def search_vault(vault: Path, query: str, limit: int = 8) -> list[SearchHit]:
    """Return ranked Markdown hits without exposing absolute paths."""
    terms = _words(query)
    if not vault.is_dir():
        raise ValueError(f"Vault directory does not exist: {vault}")
    documents: list[tuple[str, str, str, Counter[str]]] = []
    for path in vault.rglob("*.md"):
        try:
            body = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        relative_path = path.relative_to(vault).as_posix()
        title = _title(path, body)
        counts = Counter(_WORD_RE.findall(normalize_text(title + "\n" + body[:20000])))
        documents.append((relative_path, title, body, counts))

    if not documents:
        return []
    document_frequency = Counter(
        term for term in terms for _, _, _, counts in documents if counts[term]
    )
    average_document_length = sum(sum(counts.values()) for _, _, _, counts in documents) / len(documents)
    hits: list[SearchHit] = []
    for relative_path, title, body, counts in documents:
        score, score_components = _score(
            relative_path,
            title,
            counts,
            sum(counts.values()),
            average_document_length,
            document_frequency,
            len(documents),
            terms,
        )
        if score:
            hits.append(SearchHit(score, score_components, title, relative_path, _excerpt(body, terms)))
    return sorted(hits, key=lambda hit: (-hit.score, hit.relative_path))[:limit]


def render_packet(query: str, hits: list[SearchHit]) -> str:
    lines = [f"# Librarian Context Packet — {query}", "", "## Sources", ""]
    if not hits:
        lines.append("- No relevant Markdown sources were found.")
    for index, hit in enumerate(hits, 1):
        score_details = ", ".join(
            f"{name}={value:.3f}" for name, value in hit.score_components.items()
        )
        lines.extend([
            f"### {index}. {hit.title}",
            "",
            f"- Score: `{hit.score}`",
            f"- Score details: {score_details}",
            f"- Source: `{hit.relative_path}`",
            "",
            hit.excerpt,
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
