# Performance envelope

Cited Vault Recall is a local-first package. Its checked-in measurements are reproducible synthetic observations, not service-level objectives or hardware-independent promises.

## What is measured

Two repository scripts exercise bounded synthetic fixtures:

| Fixture | Method | Stable behavior checked | Timing meaning |
|---|---|---|---|
| 240-source derived-index fixture | `PYTHONPATH=src python3 benchmarks/index/scale_benchmark.py` | Direct lexical search returns `scale/note-0173.md`; the derived index is lifecycle-only and cannot answer queries. | Reports a five-run median direct-search observation and index-build observation. |
| 1,000-source lexical fixture | `PYTHONPATH=src python3 benchmarks/retrieval/scale_benchmark.py` | Direct lexical search returns the synthetic target `notes/note-0420.md`. | Reports one local elapsed-time and peak-memory observation. |

Both fixtures create temporary synthetic Markdown rather than reading a user vault. They perform no network request, model load, telemetry, automatic vault discovery, or production indexing.

## Interpretation boundary

The observations are **not machine-independent**: CPU, storage, Python implementation, operating-system scheduling, filesystem caching, background load, and available memory can change them. They are **not a production performance claim** and do not predict behavior for another machine, vault size, Markdown shape, query distribution, or concurrent workload.

**No hard global timing threshold** is asserted. A change may use these scripts to compare like-for-like local observations, but acceptance must preserve the explicit synthetic result and cite its environment/method. It must not convert a one-machine value into a marketing claim, SLA, or cross-platform guarantee.

## Future indexed retrieval

The current derived index remains disposable lifecycle metadata; it has no query path. Any future query acceleration needs a separate benchmarked decision showing equivalent relative citations, visible stale/integrity fallback to direct scanning, and a non-flaky measured benefit on an expanded synthetic corpus.
