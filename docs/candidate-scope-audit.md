# Candidate change and secret-scope audit

`tools/audit_release_candidate.py` produces a redacted, read-only candidate audit JSON. It is an evidence tool, not release authorization.

```bash
python3 tools/audit_release_candidate.py \
  --repository . \
  --artifact-manifest /absolute/path/outside/repo/release-candidate-manifest.json \
  --output /absolute/path/outside/repo/candidate-audit.json
```

Both output paths must be outside the repository. The script never writes into the repository, uploads artifacts, contacts a registry, changes Git state, reads untracked files as audit inputs, or prints matched secret values.

## Checks

- exact Git commit, clean working tree, and tracked-file count;
- forbidden tracked operational state (`.hermes`, `.grapify`, `.obsidian`), `.env` files, and private-key-style filenames;
- selected secret signatures (private-key markers, GitHub-token prefixes, and AWS access-key identifiers) without returning their values;
- if supplied, unpublished schema-1.0 artifact metadata and on-disk SHA-256/byte checks against `release-candidate-manifest.json`.

A passing audit is local evidence only. It does not prove registry availability, grant publication approval, create a tag/release, establish SBOM/provenance, or justify a production claim.
