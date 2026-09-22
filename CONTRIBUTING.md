# Contributing

## Before opening a change

1. Read `AGENTS.md`, `ARCHITECTURE.md`, and `SECURITY.md`.
2. Add a failing behavior test before production code.
3. Keep the project offline, read-only, and agent-neutral by default.
4. Add exact provenance before copying or adapting external code.
5. Use synthetic test data only.
6. Use the bug and feature templates; do not include real vault content, absolute paths, credentials, or agent configuration.
7. Read the [project scope](docs/project-scope.md), [public roadmap](docs/roadmap.md), and [active decisions](docs/decisions.md) before proposing new behavior; they list welcome work and deliberate privacy boundaries.
8. Start with the [good first issues backlog](docs/good-first-issues.md) for bounded, synthetic-only contribution candidates; it does not create or promise GitHub issues.
9. For a versioned public release, follow the [maintainer release checklist](docs/maintainer-release-checklist.md); it does not authorize external publication.
10. Pull requests are validated by the `Tests / Python <version>` matrix and `Tests / Clean installation smoke` checks. They run under `pull_request` with read-only contents access; do not request `pull_request_target`, write permissions, secrets, publishing, or credential persistence for ordinary contribution checks.

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
