# Capability negotiation and visible fallback

Agent Recall keeps integration and retrieval decisions explicit. This module is a **pure policy contract**: it accepts caller-supplied availability and returns a deterministic selection. It does not probe a host, read configuration, install dependencies, connect to MCP, start a process, load a model, run a query, or mutate any state.

## Transport selection

The priority order is:

```text
native provider → MCP → CLI
```

`choose_transport_mode(...)` returns a `CapabilityChoice`.

- The first supplied available mode is selected.
- If a lower-priority mode is selected, `degraded` is `true` and `reason` lists every earlier unavailable mode in priority order.
- If no mode is supplied, the choice is unavailable with `selected=None` and `reason="no_transport_available"`. It does not silently use another transport.

The policy does not assert that a native provider or MCP is installed. In the current project state, no native provider is implemented; local CLI is the verified baseline and the local stdio MCP prototype is separately bounded.

## Retrieval selection

The priority order is:

```text
hybrid → sparse → deterministic lexical
```

`choose_retrieval_mode(...)` follows the same visible-fallback contract. It neither loads nor enables a retrieval implementation. Current product retrieval remains deterministic lexical/BM25-style. ADR-0001 keeps hybrid/dense retrieval deferred; callers must not mark it available without its separately approved prerequisites and evaluation evidence.

## Integration boundary

The policy is intentionally not wired into the CLI, MCP server, or a host adapter. Wiring one of those paths would be a separate implementation point requiring its own consent, integration evidence, and rollback boundary. A caller must surface the returned mode and fallback reason rather than hiding a degraded result from users.
