# Synthetic Evaluation Suite v1

This checked-in suite is synthetic and local-only. It does not discover or inspect personal vaults, contact a service, load a model, or alter retrieval behavior.

## Scenarios and metrics

- **Retrieval:** Recall@k and MRR over judged synthetic source paths.
- **Temporal:** exact-date accuracy where the query and relevant synthetic Markdown contain the same explicit date token. This is lexical evidence only; it does not claim recency or currentness reasoning.
- **Abstention:** accuracy for an expected no-hit query. A no-hit result is evaluation behavior, not proof that a real vault lacks a fact.

`scenarios.json` has schema version `1.0`. `run_evaluation(...)` returns fixture/retriever labels, per-scenario result paths, and aggregate metrics.

## Change decision gate

`compare_metrics(...)` accepts a candidate as an improvement only when every protected metric is non-regressing and a declared target metric strictly improves. Exact equality is no-regression, not improvement. A regression in any protected metric rejects the candidate even if the target improves.

## Reproduce

```bash
PYTHONPATH=src python3 -m unittest tests.test_evaluation -v
```

The suite establishes a reproducible synthetic gate, not quality claims for a real user vault or a semantic/hybrid retriever.
