# One-shot C6b provenance attestation

This repository contains a deliberately temporary, manual-only GitHub Actions workflow for the user-approved C6b provenance attestation. GitHub documents artifact attestations as provenance evidence and requires `contents: read`, `attestations: write`, and `id-token: write` for the attesting job.[1]

## Narrow scope

The workflow:

- runs only through `workflow_dispatch` and has no push, pull-request, tag, release, registry, or PyPI trigger;
- builds the exact source commit `037f90437a05ae93a700d321d584b85abbb9e569`, not the workflow-definition commit;
- produces only the exact wheel and sdist names for version `0.2.0.dev0`;
- recomputes the candidate manifest size and SHA-256 values before transfer;
- transfers only those two subjects plus their manifest/checksum file, retained for one day;
- verifies the transferred data again in a separate job that does not check out or execute repository code;
- grants OIDC and attestation write permissions only to that separated job;
- supplies an explicit checksum list rather than a wildcard subject path.

All third-party Actions are fixed to full commits. The official `v4` tags resolve to the pinned `actions/attest`, `upload-artifact`, and `download-artifact` commits recorded in the workflow.[2][3][4]

## Boundary and cleanup

A successful run creates one durable GitHub provenance claim for the two exact unpublished artifacts. It does not create a tag, GitHub Release, release asset, registry upload, PyPI publication, deployment, or SBOM attestation. Deleting the one-day transfer artifact does not revoke an attestation.

After the single verified run, the temporary workflow must be removed from the default branch so it cannot be dispatched again without a new explicit approval and a new reviewed workflow.

## Sources

[1] https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds — GitHub Docs: artifact attestations
[2] https://api.github.com/repos/actions/attest/git/ref/tags/v4 — GitHub API: actions/attest v4 tag reference
[3] https://api.github.com/repos/actions/upload-artifact/git/ref/tags/v4 — GitHub API: upload-artifact v4 tag reference
[4] https://api.github.com/repos/actions/download-artifact/git/ref/tags/v4 — GitHub API: download-artifact v4 tag reference
