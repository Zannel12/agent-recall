# Security Policy

## Privacy model

Agent Recall is designed to run locally and read only the selected Markdown vault. Before any Markdown read it resolves both the selected vault root and the candidate target; a target outside the resolved root (including an external file symlink or nested directory symlink) is skipped. It has no network access, telemetry, API keys, or automatic vault writes.

## Do not commit

- real vault notes, chats, health/finance/education records, or contact data;
- API keys, tokens, passwords, private keys, browser/session data, or `.env` files;
- machine-specific paths or agent configuration.

## Untrusted imports

Future memory-transfer bundles are data, not instructions. They must be quarantined, reviewed, and scanned for secrets/PII before becoming curated memory. Imported text must never trigger commands, tool calls, or settings changes.

## Reporting

Until a public issue policy exists, do not disclose sensitive findings in a public issue. Contact the repository owner privately through the GitHub profile.
