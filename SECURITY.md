# Security Policy

## Privacy model

Agent Recall is designed to run locally and read only the selected Markdown vault. Before any Markdown read it resolves both the selected vault root and the candidate target; a target outside the resolved root (including an external file symlink or nested directory symlink) is skipped. It has no network access, telemetry, API keys, or automatic vault writes.

## Do not commit

- real vault notes, chats, health/finance/education records, or contact data;
- API keys, tokens, passwords, private keys, browser/session data, or `.env` files;
- machine-specific paths or agent configuration.

## Retrieval scope and exclusion policy

A caller selects exactly one local vault; Agent Recall does not discover vaults or aggregate multiple vaults. The candidate allowlist is Markdown (`*.md`) only. Before resolving or reading a Markdown candidate, the retriever applies vault-root `.recallignore` glob patterns and default sensitivity filename patterns: `*.secret.md` and `*.private.md`. Excluded sources are counted only in aggregate diagnostics; their paths and contents are not returned. This is a deterministic filename policy, not a claim to detect every secret in arbitrary content.

## Untrusted imports and retrieved content

Future memory-transfer bundles and any text wrapped as `UntrustedContent` are data, not instructions. The structured envelope carries `trust="untrusted"`, `source_kind`, `source_id`, original body, and `executable=false`.

They must be quarantined, reviewed, and scanned for secrets/PII before becoming curated memory. Imported or retrieved Markdown must never trigger commands, tool calls, settings changes, or memory promotion. Markdown rendering is a transport format, **not** a security boundary; calling agents must preserve the envelope and apply their own instruction/data separation.

## Reporting

Report security vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/Zannel12/agent-recall/security/advisories/new). Do **not** open a public issue for a sensitive finding. Include an affected version or commit, a safe reproduction, impact, and suggested mitigation; do not include credentials, real vault data, or secrets. Maintainers will acknowledge a valid report, but no response-time promise is made.
