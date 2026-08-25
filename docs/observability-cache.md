# Local observability and cache policy

## Aggregate diagnostics

`index_diagnostics(vault, destination, index, ...)` returns only local aggregates:

- derived-index age in seconds;
- source and record counts;
- index format version;
- whether a rebuild is required;
- caller-supplied measured latency in milliseconds.

It never returns an absolute path, source name, query, or document body. It does not emit telemetry.

## Bounded cache

`BoundedCache` is an explicit caller-owned, process-local LRU cache. It has a positive fixed entry capacity and only these lifecycle operations:

- `get(key)`;
- `put(key, value)`;
- `invalidate(key)`;
- `clear()`.

There is no default global cache, persistence, automatic search/MCP wiring, TTL, watcher, background cleanup, discovery, or network behavior. Callers choose cache keys and must explicitly invalidate values when their own context changes.
