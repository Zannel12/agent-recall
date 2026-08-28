# Package migration manifest

This is the design-verification inventory for the future ADR-0002 identity migration. It is not the migration itself and does not change a package name, import, executable, repository, registry record, or protocol identifier.

## Current identity

| Surface | Current value | Authority |
|---|---|---|
| Distribution | `agent-recall` | `pyproject.toml` |
| Python import package | `agent_recall` | `src/agent_recall/` |
| Search/doctor/reindex executable | `agent-recall` | `pyproject.toml` `[project.scripts]` |
| MCP executable | `agent-recall-mcp` | `pyproject.toml` `[project.scripts]` |
| GitHub repository | `Zannel12/agent-recall` | current public repository URL |
| Protocol schema IDs | `https://github.com/Zannel12/agent-recall/protocol/v1/...` | `protocol/v1/*.schema.json` |

The `agent-recall` distribution-name collision is an external publication blocker, not an excuse to silently rename or publish this local alpha.

## Future target

ADR-0002 accepted these future package surfaces:

| Surface | Future value |
|---|---|
| Product | Cited Vault Recall |
| Distribution | `cited-vault-recall` |
| Python import package | `cited_vault_recall` |
| Primary executable | `cited-vault-recall` |

The migration must also deliberately rename the MCP executable. The proposed paired name is `cited-vault-recall-mcp`; A3 must either use that paired name or amend this manifest and add a tested compatibility decision before implementation. The GitHub repository and protocol-v1 schema IDs are explicitly outside this package migration unless a separate reviewed decision changes them.

## Migration inventory

A3 must update every row as one reviewed local change set. The inventory is based on the direct source scan performed on 2026-08-28.

| Surface group | Current references found | A3 requirement |
|---|---|---|
| Packaging and entry points | `pyproject.toml`: distribution, URLs, `agent-recall`, `agent-recall-mcp`, and `agent_recall.*` entry points | Replace distribution/import/console entry points together; preserve only the approved public URLs. |
| Source package and runtime literals | `src/agent_recall/`, including `hermes_adapter.py` command/server literals | Rename package directory/imports and all emitted plan literals; retain configuration-plan-only behavior. |
| Tests and installation probes | `tests/`, including module imports, editable/clean-install/wheel tests, console-script paths, and temporary clone names | Update import paths and expected binaries; prove old binaries are absent unless a separately approved alias exists. |
| Human-facing command documentation | `README.md`, `INSTALL.md`, `AGENTS.md`, `CHANGELOG.md`, `examples/`, and `docs/` | Update commands and installation instructions in the same commit; state migration boundary honestly. |
| CI | `.github/workflows/tests.yml` | Replace executable smoke command and keep the existing test matrix. |
| Protocol identity | `protocol/v1/*.schema.json` schema IDs point to the current GitHub repository | Do not change in A3; protocol v1 is transport-neutral and repository rename is out of scope. |
| Repository and GitHub links | `pyproject.toml`, README badge/links, policy/security links | Do not rename the repository in A3; retain/review links rather than assuming a future repository URL. |

## A3 acceptance contract

Before A3 can close, an isolated local build must prove all of the following:

```text
1. distribution metadata is cited-vault-recall;
2. import is cited_vault_recall;
3. primary executable is cited-vault-recall;
4. MCP executable follows the reviewed paired-name decision;
5. wheel and sdist include cited_vault_recall and omit agent_recall;
6. clean-install CLI, doctor, and local stdio MCP synthetic tests pass;
7. no compatibility alias exists unless separately decided, documented, and tested;
8. no GitHub repository rename, Git tag, GitHub Release, or package publication occurred.
```

## Deliberate non-actions

This A2 manifest performs **no registry lookup**, no package publication, no GitHub repository rename, no Git tag or GitHub Release, no SBOM, no provenance attestation, no workflow SHA pinning, no model/dependency acquisition, no deployment, and no real-host integration. It makes no registry-availability claim about `cited-vault-recall`.

No real vault, host configuration, or credential is read, written, requested, or stored by this design verification.
