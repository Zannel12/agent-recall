from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

_WORD_RE = re.compile(r"[\w-]{2,}", re.UNICODE)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


@dataclass(frozen=True)
class SearchHit:
    score: float
    score_components: dict[str, float]
    title: str
    relative_path: str
    chunk_id: str
    heading: str
    excerpt: str


@dataclass(frozen=True)
class MarkdownChunk:
    source_title: str
    relative_path: str
    chunk_id: str
    heading: str
    body: str


def normalize_text(text: str) -> str:
    """Normalize text for deterministic Unicode-insensitive matching."""
    return unicodedata.normalize("NFC", text).casefold()


def _words(text: str) -> set[str]:
    return set(_WORD_RE.findall(normalize_text(text)))


def _frontmatter(body: str) -> tuple[dict[str, str], str]:
    if not body.startswith("---\n"):
        return {}, body
    closing = body.find("\n---\n", 4)
    if closing == -1:
        return {}, body
    metadata: dict[str, str] = {}
    for line in body[4:closing].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip().casefold()] = value.strip().strip("\"'")
    return metadata, body[closing + 5 :]


def _title(path: Path, body: str) -> str:
    metadata, content = _frontmatter(body)
    if metadata.get("title"):
        return metadata["title"]
    for line in content.splitlines()[:40]:
        match = _HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
    return path.stem


def _slug(text: str) -> str:
    words = _WORD_RE.findall(normalize_text(text))
    return "-".join(words) or "section"


def chunk_markdown(relative_path: str, body: str) -> list[MarkdownChunk]:
    """Split Markdown into heading-aware chunks with stable source backlinks."""
    metadata, content = _frontmatter(body)
    source_title = metadata.get("title") or _title(Path(relative_path), body)
    chunks: list[MarkdownChunk] = []
    heading_stack: list[tuple[int, str]] = []
    current_heading = source_title
    current_lines: list[str] = []
    has_heading = False
    identifiers: Counter[str] = Counter()

    def append_chunk() -> None:
        nonlocal current_lines
        if not current_lines and not has_heading:
            return
        base_id = f"{relative_path}#{_slug(current_heading)}"
        identifiers[base_id] += 1
        chunk_id = base_id if identifiers[base_id] == 1 else f"{base_id}-{identifiers[base_id]}"
        chunks.append(MarkdownChunk(
            source_title,
            relative_path,
            chunk_id,
            current_heading,
            "\n".join(current_lines).strip(),
        ))
        current_lines = []

    for line in content.splitlines():
        match = _HEADING_RE.match(line)
        if not match:
            current_lines.append(line)
            continue
        if current_lines or has_heading:
            append_chunk()
        level = len(match.group(1))
        heading_text = match.group(2).strip()
        while heading_stack and heading_stack[-1][0] >= level:
            heading_stack.pop()
        heading_stack.append((level, heading_text))
        current_heading = " > ".join(text for _, text in heading_stack)
        has_heading = True

    append_chunk()
    if not chunks:
        chunks.append(MarkdownChunk(source_title, relative_path, f"{relative_path}#document", source_title, ""))
    return chunks


def _excerpt(body: str, terms: set[str], max_chars: int = 700) -> str:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
    if not paragraphs:
        return ""
    selected = max(paragraphs, key=lambda part: sum(term in normalize_text(part) for term in terms))
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
    """Return ranked Markdown chunk hits without exposing absolute paths."""
    terms = _words(query)
    if not vault.is_dir():
        raise ValueError(f"Vault directory does not exist: {vault}")
    resolved_vault = vault.resolve(strict=True)
    documents: list[tuple[MarkdownChunk, Counter[str]]] = []
    for path in vault.rglob("*.md"):
        try:
            resolved_path = path.resolve(strict=True)
            resolved_path.relative_to(resolved_vault)
        except (OSError, ValueError):
            continue
        if not resolved_path.is_file():
            continue
        try:
            body = resolved_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        relative_path = path.relative_to(vault).as_posix()
        for chunk in chunk_markdown(relative_path, body):
            counts = Counter(_WORD_RE.findall(normalize_text(
                f"{chunk.source_title}\n{chunk.heading}\n{chunk.body[:20000]}"
            )))
            documents.append((chunk, counts))

    if not documents:
        return []
    document_frequency = Counter(
        term for term in terms for _, counts in documents if counts[term]
    )
    average_document_length = max(
        sum(sum(counts.values()) for _, counts in documents) / len(documents), 1.0
    )
    hits: list[SearchHit] = []
    for chunk, counts in documents:
        result_title = chunk.source_title if chunk.heading == chunk.source_title else f"{chunk.source_title} — {chunk.heading}"
        score, score_components = _score(
            chunk.relative_path,
            result_title,
            counts,
            sum(counts.values()),
            average_document_length,
            document_frequency,
            len(documents),
            terms,
        )
        if score:
            hits.append(SearchHit(
                score,
                score_components,
                result_title,
                chunk.relative_path,
                chunk.chunk_id,
                chunk.heading,
                _excerpt(chunk.body, terms),
            ))
    return sorted(hits, key=lambda hit: (-hit.score, hit.chunk_id))[:limit]


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
            f"- Chunk: `{hit.chunk_id}`",
            "",
            hit.excerpt,
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
