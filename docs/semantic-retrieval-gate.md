# Semantic retrieval decision gate

Cited Vault Recall currently ships only dependency-free lexical retrieval. This page and `benchmarks/semantic-retrieval-decision-gate.json` make the decision boundary reproducible: the current decision is **DEFER** and semantic/vector/LLM implementation is not allowed.

## Evidence scope

The existing synthetic lexical baseline is:

```text
benchmarks/evaluation/v1/baseline.json
```

ADR-0001 also records two synthetic paraphrase probes where lexical Recall@1 was `0.0`. That is an evidence of a possible limitation, not a mandate to add embeddings and not a real-vault quality claim.

## Required prerequisites

All five machine-readable prerequisites must change from `NOT_READY` to `READY` before an implementation proposal can be considered:

1. Representative, privacy-safe synthetic paraphrase/multilingual benchmark with judged citations.
2. Pinned model provenance: revision, license review, checksum, size budget, and record.
3. Operator-controlled offline acquisition/cache contract.
4. Measured synthetic quality, latency, memory, and disk comparison against the lexical default.
5. Explicit opt-in behavior preserving citations, relative paths, error semantics, and lexical default retrieval.

## Current boundary

This gate adds **no model download**, **no dependency change**, no model acquisition, no vector index, no LLM call, and no network workflow. `sentence-transformers`, `transformers`, `torch`, and `faiss` are not added as project dependencies.

It does not make a real-vault quality claim, a performance claim, or a claim that a selected model is suitable. Any future implementation remains a final user-approved action after the prerequisites are actually evidenced.
