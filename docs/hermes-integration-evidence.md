# Hermes synthetic integration evidence

**Status:** Integration-tested (synthetic-only; not Production-tested)
**Host verified:** Hermes Agent v0.20.5, 2026-08-29
**Product:** Cited Vault Recall `0.2.0` (untagged, unpublished release candidate)

## Scope

An owner-approved, temporary Hermes profile connected Cited Vault Recall as a local stdio MCP server over a synthetic vault containing one Markdown document. The experiment did not use a real vault, did not download a model, and did not expose credentials in the product protocol.

## Observed end-to-end result

Hermes discovered exactly one MCP tool, `search`, and completed a model-backed search with the query `privacy`. The final host response included the vault-relative citation:

```text
[privacy.md#privacy]
```

The test profile had all built-in and plugin toolsets disabled before the invocation. The only enabled capability was Cited Vault Recall's `search` MCP tool. No fallback provider was configured for that profile.

## Cleanup

`C3-cleanup` removed the MCP entry, the temporary non-symlink synthetic vault, and the temporary Hermes profile including its profile-local sessions and configuration. Read-back confirmed that the temporary profile and vault no longer existed and that the active default profile had no MCP entry from this experiment.

## Limits

This is Integration-tested evidence for one owner-controlled synthetic-vault path. It is not Production-tested evidence: there was no production deployment, real-vault assessment, production operator/support boundary, observability/retention review, or recurring reliability test. A Hermes runtime warning about stdio child-watcher cleanup was observed during invocation; it did not prevent this bounded smoke result but remains host-runtime maintenance evidence.
