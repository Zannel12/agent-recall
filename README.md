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
# Optional, deterministic Russian morphology/synonym expansion:
agent-recall examples/demo-vault "локальную память" --format json --russian-lexical-expansion
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

`doctor --json` reports a bounded `READY`/`NOT_READY` status plus stable codes for the local executable, explicit vault readability, ignore policy, and a local search probe. It reports only aggregate counts, does not search parent directories, home directories, or agent state, and never exposes an absolute vault path.

## What it does / does not do

| Does | Does not |
|---|---|
| Search local `.md` files and cite relative paths | Upload vault contents or call an LLM |
| Return ranked excerpts | Write, delete, or reorganize your vault |
| Work without API keys | Access Hermes, OpenClaw, or any agent runtime |

## Agent integration

Read **[AGENTS.md](AGENTS.md)** before integrating. The contract is one input (vault + query) and one output (source-linked context packet). For an isolated local install for an autonomous agent, follow the **[standalone installation guide](docs/autonomous-agent-installation.md)**. For a copyable handoff to another coding/AI agent, use **[examples/agent-brief.md](examples/agent-brief.md)**. Run the synthetic expected-result [official integration demos](examples/official-integration-demos.py) for CLI, local MCP, and a **configuration-plan-only** Hermes example; it never configures or connects a Hermes host.

## Trust and provenance

- Architecture and trust boundaries: [ARCHITECTURE.md](ARCHITECTURE.md)
- Original vs adapted work: [ADAPTATIONS.md](ADAPTATIONS.md)
- Upstreams and licenses: [UPSTREAMS.md](UPSTREAMS.md)
- Security and privacy: [SECURITY.md](SECURITY.md)
- Offline dependency/action declaration inventory: [supply-chain inventory](docs/supply-chain-inventory.md)
- Public naming, migration, and deprecation boundary: [migration-and-deprecation](docs/migration-and-deprecation.md)
- Planned memory transfer protocol: [MEMORY-TRANSFER.md](MEMORY-TRANSFER.md)
- Dense retrieval decision: [ADR-0001](docs/adr/0001-defer-optional-dense-retrieval.md)

## Status

`0.2.0.dev0` is the current development package version for the unreleased `0.2.0` scope. No GitHub Release or tag exists for it. See [CHANGELOG.md](CHANGELOG.md) for scope and explicit exclusions. No real vault or personal data belongs in this repository.

## Evidence and current limits

- **Local CLI:** covered by the public Python 3.10–3.13 test workflow, including an installed-package demo and a separate clean-install smoke job.
- **Retrieval evaluation:** versioned synthetic retrieval, exact-date, and abstention scenarios are documented in [benchmarks/evaluation](benchmarks/evaluation/README.md).
- **Host support:** the public compatibility matrix distinguishes local tests from hosts that are **not integration-tested**: [compatibility](docs/compatibility.md).
- **Hermes MCP:** only a non-mutating, caller-supplied configuration-plan contract exists; no Hermes host is configured or connected: [adapter plan](docs/hermes-mcp-adapter-plan.md).
- **Release evidence:** GitHub-only release requirements are documented in [release provenance](docs/release-provenance.md). No GitHub Release, package registry publication, SBOM, or provenance attestation has been created yet.
