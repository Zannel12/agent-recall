# ADR-0004: Keep Agent Recall separate from Hermes memory-provider ownership

- **Status:** accepted
- **Date:** 2026-08-25
- **Decision scope:** ownership and conflict boundaries only; no provider implementation or configuration change

## Context

Hermes has bounded built-in `MEMORY.md` and `USER.md` stores, and may run one additive external memory provider alongside them. Provider documentation describes provider-context injection, turn synchronization, and built-in-write mirroring as Hermes/provider behavior. Agent Recall, by contrast, is an explicit-vault, local-only, read-only retrieval tool with a disposable derived index and no native Hermes provider.

Combining these roles without explicit authority rules risks duplicated personal facts, stale copies, or invisible cross-store writes.

Sources:

- [Hermes memory providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers)
- [Hermes persistent memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [Agent Recall layered authority ADR](0003-layered-architecture-boundaries.md)

## Decision

### Agent Recall boundary

**Agent Recall is not a Hermes memory provider.** It does not register as one, select one, configure one, install one, or change Hermes memory settings.

For an Agent Recall operation, the **selected Markdown vault remains authoritative** for source-linked retrieval only. A derived index and an in-memory cache are non-authoritative and rebuildable. Agent Recall does not claim authority over data outside the explicitly selected vault.

### Hermes built-in boundary

**Built-in Hermes memory remains a compact profile and routing layer.** It is not an Agent Recall source, import destination, mirror target, or replacement for the selected Markdown vault. Agent Recall never reads, writes, cleans, or reconciles Hermes built-in memory as part of retrieval.

### External-provider boundary

**External provider is non-authoritative for Agent Recall.** If a user later activates a Hermes external provider, it remains a separate Hermes-managed adjunct. Hermes/provider behavior such as injected context or provider synchronization does not make it a source for Agent Recall results, and Agent Recall does not consume provider records as vault content.

## Conflict behavior

For Agent Recall: do not synchronize these stores; do not merge their data. Apparent contradictions are represented as distinct, cited sources; no store wins automatically.

Resolving a conflict requires an **explicit user approval** for a scoped write through the owning system. Agent Recall may report the conflict and its citations, but it must not write, delete, overwrite, promote, invalidate, or mirror any store.

## Consequences

- **No Hermes configuration is changed by this ADR.** It does **not configure a provider**, disable built-in memory, or alter provider settings.
- Existing local CLI and stdio MCP boundaries remain unchanged.
- Native-provider work remains prohibited until a separate ADR and verification package defines explicit consent, data flow, provider-specific storage/security review, synthetic integration tests, rollback, and a migration/reversal plan.
- Users who enable a provider must understand its documented provider-specific data flow before doing so; this ADR neither approves nor automates that action.
