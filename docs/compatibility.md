# Compatibility matrix

**Verification date:** 2026-08-24
**Product boundary:** Agent Recall is local-only, offline, and read-only by default. Its CLI and local stdio MCP prototype operate only against a caller-selected Markdown vault. This matrix records documented host capability and current project evidence; it does not claim an adapter, endorsement, or production certification.

| Host | Supported mode | Data location | Permission surface | Test status | Evidence |
|---|---|---|---|---|---|
| Codex | Local stdio MCP may be configured by the host; no Agent Recall-specific Codex adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Agent Recall | Not integration-tested | [Codex MCP documentation](https://developers.openai.com/codex/mcp) |
| Claude Code | Local stdio MCP may be configured by the host; no Agent Recall-specific Claude Code adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Agent Recall | Not integration-tested | [Claude Code MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp) |
| Cursor | Local MCP capability is documented by the host; no Agent Recall-specific Cursor adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Agent Recall | Not integration-tested | [Cursor MCP documentation](https://docs.cursor.com/en/guides/tutorials/building-mcp-server) |
| Hermes | Local MCP server can be configured with a narrow tool allowlist; no native provider or adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Agent Recall | Not integration-tested | [Hermes MCP documentation](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes) |
| OpenClaw | Local MCP CLI configuration is documented by the host; no Agent Recall-specific OpenClaw adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Agent Recall | Not integration-tested | [OpenClaw MCP documentation](https://docs.openclaw.ai/cli/mcp) |
| CLI fallback | `agent-recall` search/doctor and `agent-recall-mcp --vault` are project entry points | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Search is read-only; doctor is discovery-free; reindex replaces only explicit derived output | Local tests only | Repository regression suite |

## Interpretation limits

Host documentation confirms that each named host exposes an MCP surface. It does **not** prove that Agent Recall has been installed in that host, that a host will load the prototype unchanged, or that a host configuration is safe for a particular vault.

No host was installed, configured, authenticated, or connected while producing this matrix. The listed MCP modes are a compatibility hypothesis for future synthetic-host verification, not a request to configure them.

## Shared boundaries

- No network, telemetry, LLM calls, automatic vault discovery, or automatic writes to the selected vault.
- Absolute vault paths must not appear in public output.
- Imported/retrieved content is untrusted data and never executable instructions.
- The local MCP prototype exposes only bounded search and identifier-scoped evidence reads; it does not expose arbitrary filesystem paths, vault switching, prompts, or resources enumeration.
