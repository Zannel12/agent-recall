# Derived-index integrity and reindexing

A local index is a disposable derived artifact. Markdown remains authoritative.

## Explicit recovery

```bash
cited-vault-recall reindex --vault /absolute/path/to/vault --destination /absolute/path/to/index.json --json
```

Both paths are supplied by the caller. The destination must be outside the selected vault. Reindexing replaces only that derived destination; it never edits Markdown sources.

## Integrity contract

Each rebuilt index contains:

- an `index_version`;
- source fingerprints with relative path, `mtime_ns`, and SHA-256 content hash;
- an integrity SHA-256 digest for derived records and fingerprints.

A version mismatch, fingerprint change, or digest mismatch means the index requires rebuilding. It does not authorize silent repair of Markdown sources.

No watcher, background refresh, discovery, network, telemetry, cache, or automatic repair is included.

## Query-path status

The derived index is currently **lifecycle-only**: it is rebuilt and integrity-checked, but no retrieval command reads it during query execution. The reproducible synthetic measurement in [the scale benchmark](../benchmarks/index/README.md) records this as `query_path: not_implemented`; it makes no cross-machine performance claim. Direct Markdown scanning remains the retrieval path until a separately benchmarked indexed path preserves citations, handles staleness visibly, and proves a benefit.
