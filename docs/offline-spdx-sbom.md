# Offline SPDX SBOM

`tools/generate_spdx_sbom.py` creates an SPDX 2.3 JSON Software Bill of Materials for the exact unpublished wheel and source distribution described by a release-candidate manifest.

## Procedure

Build a fresh candidate outside the repository, then give the SBOM generator the manifest, an external output path, and an explicit UTC creation time:

```bash
python3 tools/build_release_candidate.py --output /tmp/cited-vault-recall-candidate
python3 tools/generate_spdx_sbom.py \
  --artifact-manifest /tmp/cited-vault-recall-candidate/release-candidate-manifest.json \
  --output /tmp/cited-vault-recall-candidate/cited-vault-recall.spdx.json \
  --created 2026-08-28T00:00:00Z
```

The SBOM generator verifies the size and SHA-256 of both artifacts before writing output. It rejects a malformed manifest, a changed artifact, or an output path inside the repository.

## Content and boundaries

The generated document describes:

- the exact `cited-vault-recall` package/version;
- the local unpublished-candidate status;
- the exact wheel and source-distribution filenames and SHA-256 values;
- SPDX package/file relationships and a package URL.

It does **not** upload an SBOM, create a release asset, invoke OIDC, generate provenance attestation, certify the remote action binary, publish to PyPI, or make a release claim. It is evidence for the exact local artifacts only; rebuild after any source or build-environment change.
