from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

_WORD_RE = re.compile(r"[\w-]{2,}", re.UNICODE)


@dataclass(frozen=True)
class SearchHit:
    score: float
    title: str
    relative_path: str
    excerpt: str


def _words(text: str) -> set[str]:
    return {word.lower() for word in _WORD_RE.findall(text)}


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
    selected = max(content, key=lambda part: sum(term in part.lower() for term in terms))
    compact = re.sub(r"\s+", " ", selected).strip()
    return compact if len(compact) <= max_chars else compact[: max_chars - 1].rstrip() + "…"


def _score(relative_path: str, title: str, body: str, terms: set[str]) -> float:
    counts = Counter(_WORD_RE.findall((title + "\n" + body[:20000]).lower()))
    value = 0.0
    for term in terms:
        if counts[term]:
            value += 1.0 + len(str(counts[term]))
        if term in title.lower():
            value += 4.0
        if term in relative_path.lower():
            value += 2.0
    return value


def search_vault(vault: Path, query: str, limit: int = 8) -> list[SearchHit]:
    """Return ranked Markdown hits without exposing absolute paths."""
    terms = _words(query)
    if not vault.is_dir():
        raise ValueError(f"Vault directory does not exist: {vault}")
    hits: list[SearchHit] = []
    for path in vault.rglob("*.md"):
        try:
            body = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        relative_path = path.relative_to(vault).as_posix()
        title = _title(path, body)
        score = _score(relative_path, title, body, terms)
        if score:
            hits.append(SearchHit(round(score, 3), title, relative_path, _excerpt(body, terms)))
    return sorted(hits, key=lambda hit: (-hit.score, hit.relative_path))[:limit]


def render_packet(query: str, hits: list[SearchHit]) -> str:
    lines = [f"# Librarian Context Packet — {query}", "", "## Sources", ""]
    if not hits:
        lines.append("- No relevant Markdown sources were found.")
    for index, hit in enumerate(hits, 1):
        lines.extend([
            f"### {index}. {hit.title}",
            "",
            f"- Score: `{hit.score}`",
            f"- Source: `{hit.relative_path}`",
            "",
            hit.excerpt,
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
