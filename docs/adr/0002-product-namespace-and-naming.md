# ADR-0002: Adopt Cited Vault Recall as the durable product identity

- **Status:** accepted
- **Date:** 2026-08-24
- **Decision point:** B04.1

## Context

The existing local metadata uses `agent-recall` as the distribution and executable, and `agent_recall` as the import package. Direct first-party registry checks show that this identity is already occupied and ambiguous:

- PyPI `agent-recall` returned HTTP `200`, version `0.4.0`, described as a different persistent-memory/MCP product.
- GitHub exact-name search returned multiple unrelated `agent-recall` repositories, including several agent-memory products.

Publishing this project under the existing distribution name would collide with an existing PyPI project and make installation/provenance claims misleading.

## Decision

Adopt the following immutable identity for the next public packaging work:

| Surface | Chosen name |
|---|---|
| Product | **Cited Vault Recall** |
| PyPI distribution | `cited-vault-recall` |
| Python import package | `cited_vault_recall` |
| CLI executable | `cited-vault-recall` |

## Evidence at decision time

Direct registry checks on 2026-08-24:

| Candidate | PyPI | GitHub exact-name search | Local executable |
|---|---:|---:|---|
| `agent-recall` | occupied (`0.4.0`) | multiple unrelated repositories | current legacy name |
| `cited-vault-recall` | HTTP `404` | 0 results | absent |
| `vault-recall` | HTTP `404` | 18 results | absent |

A 404/zero-result check is point-in-time evidence, not a reservation. B04.2 must re-check PyPI immediately before any publish.

## Consequences

- `agent-recall` / `agent_recall` remain a **legacy local pre-packaging identity** only until B04.2 performs the deliberate package/import/CLI migration.
- B04.2 must update `pyproject.toml`, `src/`, tests, documentation, and installation commands together; it must not publish under the legacy PyPI name.
- Existing GitHub repository `Zannel12/agent-recall` is not renamed in this ADR. A repository rename/migration requires its own scoped decision after B04.2 has established the new package URLs and compatibility messaging.
- No PyPI package is published by this decision.
