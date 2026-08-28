# Hermes synthetic MCP verification protocol

**Status: Documented** — **Documentation-only protocol**. It is a future owner-run procedure, not a repository integration test.

Official host guide: <https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes>

## Preconditions

- Obtain fresh explicit user approval for this one host action.
- Use only `examples/demo-vault` copied to an owner-selected temporary location.
- Use the reviewed, non-executing `build_hermes_mcp_plan(...)` output; do not discover config or server names.
- Do not use a real vault. No credentials are needed by Cited Vault Recall; do not provide or record host credentials.

## Owner-controlled procedure

The owner uses the official Hermes workflow to review and apply the narrow local-stdio entry only after approval:

```text
cited-vault-recall-mcp --vault <absolute path to synthetic demo vault>
```

Expose only `search`; keep sampling disabled. No host configuration or connection is performed by this document or repository test.

## Expected bounded evidence

Capture only non-sensitive evidence that Hermes lists the bounded `search` tool and that a `privacy` query returns a citation with `relative_path: privacy.md`. Redact absolute paths. This is not proof that the host loaded Cited Vault Recall until the approved procedure succeeds and direct evidence is retained.

## Rollback

The owner removes only the created MCP entry using the reviewed Hermes rollback vector or the host's official UI, then verifies the entry is absent. Do not edit unrelated configuration.

## Evidence label

Keep the compatibility row `Documented` unless this owner-controlled synthetic procedure succeeds under fresh explicit user approval. Only then may that one row be labelled `Integration-tested`; it never establishes production support.
