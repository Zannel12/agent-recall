# Hermes MCP adapter plan generator

`agent_recall.hermes_adapter.build_hermes_mcp_plan(...)` creates a reviewable **non-executing** plan for the selected Hermes local-stdio MCP path. It does not inspect a machine, read or write `~/.hermes/config.yaml`, copy files, spawn a subprocess, connect to MCP, reload Hermes, or start Agent Recall.

## Required caller inputs

The caller supplies all observations and paths:

- target config path and a distinct backup path;
- selected vault path;
- whether the target config was observed to exist;
- observed MCP server names;
- explicit `consent=True`.

The generator deliberately does not discover these values itself. This keeps host scope explicit and makes synthetic testing possible.

## Plan outcomes

| Status | Commands emitted | Meaning |
|---|---:|---|
| `consent_required` | No | The plan is preview-only until the caller explicitly consents. |
| `config_missing` | No | An observed target config is absent; a human must resolve the target before any backup/apply plan. |
| `invalid_backup` | No | Backup and target are the same path. |
| `name_collision` | No | `agent-recall` already exists in the caller-supplied server-name set. No replacement is proposed. |
| `ready` | Yes, as data only | Future user-controlled sequence: backup, add, interactive configure, removal/rollback. |

A ready plan includes a config-entry payload for review:

```yaml
command: agent-recall-mcp
args: [--vault, <caller-selected-vault>]
tools:
  include: [search]
sampling:
  enabled: false
```

The local protocol has one `search` tool. Its identifier-scoped `resources/read` operation remains bounded in the Agent Recall protocol; it is not an arbitrary filesystem tool. Hermes tool filtering applies to `search`.

The `commands` field is a tuple of argument vectors, not shell text. It contains no secret values and is never executed by this module. The future apply workflow must review the payload, create the backup, use the Hermes interactive configuration step to verify the narrow exposure, verify the connection under a separately approved synthetic-host procedure, and use the included `hermes mcp remove agent-recall` vector for rollback if needed.

## Fallback

Every outcome exposes the deterministic non-host fallback:

```text
agent-recall <caller-selected-vault> <query> --format json
```

The CLI and MCP search schema share the core result bound: `1`–`50` hits.

No config is automatically applied, and this plan does not demonstrate that Hermes has loaded or can run Agent Recall.

## Evidence levels

### Synthetic MCP protocol E2E (required)

`tests/test_mcp_protocol_e2e.py` is a required repository test. It creates a temporary synthetic Markdown vault, starts the local stdio server directly, and verifies the JSON-RPC `tools/list`, bounded `tools/call` search, and identifier-scoped `resources/read` flow. This demonstrates the Agent Recall protocol only; it does not start, inspect, configure, authenticate, or connect a Hermes host.

### Real Hermes verification (manual opt-in)

Real Hermes verification is not a repository test and is never triggered by CI. It may occur only under a separately approved, owner-controlled procedure using a synthetic vault and a reviewed non-executing plan. The procedure must not infer success from host documentation or apply configuration automatically. No real Hermes host was configured or connected while producing this evidence.
