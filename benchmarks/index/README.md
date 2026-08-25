# Derived-index scale benchmark

This synthetic benchmark measures the current distinction between direct retrieval and the disposable derived-index artifact. **Markdown remains authoritative**; neither result is a fact store or an authorization boundary.

## Reproduce

```bash
PYTHONPATH=src python3 benchmarks/index/scale_benchmark.py
```

The script creates a temporary 240-source Markdown vault, rebuilds an index outside it, then runs the direct lexical query five times. It emits JSON with the direct-search median, index build time, source/record counts, and the returned **relative** path.

## Current decision

The index currently has no query API: `query_path` is `not_implemented` and `can_answer_query` is `false`. Its measured role is therefore **lifecycle-only**—an explicitly rebuilt, integrity-checkable, disposable artifact—not query acceleration.

The timing fields are a reproducibility observation for this synthetic run, **not a performance claim** across machines, filesystems, or user vaults. No threshold is asserted. Any future indexed query path must first preserve direct-scan citations and results, detect staleness/integrity failure, visibly fall back to direct retrieval, and demonstrate a non-flaky measured benefit on an expanded synthetic corpus.
