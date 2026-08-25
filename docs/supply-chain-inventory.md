# Offline supply-chain declaration inventory

`supply-chain-manifest.json` is a deterministic, checked-in inventory of **declared** Python dependencies and GitHub Actions workflow references. It is intentionally local, standard-library-only, and offline.

## Reproduce

Use Python 3.11+ because the verifier reads `pyproject.toml` with the standard-library `tomllib` module:

```bash
python3 tools/verify_supply_chain_manifest.py \
  --root . \
  --output supply-chain-manifest.json \
  --check
```

After a reviewed declaration change, regenerate explicitly and inspect the semantic diff:

```bash
python3 tools/verify_supply_chain_manifest.py \
  --root . \
  --output supply-chain-manifest.json \
  --write
```

`--check` fails on manifest drift or an unsupported/dynamic workflow `uses:` or literal pip-install declaration. The verifier reads only the selected repository files and writes only the explicit `--output` path in `--write` mode.

## Current baseline, accurately classified

```text
Runtime dependencies: none
Optional dependencies: none
Build requirement: setuptools>=68 — version_range_unpinned
Workflow references: actions/checkout@v4, actions/setup-python@v5 — mutable_or_unverified_reference
```

The same references can occur in multiple jobs; the manifest records each occurrence.

## Limits and deferred work

This inventory is **not a lockfile**, **not an SBOM**, and **not a provenance attestation**. It does not resolve dependencies, download artifacts, verify upstream action commits, calculate hashes, or guarantee reproducible builds. It intentionally does not wire into the Python 3.10 CI leg, because `tomllib` is Python 3.11+ and adding a parser dependency or an installation step would widen the supply-chain surface.

Replacing mutable action tags with full commit SHAs, adding dependency hashes/constraints or a lockfile, Dependabot, SBOMs, attestations, releases, and GitHub settings changes require separately verified upstream facts and explicit approval.
