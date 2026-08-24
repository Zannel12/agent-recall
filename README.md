# Agent Recall

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

`v0.1.0` public release. See [CHANGELOG.md](CHANGELOG.md) for the released scope and explicit exclusions. No real vault or personal data belongs in this repository.
