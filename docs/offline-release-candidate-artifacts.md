# Offline release-candidate artifacts

This procedure builds an **unpublished** local wheel and source distribution, then records SHA-256 checksums for the exact files. It is preparation evidence only: it does not create a Git tag, GitHub Release, package upload, SBOM, provenance attestation, OIDC request, or registry lookup.

## Build command

Run from the repository root and choose a disposable output directory outside the repository:

```bash
python3 tools/build_release_candidate.py --output /tmp/cited-vault-recall-candidate
```

The script removes and recreates only the selected `--output` directory. It rejects an output directory inside the repository, so build products cannot accidentally become tracked source artifacts.

## Output contract

```text
<output>/
  artifacts/
    <one wheel>
    <one sdist .tar.gz>
  SHA256SUMS
  release-candidate-manifest.json
```

The JSON manifest is schema `1.0` and contains only:

```text
package
version
unpublished: true
artifacts[]: filename, bytes, sha256
```

`SHA256SUMS` uses relative `artifacts/<filename>` paths and contains no machine path. The artifact list and checksum lines are filename-sorted.

## Verification boundary

The builder invokes the repository's configured local `setuptools.build_meta` backend and performs no package download, upload, or network action itself. It produces a fresh candidate from the current source tree; it does **not** claim bit-for-bit reproducibility across arbitrary machines, Python versions, setuptools versions, timestamps, or build environments.

Before any future user-approved release action, rebuild from the exact approved commit, inspect both artifacts, compare the recorded checksums against the actual files, and attach the resulting evidence only through the separately approved release procedure.
