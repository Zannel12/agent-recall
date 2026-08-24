from __future__ import annotations

import fnmatch
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

_WORD_RE = re.compile(r"[\w-]{2,}", re.UNICODE)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
MAX_QUERY_CHARS = 4_096
MAX_LIMIT = 50
MAX_FILE_BYTES = 1_048_576
MAX_OUTPUT_CHARS = 20_000
DEFAULT_SENSITIVITY_PATTERNS = ("*.secret.md", "*.private.md")


class RecallError(ValueError):
    """Stable public diagnostic without sensitive path details."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class UntrustedContent:
    body: str
    trust: str
    source_kind: str
    source_id: str
    executable: bool = False


def untrusted_content(body: str, source_kind: str, source_id: str) -> UntrustedContent:
    """Represent imported text as non-executable, untrusted data."""
    return UntrustedContent(body, "untrusted", source_kind, source_id)


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


def search_vault(vault: Path, query: str, limit: int = 8, diagnostics: dict[str, int] | None = None) -> list[SearchHit]:
    """Return ranked Markdown chunk hits without exposing absolute paths."""
    if diagnostics is not None:
        diagnostics.clear()
        diagnostics["skipped_files"] = 0

    def skipped() -> None:
        if diagnostics is not None:
            diagnostics["skipped_files"] += 1

    terms = _words(query)
    if len(query) > MAX_QUERY_CHARS:
        raise ValueError(f"query length must not exceed {MAX_QUERY_CHARS} characters")
    if not 1 <= limit <= MAX_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
    if not vault.is_dir():
        raise RecallError("VAULT_NOT_FOUND", "Selected vault directory is unavailable")
    resolved_vault = vault.resolve(strict=True)
    ignore_file = vault / ".recallignore"
    ignore_patterns = ()
    if ignore_file.is_file():
        ignore_patterns = tuple(
            line.strip() for line in ignore_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    documents: list[tuple[MarkdownChunk, Counter[str]]] = []
    for path in vault.rglob("*.md"):
        relative_path = path.relative_to(vault).as_posix()
        if any(fnmatch.fnmatchcase(relative_path, pattern) for pattern in ignore_patterns + DEFAULT_SENSITIVITY_PATTERNS):
            skipped()
            continue
        try:
            resolved_path = path.resolve(strict=True)
            resolved_path.relative_to(resolved_vault)
        except (OSError, ValueError):
            skipped()
            continue
        if not resolved_path.is_file():
            skipped()
            continue
        try:
            if resolved_path.stat().st_size > MAX_FILE_BYTES:
                skipped()
                continue
            body = resolved_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            skipped()
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


def render_packet(query: str, hits: list[SearchHit], max_chars: int = MAX_OUTPUT_CHARS) -> str:
    """Render a bounded Markdown packet from cited retrieval hits."""
    if not 1 <= max_chars <= MAX_OUTPUT_CHARS:
        raise ValueError(f"max_chars must be between 1 and {MAX_OUTPUT_CHARS}")
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
    packet = "\n".join(lines).rstrip() + "\n"
    if len(packet) <= max_chars:
        return packet
    if max_chars == 1:
        return "…"
    return packet[: max_chars - 1].rstrip() + "…"


PROFILE_BUDGETS = {"exact": 2_000, "standard": 8_000, "deep": MAX_OUTPUT_CHARS}


def render_profiled_packet(query: str, hits: list[SearchHit], profile: str = "standard") -> tuple[str, dict[str, object]]:
    """Render a named deterministic budget profile with explicit truncation metadata."""
    if profile not in PROFILE_BUDGETS:
        raise ValueError("profile must be exact, standard, or deep")
    budget = PROFILE_BUDGETS[profile]
    full = render_packet(query, hits, MAX_OUTPUT_CHARS)
    packet = render_packet(query, hits, budget)
    return packet, {"profile": profile, "budget_chars": budget, "truncated": len(full) > budget}
