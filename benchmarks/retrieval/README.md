# Synthetic Retrieval Baseline

This corpus is synthetic and contains no personal vault data. It records the current behavior of the local lexical retriever before later ranking work.

## Metrics

- `Recall@k`: fraction of judged relevant source paths returned within each query's declared `k`.
- `MRR`: reciprocal rank of the first judged relevant path, averaged across queries.

## Reproduce

```bash
PYTHONPATH=src python3 -m unittest tests.test_retrieval_baseline -v
```

`baseline.json` is a checked-in no-regression record for the fixture corpus. It is not a claim about retrieval quality on a real vault.

## Current scoring model

The baseline retriever uses a deterministic local BM25-style sparse score with explicit title and relative-path boosts. Every result records `bm25`, `title_boost`, and `path_boost`, so score composition is inspectable in JSON and Markdown packets.
