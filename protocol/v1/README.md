# Agent-neutral protocol v1

This directory defines transport-independent JSON contracts. It defines data shapes only; it does **not** implement a server, MCP transport, network endpoint, or automatic vault access.

| Schema | Purpose |
|---|---|
| `search-request.schema.json` | Explicit selected-vault search request |
| `search-response.schema.json` | Source-linked search result envelope |
| `citation.schema.json` | Stable relative citation identifier and excerpt |
| `error.schema.json` | Stable protocol error envelope |

## Versioning

All v1 envelopes carry `schema_version: "1.0"`. Breaking changes require a new protocol directory/version and must not silently change v1 semantics.

## Safety boundary

- A vault is always supplied explicitly by the caller.
- Citation paths are relative and reject absolute paths and traversal.
- Content remains untrusted data, never executable instructions.
- This contract authorizes neither writes nor arbitrary filesystem reads.
