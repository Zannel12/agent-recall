# Maintainer release checklist

Use this checklist for a **new version only**. It is a process aid, not authorization: each external mutation still needs a fresh scoped decision and exact read-back.

## 1. Version and release notes

- [ ] Choose the next semantic version from the public API and compatibility change.
- [ ] Update metadata, user documentation, changelog, and any CLI/MCP version literal together.
- [ ] Add or update a behavior-level release-state contract before changing public release claims.
- [ ] State current limits accurately: local-first scope, PyPI state, host-integration evidence level, and hosted-deployment status.

## 2. Focused and full verification

- [ ] Run the changed contract tests and confirm the intended RED failure before implementation.
- [ ] Run focused tests after the minimal change.
- [ ] Run the full suite, `git diff --check`, and the bounded synthetic CLI/MCP smoke checks.
- [ ] Review staged paths for private vaults, agent state, credentials, `.env`, model files, and other excluded data.
- [ ] Commit, push, and read back exact CI success for the reviewed commit.

## 3. Exact artifacts and checksums

- [ ] Start from a clean, reviewed source commit and build only wheel and sdist outside the repository.
- [ ] Record filenames, byte sizes, SHA-256 digests, source commit, version, and explicit unpublished/published state.
- [ ] Install the wheel in a fresh environment and run only synthetic fixtures.
- [ ] Do not claim byte-for-byte reproducibility across different builders unless it has been independently demonstrated.

## 4. SPDX SBOM

- [ ] Generate an SPDX-2.3 SBOM for the exact artifact bytes selected above.
- [ ] Recompute the artifact checksums before SBOM generation and inspect the SBOM references afterward.
- [ ] Never attach an SBOM created for different bytes, a different source commit, or a different version.

## 5. GitHub provenance attestation

- [ ] Use a reviewed, manual-only, least-privilege workflow that receives only the exact subjects.
- [ ] Keep build and OIDC/attestation permissions separated where practical.
- [ ] Verify the produced attestation against each exact wheel/sdist with repository and signer-workflow identity constraints.
- [ ] Record the attestation URL/ID and retain the distinction between historical and current artifact evidence.

## 6. Annotated Git tag

- [ ] Perform a fresh preflight: clean tree, remote branch, version, candidate commit, CI, artifacts, SBOM, and attestation.
- [ ] Obtain fresh approval for this one external action.
- [ ] Create and push an annotated Git tag pointing to the reviewed source commit.
- [ ] Read the remote tag object and peeled target back exactly.

## 7. GitHub Release

- [ ] Perform a fresh preflight confirming the tag, absent/released state, exact assets, hashes, SBOM, and attestation.
- [ ] Obtain fresh approval for this one external action.
- [ ] Create the GitHub Release and attach only the verified wheel, sdist, and matching SBOM.
- [ ] Read back the release URL, tag, asset list, byte sizes, and digests; re-download and hash assets when practical.

## 8. PyPI publication

- [ ] Perform a fresh PyPI package/version availability check.
- [ ] Use the reviewed manual-only workflow `.github/workflows/pypi-publish.yml`; do not add automatic triggers, a checkout step, repository write permissions, or a package-index token.
- [ ] Dispatch only after a fresh preflight and type the exact workflow confirmation phrase for the reviewed version; its job downloads only the named GitHub Release wheel/sdist and verifies their approved SHA-256 hashes before it can invoke PyPI Trusted Publishing.
- [ ] Confirm the workflow job uses the dedicated `pypi` environment and only `id-token: write`; Never paste or store credentials, secrets, variables, passwords, tokens, codes, cookies, or browser sessions.
- [ ] Obtain fresh approval for this one external action.
- [ ] Publish only the exact wheel and sdist already selected for the release.
- [ ] Read back the PyPI version and download/hash each package file against the approved artifacts.

## Operating rule

Execute one external action per Goal turn. Every external action needs a fresh preflight, a fresh scoped approval where required, and an exact read back before the next action. A GitHub Release, registry publication, provenance attestation, tag, or hosted deployment is never implied by a passing build.
