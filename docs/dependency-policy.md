# Dependency policy

Cited Vault Recall intentionally ships with no runtime dependencies and no optional dependency groups. The standard library is the current runtime baseline.

## Explicit dependency review

Any proposed runtime or optional dependency must be reviewed in the same change before it is declared. The pull request must state:

1. the exact package, version constraint, license, and why the standard library cannot meet the need;
2. whether it is a network-capable runtime dependency, starts subprocesses, reads credentials, or introduces telemetry;
3. install size, supported Python impact, offline behavior, and how the dependency is verified;
4. a privacy boundary, synthetic test evidence, and a rollback/removal path;
5. the matching update and review of `supply-chain-manifest.json`.

The review is a decision record, not an automatic approval. The maintainer must reject additions that create no silent network access, automatic vault discovery, hidden writes, or unbounded external data processing.

## Model and vector boundary

A mandatory model download is forbidden. The following dense-retrieval packages are not current project dependencies and may not be added as an ordinary patch: `sentence-transformers`, `transformers`, `torch`, and `faiss`.

Any reconsideration follows [`semantic-retrieval-gate.md`](semantic-retrieval-gate.md) and ADR-0001: it requires a privacy-safe synthetic benchmark, pinned model provenance and license, an operator-controlled offline acquisition/cache contract, measured resource comparison, and explicit opt-in citation equivalence. Until that gate changes under documented evidence, semantic/vector/LLM implementation remains `DEFER`.

## Enforcement and reproduction

The checked-in [`supply-chain-manifest.json`](../supply-chain-manifest.json) declares the runtime/optional/build dependencies and literal workflow installs. Run:

```bash
python3 tools/verify_supply_chain_manifest.py \
  --root . \
  --output supply-chain-manifest.json \
  --check
```

A dependency declaration that changes without the matching reviewed inventory fails the existing manifest check. This policy and its contract test make the current empty runtime baseline visible; changing either requires an explicit, reviewable diff rather than a silent package install.
