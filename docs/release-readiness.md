# Release readiness matrix

This page distinguishes verified public-release facts from future publication and hosted-deployment work. It is documentation and a local contract only: it does not create a tag, release, publication, deployment, SBOM, or attestation.

## Status vocabulary

- `READY` — the stated evidence has been verified for the named public release or current repository snapshot.
- `NOT_READY` — a required artifact or proof does not yet exist.
- `BLOCKED` — progress depends on an unresolved prerequisite or external owner action.

## Current readiness

| Gate | Status | Current evidence or blocker | Next allowed step |
|---|---|---|---|
| Local regression and clean-install evidence | `READY` | The repository has focused/full regression tests and CI evidence; rerun them for each new reviewed commit. | Re-run against the next reviewed commit. |
| GitHub Release `v0.2.0` | `READY` | GitHub Release `v0.2.0` is published from immutable tag [`v0.2.0`](https://github.com/Zannel12/agent-recall/releases/tag/v0.2.0). | Keep release notes and public docs truthful. |
| Exact `v0.2.0` release assets | `READY` | The published wheel, sdist, and SPDX SBOM were read back and hashed after upload. | Build a new exact set for any future version. |
| SPDX SBOM and provenance | `READY` | The current release assets have an SPDX 2.3 SBOM and GitHub provenance attestation. | Never reuse this evidence for different artifact bytes. |
| PyPI publication | `BLOCKED` | Trusted Publisher and a reviewed manual-only OIDC workflow are configured; `cited-vault-recall` / `0.2.0` remains absent at the last registry check. | Perform a fresh preflight and obtain fresh explicit approval before dispatch. |
| Semantic/vector decision gate | `READY` | The explicit decision is `DEFER`; mandatory model downloads, vector indexes, and LLM retrieval are not allowed. | Reconsider only through a separately approved evidence gate. |
| Hermes integration evidence | `READY` | Hermes has bounded synthetic-vault `Integration-tested` evidence only. | Do not claim production-tested host integration. |
| Hosted production deployment | `BLOCKED` | This is a local Python package, not a hosted service; no target, operator, rollback, privacy, observability, or retention boundary is defined. | Either record “no hosted deployment” or approve a separate hosted-product design. |

## Future external-action gates

Every future external mutation remains independently scoped: one action per Goal turn, fresh preflight, exact read-back, and no credentials in chat. The ordered maintainer procedure is documented in the [release checklist](maintainer-release-checklist.md).

| Future action | Current status | Preconditions | Hard stop |
|---|---|---|---|
| Publish `cited-vault-recall==0.2.0` to PyPI | `BLOCKED` | PyPI Trusted Publisher, exact asset hashes, fresh registry preflight, reviewed manual workflow | Stop if owner-side route or OIDC verification is unavailable. |
| Create a later GitHub Release | `NOT_READY` | New version, exact artifacts, SBOM, attestation, tag, release notes | Do not mix artifacts or evidence across versions. |
| Hosted deployment | `BLOCKED` | Named target, operator, rollback, privacy boundary, observability, retention, support scope | Do not treat distribution publication as service deployment. |

## Non-action guarantee

This matrix does not grant implicit approval, handle credentials, change a host, invoke OIDC, upload artifacts, or publish anything. Historical `0.2.0.dev0` evidence is distinct from `v0.2.0` release evidence.
