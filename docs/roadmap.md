# Public roadmap

This is a short, evidence-based roadmap for Cited Vault Recall. It lists only current public priorities; it is not a promise of dates, a release authorization, or a hosted-service plan.

## Current state

- GitHub Release [`v0.2.0`](https://github.com/Zannel12/agent-recall/releases/tag/v0.2.0) is published.
- PyPI publication remains pending. A non-secret Trusted Publisher and a reviewed manual-only OIDC workflow now exist, but the workflow has not been dispatched and no package was uploaded.
- The product remains local-first, read-only, explicit-vault, and offline by default.
- No hosted deployment is selected. Public package distribution is not a hosted production service.

## Execution state

**Autonomous OSS foundation (Tasks 1–15) is complete.** It delivered public release/evidence truthfulness, maintainer and contributor surfaces, synthetic evaluation/performance boundaries, one path-safe setup remediation, dependency and CI guardrails, a privacy-safe backlog, a read-only repository hygiene audit, and a manual-only publication workflow that has never been dispatched.

The next single dependency-gated action is **Task 16**: publish the exact `v0.2.0` wheel and sdist to PyPI. This is externally irreversible and requires **fresh scoped approval** after a fresh release/hash/attestation/PyPI-state preflight. No credential, token, browser session, or one-time code is requested in the repository or chat.

Actual and planned owner participation is **5 / 18 = 27.8%**, below the 33% cap: the Task 11 backlog-revision authorization, Task 14 account-side configuration, a fresh Task 16 publication approval, and the two deliberately late owner steps (Tasks 17 and 18).

## Owner-blocked decisions

- **PyPI publication:** Task 16 is ready for a fresh preflight and fresh scoped approval. The Trusted Publisher and manual-only OIDC workflow exist, but no workflow dispatch or package upload has occurred.
- **Hosted-product boundary:** No hosted deployment is selected. Package distribution is not a service deployment; a later owner decision must either retain this boundary or define a separate target and operating model.

## Deferred and non-goals

- Semantic/vector/LLM retrieval is `DEFER` until its documented privacy-safe benchmark, provenance, offline-cache, resource, and citation-equivalence gates are met.
- Cloud sync, telemetry, automatic vault discovery/writes, and mandatory model downloads are not current roadmap work.
- A hosted API, Docker service, or other deployment requires a separate target, operator, rollback, privacy, observability, retention, and support decision before implementation.

## How to contribute

See [project scope](project-scope.md), [decisions](decisions.md), and the repository issue templates. Use synthetic fixtures and bounded acceptance evidence.
