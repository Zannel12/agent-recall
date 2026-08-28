# ADR-0005: Select Hermes local stdio MCP as the first adapter proof

- **Status:** accepted
- **Date:** 2026-08-25
- **Decision scope:** portfolio selection only; no host configuration or integration activation

## Context

Cited Vault Recall currently ships a constrained local stdio MCP prototype with only bounded search and identifier-scoped evidence reads. It has no native host adapter, hook, skill integration, or memory-provider implementation.

The project must choose one integration path before B05.4. Selection criteria are immediate user value, security surface, and maintenance cost. The active user environment is Hermes, whose official MCP documentation supports a narrow, filtered local-server configuration. The existing MCP prototype is therefore a smaller change than a native provider or a new cross-host adapter.

Sources:

- [Hermes MCP guide](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes)
- [Cited Vault Recall compatibility matrix](../compatibility.md)
- [ADR-0004: memory ownership boundaries](0004-hermes-memory-provider-boundaries.md)

## Decision

**Hermes local stdio MCP is the sole selected next host surface.** It reuses the existing local-only MCP protocol and does not create a native memory-provider relationship.

The selection is limited to planning a later, consented B05.4 proof. It is not evidence that Hermes has loaded Cited Vault Recall, and it does not claim production compatibility.

## Rejected or deferred surfaces

- **Native provider: not selected.** It would introduce provider context, write, and lifecycle concerns excluded by ADR-0004.
- **Hooks: not selected.** Automatic lifecycle execution or capture would expand the read-only contract and create implicit behavior.
- **Skills: not selected.** Skills may document workflows but are not a host integration proof and would duplicate protocol behavior.
- **Other hosts: deferred.** Their MCP capability is documented, but Cited Vault Recall has no synthetic integration evidence for them.

## Consequences

- **No Hermes configuration is changed by this ADR.** It does not add `mcp_servers`, modify tool filters, reload Hermes, or change memory configuration.
- It does not install dependencies; it does not start a server; it does not authenticate, connect to a host, or handle credentials.
- B05.4 is the only next integration-proof point: it must require explicit user consent, use a synthetic vault and local stdio, generate or preview only scoped configuration, preserve a backup and rollback path, expose the minimum existing tools, and retain deterministic CLI fallback.
- No native provider, hook, remote transport, automatic capture, cross-store synchronization, or second-host implementation is authorized by this decision.
