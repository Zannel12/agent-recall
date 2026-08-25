# Migration and deprecation policy

## Current status

Agent Recall is at `0.2.0.dev0`, an unreleased development scope. This policy is documentation and a public-contract guard only: it performs **no release, tag, publication**, repository rename, package upload, or automatic migration.

The identity migration accepted by [ADR-0002](adr/0002-product-namespace-and-naming.md) is **not implemented**. The proposed durable identity is **Cited Vault Recall** with the future distribution, import, and executable names `cited-vault-recall`, `cited_vault_recall`, and `cited-vault-recall`. Those names are a future migration target, not present installation instructions and not evidence of registry availability.

Until a separately scoped migration is completed, `agent-recall` / `agent_recall` are the current local pre-packaging identity. Because ADR-0002 documents an existing PyPI name collision, `agent-recall` **must not be published** to a package registry.

## Current supported contracts

The currently tested local commands are:

```text
agent-recall <vault> <query> [--format markdown|json]
agent-recall doctor --vault <vault> --json
agent-recall reindex --vault <vault> --destination <outside-vault-index> --json
agent-recall-mcp --vault <vault>
```

There is no compatibility alias for the removed `agent-recall search` subcommand. Consumers must use the canonical positional command rather than relying on undocumented fallbacks.

The public Python API is the package `__all__`:

```text
SearchHit
render_packet
search_vault
```

The transport-neutral search response and citation schemas remain protocol v1. A breaking schema change requires a **new protocol directory/version**; v1 semantics must not silently change. The development package version, protocol version, schema version, and derived-index version are intentionally independent.

## Deprecation and migration rules

A future migration must be a separate reviewed change set that updates package metadata, source/import layout, tests, public documentation, and installation commands together. Before any publication it must re-check the target registry name, follow the release-evidence policy, and obtain the required release approval.

Compatibility aliases, shims, a repository rename, registry redirects, or a promised deprecation deadline are deliberately not defined here. Adding any of them requires an explicit compatibility decision, a bounded rollback/recovery plan, and tests that prove the claimed behavior. No legacy name is silently mapped to a different package, host integration, vault, or network service.

## Non-goals

This policy does not certify host integration, Windows CI support, package-registry availability, backward compatibility beyond the documented current contracts, or a future release date. It does not widen local-only, offline, read-only, explicit-vault, or relative-path boundaries.
