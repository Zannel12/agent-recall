"""Synthetic, read-only measurement of current derived-index query-path value."""

from __future__ import annotations

import json
import statistics
import tempfile
import time
from pathlib import Path
from typing import cast

from cited_vault_recall.core import build_local_index, search_vault


SOURCE_COUNT = 240
TARGET = 173
QUERY = "target evidence"


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        vault = root / "vault"
        notes = vault / "scale"
        notes.mkdir(parents=True)
        for number in range(SOURCE_COUNT):
            body = "target evidence" if number == TARGET else "ordinary synthetic content"
            (notes / f"note-{number:04}.md").write_text(
                f"# Synthetic note {number}\n\n{body}. " * 8,
                encoding="utf-8",
            )
        index_destination = root / "derived" / "index.json"
        started = time.perf_counter_ns()
        index = build_local_index(vault, index_destination)
        build_ns = time.perf_counter_ns() - started
        timings: list[int] = []
        paths: list[str] = []
        for _ in range(5):
            started = time.perf_counter_ns()
            hits = search_vault(vault, QUERY, 1)
            timings.append(time.perf_counter_ns() - started)
            paths = [hit.relative_path for hit in hits]
        report = {
            "dataset": "synthetic-derived-index-v1",
            "source_count": SOURCE_COUNT,
            "direct_search": {"runs": len(timings), "median_ns": int(statistics.median(timings)), "relative_paths": paths},
            "derived_index": {
                "build_ns": build_ns,
                "record_count": len(cast(list[object], index["records"])),
                "query_path": "not_implemented",
                "can_answer_query": False,
            },
            "decision": "lifecycle_only",
        }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
