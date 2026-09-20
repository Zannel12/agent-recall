# Contributing

## Before opening a change

1. Read `AGENTS.md`, `ARCHITECTURE.md`, and `SECURITY.md`.
2. Add a failing behavior test before production code.
3. Keep the project offline, read-only, and agent-neutral by default.
4. Add exact provenance before copying or adapting external code.
5. Use synthetic test data only.
6. Use the bug and feature templates; do not include real vault content, absolute paths, credentials, or agent configuration.
7. Read the [project scope](docs/project-scope.md) before proposing new behavior; it lists welcome contribution areas and deliberate privacy boundaries.
8. For a versioned public release, follow the [maintainer release checklist](docs/maintainer-release-checklist.md); it does not authorize external publication.

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
