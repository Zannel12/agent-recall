# GitHub Actions SHA pinning

The test workflow pins its existing action references to immutable 40-character commits. This reduces exposure to a mutable major-version tag moving after review; it does not verify the remote action binary, create a lockfile, or establish an SBOM/provenance attestation.

## Verified mapping

The read-only official upstream tag-reference lookups established the two pinned mappings below.[1][2]

| Existing major tag | Pinned workflow reference | Verification evidence |
|---|---|---|
| `actions/checkout@v4` | `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` | The official GitHub tag reference for `v4` resolves to this commit.[1] |
| `actions/setup-python@v5` | `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` | The official GitHub tag reference for `v5` resolves to this commit.[2] |

Both references occur twice in `.github/workflows/tests.yml`. The workflow keeps its original `permissions: contents: read`, job structure, Python matrix, package-install commands, and test commands.

## Inventory boundary

`supply-chain-manifest.json` is regenerated from the checked-in declarations and labels these entries `full_sha_format_unverified`. That format label means the repository verifier confirmed a full SHA shape; the mapping evidence above records the separate, read-only upstream tag lookup.

The inventory remains **not a lockfile**, **not an SBOM**, **not a provenance attestation**, and does not pin `setuptools>=68`. Pinning package dependencies or generating release evidence requires its own approved scope.

## Rollback

Revert only the reviewed workflow and inventory changes, then rerun the supply-chain manifest check and CI. Do not change GitHub settings, permissions, release configuration, or credentials as part of this pinning action.

## Sources

[1] https://api.github.com/repos/actions/checkout/git/ref/tags/v4 — GitHub API checkout v4 tag reference
[2] https://api.github.com/repos/actions/setup-python/git/ref/tags/v5 — GitHub API setup-python v5 tag reference
