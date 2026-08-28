# Production-evidence policy

This is a **definition of evidence**, not a deployment runbook. It is **not a deployment**, creates no infrastructure, starts no service, changes no host, and is **not proof of production**.

Cited Vault Recall remains local-first, offline, read-only, and explicit-vault by default. No target is selected, no operator is assigned, and no production-evidence claim is currently valid.

## Claim threshold

A row may be called `Production-tested` only after one separately approved, owner-controlled deployment produces a retained evidence packet that satisfies every item below. A successful local test, package build, CI run, documentation page, MCP protocol test, or synthetic host integration is insufficient on its own.

The deployment procedure itself requires fresh explicit user approval immediately before execution. Approval for a release, host integration, or artifact build does not authorize a deployment.

## Required evidence packet

| Dimension | Minimum retained evidence | Boundary |
|---|---|---|
| Owner | Named accountable operator and a contact/decision record outside the package artifact. | No inferred owner from commit authorship or a GitHub account. |
| Environment | Defined operator-controlled target, deployment identifier, version/commit, deployment timestamp, and explicit distinction from test/staging. | Do not include hostname, absolute local paths, tokens, or private configuration. |
| Rollback | Pre-checked reversal steps, rollback owner, and direct evidence that the specific deployment can be reverted without modifying a selected vault. | A generic statement that rollback is possible is insufficient. |
| Privacy boundary | Data-flow statement proving selected-vault scope, read-only behavior, no telemetry, no unapproved network egress, and no retention of vault contents outside approved derived data. | Do not use a real private vault merely to obtain evidence. |
| Observability | Bounded health/readiness signal, structured failure evidence, and an agreed alert/escalation owner. | Logs must redact secrets, absolute paths, query text, and vault content unless separately approved. |
| Evidence retention | Location, access scope, retention period, and deletion/review owner for the evidence packet. | Retain only minimum metadata and redacted outcomes; never retain credentials or raw vault data. |

## Evidence procedure boundary

A future owner-controlled procedure must first use a synthetic vault and perform only the reviewed scoped workflow. If that is insufficient for the selected production claim, stop and obtain a new explicit approval before any broader data or environment scope.

The packet must identify the exact artifact checksum and commit, observed outcome, time window, rollback result or tested rollback readiness, and all deviations. Evidence must be independently reviewable without secrets, credentials, private keys, `.env` values, browser state, real-vault data, or absolute vault paths.

## Reject as insufficient

Reject as insufficient:

- documentation-only compatibility evidence;
- a passing unit suite, CI workflow, checksum manifest, or local CLI/MCP demonstration;
- an integration test without an owner, defined environment, rollback proof, privacy evidence, observability, and retention record;
- a deployment without direct retained evidence for the exact artifact;
- a claim based only on a vendor dashboard, HTTP 200, deployment log, or screenshot;
- an environment containing unredacted secrets, private vault content, or unspecified data retention.

## Current status and next boundary

No target is selected. Therefore `production deployment evidence` remains `BLOCKED` in the release readiness matrix, and no compatibility row is `Production-tested`.

This policy only completes the definition gate. It does not select a target, authorize a deployment, authorize a real host connection, authorize telemetry, or change Cited Vault Recall's local-first support boundary.
