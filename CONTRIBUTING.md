# Contributing

## Before opening a change

1. Read `AGENTS.md`, `ARCHITECTURE.md`, and `SECURITY.md`.
2. Add a failing behavior test before production code.
3. Keep the project offline, read-only, and agent-neutral by default.
4. Add exact provenance before copying or adapting external code.
5. Use synthetic test data only.

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
