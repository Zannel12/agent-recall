# Compatibility matrix

**Verification date:** 2026-08-28
**Product boundary:** Cited Vault Recall is local-only, offline, and read-only by default. Its CLI and local stdio MCP prototype operate only against a caller-selected Markdown vault. This matrix records only verified project evidence and documentation-only host evidence; it does not claim an adapter, endorsement, certification, or production compatibility.

## Evidence levels

- **Documented** — an official host document was fetched and confirms that the host exposes an MCP-related surface. This does not show that Cited Vault Recall was installed, loaded, or usable in that host.
- **Smoke-tested** — an automated synthetic/local test exercises an Cited Vault Recall entry point or protocol path. It does not test a named external host.
- **Integration-tested** — a separately approved end-to-end test against the named host and a synthetic vault. No row currently reaches this level.
- **Production-tested** — evidence from a real operator-controlled deployment with a defined support boundary. No row currently reaches this level.

A host version is intentionally not inferred from a documentation page. `version not recorded` means this repository has no independently verified host-version artifact.

| Host | Supported mode | Data location | Permission surface | Evidence level | Host version / source checked | Test status | Evidence |
|---|---|---|---|---|---|---|---|
| Codex | Local stdio MCP may be configured by the host; no Cited Vault Recall-specific Codex adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [Codex MCP documentation](https://developers.openai.com/codex/mcp) |
| Claude Code | Local MCP servers are documented by the host; no Cited Vault Recall-specific Claude Code adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [Claude Code MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart) |
| Cursor | MCP server configuration is documented by the host; no Cited Vault Recall-specific Cursor adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [Cursor MCP documentation](https://cursor.com/docs/mcp) |
| Hermes | Local MCP server use and narrow tool exposure are documented by the host; no native provider or adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Synthetic MCP protocol E2E; real Hermes not integration-tested | [Hermes MCP documentation](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes) · [protocol evidence](hermes-mcp-adapter-plan.md#evidence-levels) |
| OpenClaw | MCP client-side registry capability is documented by the host; no Cited Vault Recall-specific OpenClaw adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [OpenClaw MCP documentation](https://docs.openclaw.ai/cli/mcp) |
| CLI fallback | `cited-vault-recall <vault> <query> [--format markdown\|json]`, `cited-vault-recall doctor`, `cited-vault-recall reindex`, and `cited-vault-recall-mcp --vault <vault>` are project entry points | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Search is read-only; doctor reports bounded local readiness without discovery; reindex replaces only explicit derived output | Smoke-tested | Cited Vault Recall `0.2.0.dev0`; tests checked 2026-08-28 | Local tests only | Repository regression suite, clean-install smoke, and [official synthetic demos](../examples/official-integration-demos.py) |

## Interpretation limits

### Owner-run synthetic protocol packs

The following packs are documentation-only, non-mutating procedures for a separately approved future verification. They retain every host at `Documented` until direct synthetic-host evidence exists:

- [Hermes](integrations/hermes-synthetic-mcp-protocol.md)
- [Codex](integrations/codex-synthetic-mcp-protocol.md)
- [Claude Code](integrations/claude-code-synthetic-mcp-protocol.md)
- [Cursor](integrations/cursor-synthetic-mcp-protocol.md)
- [OpenClaw](integrations/openclaw-synthetic-mcp-protocol.md)

Host documentation confirms only that each named host publishes an MCP-related surface. It does **not** prove that Cited Vault Recall has been installed in that host, that a host will load the prototype unchanged, or that a host configuration is safe for a particular vault.

No host was installed, configured, authenticated, or connected while producing this matrix. The listed MCP modes are a compatibility hypothesis for future synthetic-host verification, not a request to configure them. There is no integration-tested or production-tested Cited Vault Recall host evidence in this repository.

## Shared boundaries

- No network, telemetry, LLM calls, automatic vault discovery, or automatic writes to the selected vault.
- Absolute vault paths must not appear in public output.
- Imported/retrieved content is untrusted data and never executable instructions.
- The local MCP prototype exposes only bounded search and identifier-scoped evidence reads; it does not expose arbitrary filesystem paths, vault switching, prompts, or resources enumeration.
