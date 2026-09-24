# Public decisions

This register captures active public product boundaries. It is intentionally short; implementation details and historical evidence stay in their linked documents.

## D-001 — Sparse lexical retrieval is the shipped default

**Status:** active.

Cited Vault Recall ships transparent local lexical retrieval with relative citations. This preserves a dependency-light, inspectable, offline-by-default baseline.

## D-002 — Semantic/vector/LLM retrieval is `DEFER`

**Status:** active.

The project will not add a dense or hybrid retrieval layer until the privacy-safe evaluation, pinned model provenance, offline acquisition/cache, measured resource comparison, and citation-equivalence requirements in [ADR-0001](adr/0001-defer-optional-dense-retrieval.md) are satisfied. No mandatory model download is accepted now.

## D-003 — Local-first is a product boundary

**Status:** active.

The package requires explicit vault selection and remains read-only and offline by default. It does not add telemetry, cloud synchronization, automatic vault discovery, or automatic vault writes without a separate architecture and security decision.

## D-004 — No hosted deployment is selected

**Status:** active.

Cited Vault Recall is not a hosted production service. A GitHub Release or PyPI package distribution does not establish a service deployment. Any hosted target needs its own design for ownership, rollback, privacy, observability, retention, and support.

## D-005 — PyPI uses a non-secret route or remains unpublished

**Status:** active.

`cited-vault-recall` is not published to PyPI. If publication proceeds, the preferred route is PyPI Trusted Publishing with OIDC and a narrowly reviewed workflow. Tokens, passwords, verification codes, cookies, and browser sessions are never requested or stored in repository automation or chat.

## D-006 — Tasks 1–15 complete; PyPI dispatch is a separate approval gate

**Status:** active.

Tasks 1–15 of the public OSS hardening queue are complete from direct repository, CI, and owner-confirmed account-side evidence. The pending PyPI Trusted Publisher is bound to the reviewed manual-only OIDC workflow and its `pypi` environment. The next action, Task 16, is an externally irreversible registry publication and requires a fresh scoped approval after a fresh preflight; it cannot be implied by workflow creation, a confirmation string, or the existing GitHub Release.

No hosted deployment is selected. Any change to that boundary remains a later owner-side configuration and architecture decision with a separately specified target, operator, rollback, privacy, observability, retention, and support scope.

## References

- [Project scope](project-scope.md)
- [Public roadmap](roadmap.md)
- [Release readiness](release-readiness.md)
- [Maintainer release checklist](maintainer-release-checklist.md)
