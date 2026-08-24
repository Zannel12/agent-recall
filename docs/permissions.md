# Namespace capability gate

`agent_recall.permissions` is a **closed, category-only capability gate**. It is not an identity, authentication, ownership, tenancy, resource, path-safety, or complete authorization system.

## Closed inputs

- Scopes: `user`, `agent`, `project`, `task`
- Actions: `read`, `write`
- Callers must provide the exported enum values. Strings, aliases, whitespace variants, unknown values, and wrong types are denied.

## Current matrix

All known scopes may request `read`; every `write` request is denied. No scope inherits another scope's permissions.

The gate performs no I/O and is not connected to MCP, vaults, filesystem paths, persistence, credentials, or identity. A separate reviewed design is required before granting any write capability or treating this gate as resource-level authorization.
