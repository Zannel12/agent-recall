# Release readiness matrix

This page is a bounded readiness assessment for Agent Recall. It separates completed local evidence from work that must remain at the end of the release-readiness roadmap. It is not release authorization and does not create a tag, release, publication, deployment, SBOM, or attestation.

## Status vocabulary

- `READY` — the stated local evidence exists and has been verified for the current repository snapshot.
- `NOT_READY` — a required artifact or proof does not yet exist.
- `BLOCKED` — progress depends on an unresolved prerequisite or an external fact/owner action.

## Current readiness

| Gate | Status | Current evidence or blocker | Next allowed step |
|---|---|---|---|
| Local regression and clean-install evidence | `READY` | The repository has focused/full regression tests and CI evidence; the exact count and run are recorded per completed roadmap point. | Re-run against the next reviewed commit. |
| Unreleased package state | `READY` | Metadata remains `0.2.0.dev0`; no GitHub tag, GitHub Release, or registry publication exists. | Keep unreleased until final gates are approved. |
| Publishable local package identity | `READY` | Local distribution/import/executables now use the non-legacy ADR-0002 identity; registry availability is deliberately unknown. | Complete A4 locally, then re-check the registry only in the separately approved final publication procedure. |
| Release-candidate artifact/checksum proof | `NOT_READY` | No reviewed release-candidate artifact set is designated. | Complete roadmap A4 locally. |
| Semantic/vector decision gate | `NOT_READY` | ADR-0001 defers optional semantic retrieval pending reproducible evidence. | Complete roadmap A5; do not acquire a model or add dependencies yet. |
| Real-host procedure packs | `NOT_READY` | Existing host information is documentation-only or synthetic protocol evidence. | Complete roadmap A6 without configuring any host. |
| Production-evidence definition | `NOT_READY` | No deployment target/support boundary is defined. | Complete roadmap A7 without deploying anything. |

## Final approval gates

Every item below remains intentionally last. It requires a **fresh explicit user approval** immediately before its own execution and exactly **one final action per Goal turn**. Completing one row never approves another row.

| Final action | Current status | Preconditions | Owner participation / hard stop |
|---|---|---|---|
| dependency/action SHA pinning | `NOT_READY` | Verified official upstream commit facts | Stop if a trust anchor cannot be independently verified. |
| semantic/vector/LLM retrieval | `BLOCKED` | A5 passes; selected model revision/hash and resource costs are approved | Stop before dependency/model acquisition, network use, or any quality regression. |
| real Hermes integration | `NOT_READY` | A6 protocol, synthetic vault, approved rollback | Owner controls any host configuration directly; no real/private vault. |
| real Codex / Claude Code / Cursor / OpenClaw integration | `NOT_READY` | A6 protocol for the named host, synthetic vault, approved rollback | One host at a time; owner completes any host-specific install/auth directly. |
| production deployment evidence | `BLOCKED` | A7 defines a target, operator, privacy boundary, rollback, and support scope | If no target is approved, retain local-first delivery and record no deployment. |
| SBOM | `NOT_READY` | Exact reviewed artifacts and checksums | Generate only for the approved artifact set. |
| provenance attestation | `NOT_READY` | Exact reviewed artifacts, approved workflow permissions | Stop if OIDC/workflow permissions or output cannot be verified. |
| Git tag | `NOT_READY` | Exact approved commit/version and release evidence | User-visible external publication event; requires separate approval. |
| GitHub Release | `NOT_READY` | Approved tag and reviewed assets/checksums/SBOM/attestation where selected | Read back the published release and all assets. |
| PyPI publication | `BLOCKED` | Non-colliding identity, immediate registry check, owner-confirmed namespace, reviewed artifact | There is currently **no PyPI upload**; owner completes registry authentication directly. |

## Non-action guarantee

This matrix is documentation and a local contract test only. It never grants an implicit approval, handles credentials, changes a host, invokes OIDC, uploads artifacts, or publishes anything. User approval applies only to the single selected final row and expires after that one action.
