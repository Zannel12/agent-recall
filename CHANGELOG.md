# Changelog

All notable changes to Agent Recall are documented here.

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
