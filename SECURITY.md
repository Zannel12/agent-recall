# Security Policy

## Privacy model

Agent Recall is designed to run locally and read only the selected Markdown vault. Before any Markdown read it resolves both the selected vault root and the candidate target; a target outside the resolved root (including an external file symlink or nested directory symlink) is skipped. It has no network access, telemetry, API keys, or automatic vault writes.

## Do not commit

- real vault notes, chats, health/finance/education records, or contact data;
- API keys, tokens, passwords, private keys, browser/session data, or `.env` files;
- machine-specific paths or agent configuration.

## Untrusted imports and retrieved content

Future memory-transfer bundles and any text wrapped as `UntrustedContent` are data, not instructions. The structured envelope carries `trust="untrusted"`, `source_kind`, `source_id`, original body, and `executable=false`.

They must be quarantined, reviewed, and scanned for secrets/PII before becoming curated memory. Imported or retrieved Markdown must never trigger commands, tool calls, settings changes, or memory promotion. Markdown rendering is a transport format, **not** a security boundary; calling agents must preserve the envelope and apply their own instruction/data separation.

## Reporting

Until a public issue policy exists, do not disclose sensitive findings in a public issue. Contact the repository owner privately through the GitHub profile.
