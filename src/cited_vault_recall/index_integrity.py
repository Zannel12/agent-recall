from __future__ import annotations

import hashlib
import json
from pathlib import Path

INDEX_VERSION = "1.0"


def source_fingerprints(vault: Path) -> list[dict[str, int | str]]:
    """Return contained Markdown source metadata without writing to the vault."""
    if not vault.is_dir():
        raise ValueError("selected vault is unavailable")
    root = vault.resolve(strict=True)
    fingerprints: list[dict[str, int | str]] = []
    for path in sorted(vault.rglob("*.md")):
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root)
            content = resolved.read_bytes()
            stat = resolved.stat()
        except (OSError, ValueError):
            continue
        fingerprints.append({
            "relative_path": path.relative_to(vault).as_posix(),
            "mtime_ns": stat.st_mtime_ns,
            "sha256": hashlib.sha256(content).hexdigest(),
        })
    return fingerprints


def integrity_digest(records: object, fingerprints: object) -> str:
    """Hash the derived index payload deterministically; it does not authenticate a source."""
    payload = json.dumps(
        {"index_version": INDEX_VERSION, "records": records, "source_fingerprints": fingerprints},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def index_needs_rebuild(vault: Path, index: object) -> bool:
    """Report derived-index staleness or corruption; never repair anything."""
    if not isinstance(index, dict) or index.get("index_version") != INDEX_VERSION:
        return True
    records = index.get("records")
    fingerprints = index.get("source_fingerprints")
    digest = index.get("integrity_sha256")
    if not isinstance(records, list) or not isinstance(fingerprints, list) or not isinstance(digest, str):
        return True
    try:
        if digest != integrity_digest(records, fingerprints):
            return True
        return fingerprints != source_fingerprints(vault)
    except (TypeError, ValueError, OSError):
        return True
