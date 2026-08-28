# Migration and deprecation policy

## Current status

Cited Vault Recall is at `0.2.0.dev0`, an unreleased development scope. The local ADR-0002 package/import/console migration is implemented; this policy performs **no release, tag, publication**, repository rename, package upload, or automatic migration for downstream users.

The current local identity is **Cited Vault Recall** with distribution, import, and primary executable names `cited-vault-recall`, `cited_vault_recall`, and `cited-vault-recall`. The paired local stdio MCP executable is `cited-vault-recall-mcp` under the migration manifest decision. Registry availability is deliberately unknown until the immediate, separately approved pre-publication registry check.

The former `agent-recall` / `agent_recall` identity is legacy pre-migration history. It must not be published: ADR-0002 records that its PyPI distribution name is occupied. There is no compatibility alias or shim for legacy console scripts or imports.

## Current supported contracts

The currently tested local commands are:

```text
cited-vault-recall <vault> <query> [--format markdown|json]
cited-vault-recall doctor --vault <vault> --json
cited-vault-recall reindex --vault <vault> --destination <outside-vault-index> --json
cited-vault-recall-mcp --vault <vault>
```

Consumers must use these canonical commands and the `cited_vault_recall` import package rather than relying on historical names.

The public Python API is the package `__all__`:

```text
SearchHit
render_packet
search_vault
```

The transport-neutral search response and citation schemas remain protocol v1. A breaking schema change requires a **new protocol directory/version**; v1 semantics must not silently change. The development package version, protocol version, schema version, and derived-index version are intentionally independent.

## Deprecation and migration rules

No legacy compatibility alias, shim, repository rename, registry redirect, or deprecation deadline is provided. Adding any of them requires an explicit compatibility decision, a bounded rollback/recovery plan, and tests that prove the claimed behavior. No legacy name is silently mapped to a different package, host integration, vault, or network service.

Before any future publication, the operator must re-check the target registry, follow the release-evidence policy, and obtain the separate release approval. The local rename neither reserves the new distribution name nor certifies package-registry availability.

## Non-goals

This policy does not certify host integration, Windows CI support, package-registry availability, backward compatibility for legacy names, or a future release date. It does not widen local-only, offline, read-only, explicit-vault, or relative-path boundaries.
