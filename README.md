# Agent Recall

[![Tests](https://github.com/Zannel12/agent-recall/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Zannel12/agent-recall/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Cited, scoped memory from a local Markdown vault for AI agents.**

Agent Recall searches a vault you select and returns ranked excerpts with relative source paths. It is read-only, local-first, offline by default, and does not send the whole vault to an agent.

## 60-second quickstart

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
agent-recall examples/demo-vault "privacy local memory"
```

JSON for an integration:

```bash
agent-recall examples/demo-vault "privacy" --format json
```

## Local configuration and doctor

Agent Recall never discovers a vault. Pass one explicitly or use a user-created JSON file:

```json
{"vault": "/absolute/path/to/your/vault"}
```

```bash
agent-recall doctor --config recall.json --json
# or: agent-recall doctor --vault /absolute/path/to/your/vault --json
```

`doctor --json` reports only install health, explicit vault accessibility, and whether discovery occurred (`false`). It does not search parent directories, home directories, or agent state.

## What it does / does not do

| Does | Does not |
|---|---|
| Search local `.md` files and cite relative paths | Upload vault contents or call an LLM |
| Return ranked excerpts | Write, delete, or reorganize your vault |
| Work without API keys | Access Hermes, OpenClaw, or any agent runtime |

## Agent integration

Read **[AGENTS.md](AGENTS.md)** before integrating. The contract is one input (vault + query) and one output (source-linked context packet). For a copyable handoff to another coding/AI agent, use **[examples/agent-brief.md](examples/agent-brief.md)**.

## Trust and provenance

- Architecture and trust boundaries: [ARCHITECTURE.md](ARCHITECTURE.md)
- Original vs adapted work: [ADAPTATIONS.md](ADAPTATIONS.md)
- Upstreams and licenses: [UPSTREAMS.md](UPSTREAMS.md)
- Security and privacy: [SECURITY.md](SECURITY.md)
- Planned memory transfer protocol: [MEMORY-TRANSFER.md](MEMORY-TRANSFER.md)
- Dense retrieval decision: [ADR-0001](docs/adr/0001-defer-optional-dense-retrieval.md)

## Status

`v0.1.0` is the current package version. See [CHANGELOG.md](CHANGELOG.md) for scope and explicit exclusions. No real vault or personal data belongs in this repository.

## Evidence and current limits

- **Local CLI:** covered by the public Python 3.11/3.12 test workflow, including an installed-package demo.
- **Retrieval evaluation:** versioned synthetic retrieval, exact-date, and abstention scenarios are documented in [benchmarks/evaluation](benchmarks/evaluation/README.md).
- **Host support:** the public compatibility matrix distinguishes local tests from hosts that are **not integration-tested**: [compatibility](docs/compatibility.md).
- **Hermes MCP:** only a non-mutating, caller-supplied configuration-plan contract exists; no Hermes host is configured or connected: [adapter plan](docs/hermes-mcp-adapter-plan.md).
- **Release evidence:** GitHub-only release requirements are documented in [release provenance](docs/release-provenance.md). No GitHub Release, package registry publication, SBOM, or provenance attestation has been created yet.
