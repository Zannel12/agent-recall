# Project scope

Cited Vault Recall is a local-first Python package for searching a user-selected Markdown vault and returning source-linked context. It is designed for transparent, bounded retrieval rather than a cloud memory platform.

## Contributions welcome

- reproducible bug fixes using synthetic fixtures;
- public documentation, installation, accessibility, and contributor-experience improvements;
- deterministic lexical retrieval quality, ranking, citations, diagnostics, and explicit-vault UX;
- packaging, supported-Python, wheel/sdist, CLI, MCP-stdio, and CI reliability work;
- security and privacy reports through the responsible-disclosure route in `SECURITY.md`.

## Deliberate boundaries

The project does not accept casual changes that introduce:

- network retrieval, telemetry, cloud synchronization, or upload of vault contents;
- automatic vault discovery, writes, deletion, or reorganization;
- mandatory model downloads, vector indexes, or LLM-backed retrieval;
- real vaults, personal data, credentials, browser state, host configuration, or machine paths in fixtures, issues, or pull requests.

A proposal that changes one of these boundaries needs a separate architecture and security decision before implementation. Public package distribution is not a hosted production service and does not establish a production deployment.

## Intake

Use the repository issue templates for bugs, documentation, safe retrieval, packaging, and non-sensitive security/privacy triage. Keep reports reproducible with synthetic data and provide a bounded acceptance criterion.
