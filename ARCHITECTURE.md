# Architecture

```text
selected local Markdown vault + query
  → frontmatter/title extraction + heading-aware chunks
  → deterministic BM25-style sparse ranking (title, path, chunk body)
  → cited ranked chunks (relative parent path + stable chunk ID + excerpt)
  → Markdown packet or JSON
  → calling agent decides what to use
```

## Trust boundary

The vault stays local. Agent Recall reads only `.md` files under the path supplied by the caller. It has no network client, API key, agent runtime dependency, or vault-write feature.

## Design choices

- **Relative paths:** packets identify sources without leaking machine paths.
- **Transparent lexical scoring:** users can inspect and modify ranking behavior.
- **Read-only:** retrieval cannot mutate the knowledge base.
- **Agent-neutral:** integrations are adapters, not runtime dependencies.
