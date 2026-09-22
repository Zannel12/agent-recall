# Good first issues

This is a contributor-ready backlog, not a set of GitHub issues and not a promise of urgency. It was rebuilt after Tasks 6–10 were verified complete, so it does not relabel completed work as open.

All items use synthetic fixtures only. **No real vault**, personal data, credential, or machine path belongs in a contribution. **No network** access or **No model download** is introduced by these candidates. **Do not create GitHub issues** from this page automatically; a maintainer may later choose which items to publish.

## 1. Add a checked-in Markdown link contract

**Why it is small:** public docs already use repository-relative links, but there is no deterministic checker for broken local Markdown targets.

**Acceptance check:** add a stdlib-only test that walks tracked public Markdown, validates local relative links to tracked files/anchors according to a documented bounded rule, and passes on the repository.

**Scope exclusion:** No network link checking, crawling, telemetry, or private/local documentation paths.

## 2. Add an unreadable-vault doctor remediation

**Why it is small:** `doctor` already gives a path-free remedy for a missing vault; an existing but unreadable explicit directory still needs one bounded next-step diagnostic.

**Acceptance check:** use a synthetic unreadable-vault fixture or platform-safe equivalent to assert a stable, path-free doctor code and remediation value without discovery.

**Scope exclusion:** No permission escalation, path echoing, retrying alternative directories, or automatic vault discovery.

## 3. Document PowerShell explicit-vault setup

**Why it is small:** the local-first quickstart is POSIX-oriented; a PowerShell example can make explicit setup more accessible while keeping platform evidence honest.

**Acceptance check:** add a PowerShell section that creates a venv, installs the local package, invokes `doctor --vault <explicit-vault> --json`, and labels Windows execution as documented unless it is actually run in CI.

**Scope exclusion:** No Windows support claim without execution evidence, no installer download script, no browser automation, and no search for a vault.

## 4. Add a synthetic paraphrase evaluation fixture

**Why it is small:** ADR-0001 records a lexical paraphrase limitation, but the versioned evaluation suite does not yet contain a dedicated judged paraphrase scenario.

**Acceptance check:** add only synthetic Markdown and judged paths, make the lexical result explicit in the baseline, and preserve deterministic test execution without external services.

**Scope exclusion:** No semantic/vector/LLM implementation, model download, new runtime dependency, network access, or real-vault quality claim.

## Contribution boundary

Read [project scope](project-scope.md), [dependency policy](dependency-policy.md), and [semantic retrieval gate](semantic-retrieval-gate.md) before beginning. Every patch must retain the local-first, read-only, offline-by-default contract and include a focused, reviewable acceptance check.
