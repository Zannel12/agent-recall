from __future__ import annotations

import json
import tempfile
import time
import tracemalloc
from pathlib import Path

from cited_vault_recall.core import search_vault

FILE_COUNT = 1_000
QUERY = "synthetic retrieval target"
TARGET = "notes/note-0420.md"


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        vault = Path(directory)
        for index in range(FILE_COUNT):
            path = vault / "notes" / f"note-{index:04d}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            body = f"# Synthetic note {index}\n\nBackground corpus text {index}.\n"
            if index == 420:
                body += "Synthetic retrieval target is present here.\n"
            path.write_text(body, encoding="utf-8")

        tracemalloc.start()
        started = time.perf_counter()
        hits = search_vault(vault, QUERY, limit=5)
        latency_ms = round((time.perf_counter() - started) * 1000, 3)
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    print(json.dumps({
        "corpus": {"file_count": FILE_COUNT, "synthetic": True},
        "query": QUERY,
        "latency_ms": latency_ms,
        "peak_memory_bytes": peak_bytes,
        "quality": {"target_path": TARGET, "retrieved": TARGET in [hit.relative_path for hit in hits]},
        "production_index": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
