# Changelog

All notable changes to Cited Vault Recall are documented here.

## [0.2.0] — Release candidate, untagged

This release candidate is represented by package version `0.2.0`. It is **not** a GitHub Release or tag and has not been published to a package registry.

### Added

- Local stdio MCP entry point: `cited-vault-recall-mcp --vault <vault>`, with a bounded `search` tool and identifier-scoped evidence reads.
- Explicit CLI operations for `doctor` and `reindex`, plus a canonical positional search contract: `cited-vault-recall <vault> <query>`.
- A bounded synthetic-vault Hermes local stdio MCP integration, verified with only `search` exposed, a relative citation, and teardown of temporary state.
- Derived-index integrity checks, explicit lifecycle/permission boundaries, aggregate diagnostics, and synthetic retrieval evaluation fixtures.
- Installation, built-distribution, MCP-entry-point, public-command-contract, Python 3.10 compatibility, and clean end-to-end smoke tests.
- Public contribution surface: code of conduct, issue/PR templates, contributor privacy guidance, and local tool-state ignore rules.
- GitHub Actions coverage for Python 3.10–3.13 and a separate clean-install smoke job.

### Changed

- MCP, CLI, core, and public documentation share a `1`–`50` result-limit contract.
- The package metadata now declares the untagged, unpublished release-candidate version `0.2.0`.

### Still not a release

- No GitHub Release, tag, or registry publication has been created. The historical C6a SBOM and C6b provenance attestation apply only to earlier `0.2.0.dev0` artifacts, not this candidate's future exact artifacts.
- Hermes has bounded synthetic-vault `Integration-tested` evidence only; Codex, Claude Code, Cursor, and OpenClaw remain documentation-only, and no host is Production-tested.

## [0.1.0] — 2026-08-21

### Added

- Local, read-only search across a user-selected Markdown vault.
- Transparent lexical ranking using query matches in titles, paths, and bodies.
- Source-linked Markdown context packets and JSON output.
- Installable CLI: `agent-recall <vault> <query> [--format markdown|json]`.
- Synthetic demo vault, deterministic tests, and an AI-agent integration brief.
- Agent-facing documentation: architecture, security, provenance, upstreams, contributing, and future memory-transfer boundaries.

### Security and privacy boundary

- No network access, telemetry, API keys, LLM calls, agent-runtime dependency, or automatic vault writes.
- Output exposes relative source paths rather than machine paths.
- The real personal vault, Hermes memory, financial/health data, chats, credentials, and configuration are out of scope and must not enter this repository.

### Not included

- Memory-transfer import/export implementation; planned for a later version.
- Adapters for Hermes, OpenClaw, or other agent ecosystems.
- Semantic/LLM retrieval, vector databases, cloud sync, or auto-curation.
