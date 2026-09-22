# Public roadmap

This is a short, evidence-based roadmap for Cited Vault Recall. It lists only current public priorities; it is not a promise of dates, a release authorization, or a hosted-service plan.

## Current state

- GitHub Release [`v0.2.0`](https://github.com/Zannel12/agent-recall/releases/tag/v0.2.0) is published.
- PyPI publication remains pending until a non-secret owner-side PyPI Trusted Publishing route exists.
- The product remains local-first, read-only, explicit-vault, and offline by default.
- No hosted deployment is selected. Public package distribution is not a hosted production service.

## Execution state

**Autonomous OSS foundation (Tasks 1–13) is complete.** It delivered public release/evidence truthfulness, maintainer and contributor surfaces, synthetic evaluation/performance boundaries, one path-safe setup remediation, dependency and CI guardrails, a privacy-safe backlog, and a read-only repository hygiene audit.

The next single dependency-gated action is **Task 14**: owner-side PyPI Trusted Publishing configuration. PyPI publication remains pending; no credential, token, browser session, or one-time code is requested in the repository or chat.

Actual and planned owner participation is **4 / 18 = 22.2%**, below the 33% cap: one explicit Task 11 backlog-revision authorization plus the three deliberately late owner steps (Tasks 14, 17, and 18).

## Owner-blocked decisions

- **PyPI Trusted Publishing:** Task 14 requires owner-side configuration before a narrow publication workflow can be reviewed or used.
- **Hosted-product boundary:** No hosted deployment is selected. Package distribution is not a service deployment; a later owner decision must either retain this boundary or define a separate target and operating model.

## Deferred and non-goals

- Semantic/vector/LLM retrieval is `DEFER` until its documented privacy-safe benchmark, provenance, offline-cache, resource, and citation-equivalence gates are met.
- Cloud sync, telemetry, automatic vault discovery/writes, and mandatory model downloads are not current roadmap work.
- A hosted API, Docker service, or other deployment requires a separate target, operator, rollback, privacy, observability, retention, and support decision before implementation.

## How to contribute

See [project scope](project-scope.md), [decisions](decisions.md), and the repository issue templates. Use synthetic fixtures and bounded acceptance evidence.
