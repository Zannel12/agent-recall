# Codex synthetic MCP verification protocol

**Status: Documented** — **Documentation-only protocol**. It is a future owner-run procedure, not a repository integration test.

Official host guide: <https://developers.openai.com/codex/mcp>

## Preconditions

- Obtain fresh explicit user approval for this one host action.
- Use only `examples/demo-vault` copied to an owner-selected temporary location.
- Do not use a real vault. No credentials are needed by Cited Vault Recall; do not provide or record host credentials.

## Owner-controlled procedure

The owner follows the official Codex MCP documentation to add one local stdio server with the reviewed command:

```text
cited-vault-recall-mcp --vault <absolute path to synthetic demo vault>
```

Allow only `search` if the host exposes a tool filter. No host configuration or connection is performed by this document or repository test.

## Expected bounded evidence

Capture only non-sensitive evidence that Codex lists the bounded `search` tool and that a `privacy` query returns a citation with `relative_path: privacy.md`. Redact absolute paths. This is not proof that the host loaded Cited Vault Recall until the approved procedure succeeds and direct evidence is retained.

## Rollback

The owner removes only the created Codex MCP entry through the official host procedure, then verifies the entry is absent. Do not edit unrelated configuration.

## Evidence label

Keep the compatibility row `Documented` unless this owner-controlled synthetic procedure succeeds under fresh explicit user approval. Only then may that one row be labelled `Integration-tested`; it never establishes production support.
