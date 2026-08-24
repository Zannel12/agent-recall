# Architecture

```text
selected local Markdown vault + query
  → frontmatter/title extraction + heading-aware chunks
  → deterministic BM25-style sparse ranking (title, path, chunk body)
  → cited ranked chunks (relative parent path + stable chunk ID + excerpt)
  → Markdown packet or JSON
  → calling agent decides what to use
```

## Frozen target boundaries

[ADR-0003](docs/adr/0003-layered-architecture-boundaries.md) freezes the product’s authority model:

1. **Curated source vault** is the human-controlled canonical evidence.
2. **Trusted retrieval core** is the current read-only parser/chunker/ranker/citation path.
3. A future **managed store** is staged/approved derived memory, never a replacement for curated sources.
4. A future **derived index** is disposable and rebuildable from canonical inputs.
5. A future **semantic layer** is optional ranking only, locally bounded and visibly fallback-safe.
6. **Adapters** are bounded integration edges; they cannot widen filesystem, network, write, or authority scope.

No derived layer, adapter, or score is a source-of-truth substitute for cited canonical evidence.

## Resource limits

- Query: at most `4,096` characters.
- Hit limit: `1`–`50`.
- Markdown input file: at most `1 MiB`; larger candidates are skipped before read.
- Markdown context packet: at most `20,000` characters; deterministic truncation ends in `…`.

Invalid query/limit/budget arguments return deterministic validation errors. JSON output remains an integration format; its packet-budget contract is scheduled separately with B02.3.

## Trust boundary

The vault stays local. Agent Recall resolves the caller-selected vault root before reading and reads a Markdown candidate only when its resolved target remains under that root. External file symlinks and nested directory symlinks are skipped; contained targets remain cited by a relative caller-visible path. It has no network client, API key, agent runtime dependency, or vault-write feature.

## Design choices

- **Relative paths:** packets identify sources without leaking machine paths.
- **Transparent lexical scoring:** users can inspect and modify ranking behavior.
- **Read-only:** retrieval cannot mutate the knowledge base.
- **Agent-neutral:** integrations are adapters, not runtime dependencies.
