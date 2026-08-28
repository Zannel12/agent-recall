# Package migration manifest

This document is the verified implementation inventory for the ADR-0002 local identity migration. It records the exact surfaces changed from the legacy local alpha identity to the current unreleased identity. It is not registry evidence and does not create a package publication, repository rename, tag, release, or protocol version change.

## Current identity

| Surface | Current value | Authority |
|---|---|---|
| Product | Cited Vault Recall | public documentation |
| Distribution | `cited-vault-recall` | `pyproject.toml` |
| Python import package | `cited_vault_recall` | `src/cited_vault_recall/` |
| Search/doctor/reindex executable | `cited-vault-recall` | `pyproject.toml` `[project.scripts]` |
| MCP executable | `cited-vault-recall-mcp` | `pyproject.toml` `[project.scripts]` |
| GitHub repository | `Zannel12/agent-recall` | current public repository URL |
| Protocol schema IDs | `https://github.com/Zannel12/agent-recall/protocol/v1/...` | `protocol/v1/*.schema.json` |

Registry availability is deliberately unknown. The local non-colliding identity is not a reservation and must be checked immediately before any separately approved publication.

## Implemented target

ADR-0002 accepted the durable product, distribution, import, and primary executable identity:

```text
Cited Vault Recall
cited-vault-recall
cited_vault_recall
cited-vault-recall
```

The paired MCP executable `cited-vault-recall-mcp` was adopted as the reviewed A3 companion name. The GitHub repository and protocol-v1 schema IDs deliberately remain unchanged: repository rename and protocol-version changes are separate decisions.

## Migration inventory

| Surface group | Implemented result |
|---|---|
| Packaging and entry points | `pyproject.toml` now declares the new distribution, `cited_vault_recall.*` entry points, `cited-vault-recall`, and `cited-vault-recall-mcp`. |
| Source package and runtime literals | `src/cited_vault_recall/` replaces the legacy source directory; command literals used by the non-executing Hermes plan use the new executables. |
| Tests and installation probes | `tests/` imports and installed-script assertions target the new package/commands. The clean-source smoke tests copy the working source tree rather than cloning an old committed snapshot, so they prove the candidate change before commit. |
| Human-facing command documentation | `README.md`, `INSTALL.md`, `AGENTS.md`, `examples/`, and `docs/` use the current command/import names where they describe current behavior. Historical ADR/release material preserves the legacy identity as history. |
| CI | `.github/workflows/tests.yml` invokes the current CLI smoke command. |
| Protocol identity | `protocol/v1/*.schema.json` retains the existing repository schema IDs and v1 semantics. |
| Repository and GitHub links | Existing `Zannel12/agent-recall` URLs remain unchanged. |

## Legacy boundary

`agent-recall`, `agent_recall`, and `agent-recall-mcp` are no longer installed or supported local package/import/executable names. No compatibility alias exists. Historical mentions are retained only when they identify the former name, its PyPI collision, or an old source/release fact.

## Deliberate non-actions

This implementation performs **no registry lookup**, no package publication, no GitHub repository rename, no Git tag or GitHub Release, no SBOM, no provenance attestation, no workflow SHA pinning, no model/dependency acquisition, no deployment, and no real-host integration. It makes no registry-availability claim about `cited-vault-recall`.

No real vault, host configuration, or credential is read, written, requested, or stored by this local package migration.
