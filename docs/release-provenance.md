# Release and provenance policy

## Release channel and authorization

Cited Vault Recall releases are **GitHub-only**. **No PyPI upload** occurs unless the final, separately approved publication point is selected after an immediate target-registry check. A release needs a separate explicit release decision; this policy is not release authorization.

A release tag must match the version in `pyproject.toml` (for example `v0.1.0` for `0.1.0`) and must point to the reviewed commit range.

## Versioning and public API

The public v0.1 API is the package `__all__`: `SearchHit`, `render_packet`, and `search_vault`.

- **PATCH**: compatible fixes, documentation, or internal changes.
- **MINOR**: backward-compatible public additions.
- **MAJOR**: breaking public API, CLI contract, schema, or supported-environment changes.

## Future release evidence

Before a future GitHub release, the release operator must record:

1. clean-tree and outgoing commit-range audit, including excluded/private-artifact review;
2. full test suite and `git diff --check` results;
3. isolated artifact build, artifact inspection, and checksums;
4. generated SBOM for the exact artifacts;
5. GitHub provenance attestation using the release workflow's approved OIDC permissions;
6. review of `UPSTREAMS.md` and `ADAPTATIONS.md`. Copied/adapted code must have exact source path, revision, license, destination, and modification record;
7. GitHub release asset upload and a read-back verification of tag, assets, checksums, SBOM, and attestation.

The SBOM and provenance attestation are required future release assets. They are not claims about current CI.

## Non-action guarantee

**No release, tag, artifact, or attestation is created by this policy.** It does not publish a package, modify workflows, invoke OIDC, or handle credentials.
