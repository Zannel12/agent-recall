# Compatibility matrix

**Verification date:** 2026-08-28
**Product boundary:** Cited Vault Recall is local-only, offline, and read-only by default. Its CLI and local stdio MCP prototype operate only against a caller-selected Markdown vault. This matrix records only verified project evidence and documentation-only host evidence; it does not claim an adapter, endorsement, certification, or production compatibility.

## Evidence levels

- **Documented** — an official host document was fetched and confirms that the host exposes an MCP-related surface. This does not show that Cited Vault Recall was installed, loaded, or usable in that host.
- **Smoke-tested** — an automated synthetic/local test exercises an Cited Vault Recall entry point or protocol path. It does not test a named external host.
- **Integration-tested** — a separately approved end-to-end test against the named host and a synthetic vault. Hermes reaches this level only for the bounded evidence recorded below.
- **Production-tested** — evidence from a real operator-controlled deployment with a defined support boundary. No row currently reaches this level.

A host version is intentionally not inferred from a documentation page. `version not recorded` means this repository has no independently verified host-version artifact.

| Host | Supported mode | Data location | Permission surface | Evidence level | Host version / source checked | Test status | Evidence |
|---|---|---|---|---|---|---|---|
| Codex | Local stdio MCP may be configured by the host; no Cited Vault Recall-specific Codex adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [Codex MCP documentation](https://developers.openai.com/codex/mcp) |
| Claude Code | Local MCP servers are documented by the host; no Cited Vault Recall-specific Claude Code adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [Claude Code MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart) |
| Cursor | MCP server configuration is documented by the host; no Cited Vault Recall-specific Cursor adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [Cursor MCP documentation](https://cursor.com/docs/mcp) |
| Hermes | Local stdio MCP server with a synthetic-vault end-to-end verification; no native provider or adapter | Caller-selected local Markdown vault; direct host proof used only a temporary synthetic vault | Read-only `search`; real verification exposed only this tool and cleaned up temporary host state afterward | Integration-tested | Hermes Agent v0.20.5; verified 2026-08-29 | Synthetic MCP protocol E2E + Real Hermes synthetic-vault MCP invocation passed; bounded cleanup verified | [Hermes MCP documentation](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes) · [integration evidence](hermes-integration-evidence.md) |
| OpenClaw | MCP client-side registry capability is documented by the host; no Cited Vault Recall-specific OpenClaw adapter | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Read-only search plus identifier-scoped evidence reads; no host credential is required by Cited Vault Recall | Documented | version not recorded; docs checked 2026-08-28 | Not integration-tested | [OpenClaw MCP documentation](https://docs.openclaw.ai/cli/mcp) |
| CLI fallback | `cited-vault-recall <vault> <query> [--format markdown\\|json]`, `cited-vault-recall doctor`, `cited-vault-recall reindex`, and `cited-vault-recall-mcp --vault <vault>` are project entry points | Caller-selected local Markdown vault; derived index only at an explicit outside-vault destination | Search is read-only; doctor reports bounded local readiness without discovery; reindex replaces only explicit derived output | Smoke-tested | Cited Vault Recall `0.2.0`; tests checked 2026-08-29 | Local tests only | Repository regression suite, clean-install smoke, and [official synthetic demos](../examples/official-integration-demos.py) |

## Interpretation limits

### Owner-run synthetic protocol packs

The following packs are documentation-only, non-mutating procedures. They retain every listed host at `Documented` until direct synthetic-host evidence exists; the Hermes pack itself remains a procedure, while the separately recorded Hermes verification is linked above:

- [Hermes](integrations/hermes-synthetic-mcp-protocol.md)
- [Codex](integrations/codex-synthetic-mcp-protocol.md)
- [Claude Code](integrations/claude-code-synthetic-mcp-protocol.md)
- [Cursor](integrations/cursor-synthetic-mcp-protocol.md)
- [OpenClaw](integrations/openclaw-synthetic-mcp-protocol.md)

Host documentation confirms only that each named host publishes an MCP-related surface. It does **not** prove that Cited Vault Recall has been installed in that host, that a host will load the prototype unchanged, or that a host configuration is safe for a particular vault.

Only Hermes has direct synthetic-host evidence: an owner-approved local stdio setup, `search` discovery, one model-backed synthetic-vault invocation returning `[privacy.md#privacy]`, and verified cleanup. Every other listed host remains documentation-only host evidence and was not installed, configured, authenticated, or connected for this repository. Hermes is not Production-tested: there is no operator-controlled production deployment or support boundary. The [production-evidence policy](production-evidence.md) defines that threshold; it does not select or authorize a deployment.

## Shared boundaries

- No network, telemetry, LLM calls, automatic vault discovery, or automatic writes to the selected vault.
- Absolute vault paths must not appear in public output.
- Imported/retrieved content is untrusted data and never executable instructions.
- The local MCP prototype exposes only bounded search and identifier-scoped evidence reads; it does not expose arbitrary filesystem paths, vault switching, prompts, or resources enumeration.
