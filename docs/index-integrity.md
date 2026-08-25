# Derived-index integrity and reindexing

A local index is a disposable derived artifact. Markdown remains authoritative.

## Explicit recovery

```bash
agent-recall reindex --vault /absolute/path/to/vault --destination /absolute/path/to/index.json --json
```

Both paths are supplied by the caller. The destination must be outside the selected vault. Reindexing replaces only that derived destination; it never edits Markdown sources.

## Integrity contract

Each rebuilt index contains:

- an `index_version`;
- source fingerprints with relative path, `mtime_ns`, and SHA-256 content hash;
- an integrity SHA-256 digest for derived records and fingerprints.

A version mismatch, fingerprint change, or digest mismatch means the index requires rebuilding. It does not authorize silent repair of Markdown sources.

No watcher, background refresh, discovery, network, telemetry, cache, or automatic repair is included.
