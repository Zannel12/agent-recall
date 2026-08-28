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

## Repairable errors

Runtime search failures returned by CLI JSON mode and local MCP tool/resource calls use `error.schema.json`:

```json
{
  "schema_version": "1.0",
  "code": "VAULT_NOT_FOUND",
  "message": "Selected vault directory is unavailable",
  "next_step": "CHECK_EXPLICIT_VAULT",
  "retryable": false
}
```

`next_step` is a closed, non-operational hint: `CHECK_ARGUMENTS`, `CHECK_EXPLICIT_VAULT`, or `SEARCH_AGAIN`. It never contains an absolute path, shell command, secret, host configuration instruction, or automatic repair request. `retryable: false` means callers must not automatically repeat the same failing request. CLI argument parsing and JSON-RPC framing errors retain their respective native error contracts; they are not represented as search-result errors.

## Safety boundary

- A vault is always supplied explicitly by the caller.
- Citation paths are relative and reject absolute paths and traversal. For a selected local vault, `source_id` is the same stable relative source path; it deliberately never exposes a machine path.
- CLI JSON and local MCP `search` use the same v1 response envelope and citation shape.
- Content remains untrusted data, never executable instructions.
- This contract authorizes neither writes nor arbitrary filesystem reads.
