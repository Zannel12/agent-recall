# ADR-0001: Defer optional local dense/hybrid retrieval

- **Status:** accepted
- **Date:** 2026-08-24
- **Decision point:** B01.5

## Context

Cited Vault Recall currently provides dependency-free, local BM25-style retrieval over cited Markdown chunks. Its baseline corpus is synthetic and proves only exact/lexical no-regression behavior.

A targeted semantic paraphrase probe found the current sparse retriever does not retrieve either intended source at rank 1:

```text
"removing remembered facts" → expected retention.md → returned none
"automatic saving of personal details" → expected consent.md → returned none
Recall@1: 0.0 (2 synthetic paraphrase probes)
```

This demonstrates a potential semantic-recall gap. It does **not** prove that a dense layer will improve the product on real user vaults.

## Candidates compared

| Candidate | Evidence | Current fit | Decision |
|---|---|---|---|
| Existing sparse BM25-style chunks | Implemented locally; deterministic, inspectable, cited, offline, no model weights | Fits all v0.1 privacy and install boundaries | Keep as trusted default |
| Local multilingual dense embeddings via `intfloat/multilingual-e5-small` + Sentence Transformers | Model card describes a 384-dimensional multilingual embedding model and documents query prefixes; Sentence Transformers documents local corpus/query embedding and cosine search | `sentence_transformers`, `transformers`, `torch`, and `faiss` are absent from the current environment; no model revision/weight hash is pinned; adding it would require a new dependency and a model-weight acquisition path | Do not implement now |
| Hybrid sparse+dense fusion | Could preserve sparse citations while adding recall, but requires the dense candidate above plus a reproducible fusion and evaluation contract | Same unresolved model, provenance, storage, and benchmark prerequisites | Do not implement now |

Sources consulted:

- [multilingual-e5-small model card](https://huggingface.co/intfloat/multilingual-e5-small)
- [Sentence Transformers semantic-search documentation](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

External model-card metrics are not adopted as Cited Vault Recall metrics.

## Decision

**Do not add a dense or hybrid retrieval implementation now.** The checked-in machine-readable state is [the semantic retrieval decision gate](../semantic-retrieval-gate.md); it remains `DEFER` until every documented prerequisite is evidenced.

The optional semantic layer has not earned implementation because no candidate has been run against a versioned Cited Vault Recall acceptance corpus, and the following prerequisites are absent:

1. A representative, privacy-safe benchmark that includes paraphrase and multilingual queries beyond the two diagnostic probes.
2. A pinned model revision, license review, checksums/weight provenance, and explicit model-size budget.
3. An offline/reproducible model acquisition and local-cache contract with no silent network fetch or telemetry.
4. Measured quality, latency, memory, and disk comparison against sparse retrieval.
5. A user-visible mode boundary: dense/hybrid must be optional and must retain the same chunk citation and relative-path guarantees.

## Consequences

- Sparse BM25-style retrieval remains the only shipped search path.
- The semantic-recall probe stays evidence of an open limitation, not a mandate for embeddings.
- A future proposal may reopen this ADR only with the five prerequisites above and a measurable acceptance threshold.
