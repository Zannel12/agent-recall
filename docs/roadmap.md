# Public roadmap

This is a short, evidence-based roadmap for Cited Vault Recall. It lists only current public priorities; it is not a promise of dates, a release authorization, or a hosted-service plan.

## Current state

- GitHub Release [`v0.2.0`](https://github.com/Zannel12/agent-recall/releases/tag/v0.2.0) is published.
- PyPI publication remains pending until a non-secret owner-side PyPI Trusted Publishing route exists.
- The product remains local-first, read-only, explicit-vault, and offline by default.
- No hosted deployment is selected. Public package distribution is not a hosted production service.

## Next autonomous priorities

1. Improve public documentation, release evidence, contribution intake, and reproducible OSS maintenance checks.
2. Extend deterministic lexical retrieval evaluation with synthetic fixtures and explicit measurable acceptance criteria.
3. Improve explicit-vault setup diagnostics and packaging/installation reliability without exposing paths or adding discovery.
4. Keep CI and dependency-policy boundaries narrow: no unreviewed runtime network access, telemetry, or mandatory model acquisition.

## Deferred and non-goals

- Semantic/vector/LLM retrieval is `DEFER` until its documented privacy-safe benchmark, provenance, offline-cache, resource, and citation-equivalence gates are met.
- Cloud sync, telemetry, automatic vault discovery/writes, and mandatory model downloads are not current roadmap work.
- A hosted API, Docker service, or other deployment requires a separate target, operator, rollback, privacy, observability, retention, and support decision before implementation.

## How to contribute

See [project scope](project-scope.md), [decisions](decisions.md), and the repository issue templates. Use synthetic fixtures and bounded acceptance evidence.
