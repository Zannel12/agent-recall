"""Versioned, synthetic evaluation for the deterministic local retriever."""

from __future__ import annotations

import json
from pathlib import Path

from .core import search_vault


METRICS = ("retrieval_recall_at_k", "retrieval_mrr", "retrieval_top_n_hit_rate", "temporal_accuracy", "abstention_accuracy")


def run_evaluation(root: Path) -> dict[str, object]:
    """Run only caller-selected, checked-in synthetic scenarios."""
    fixture = json.loads((root / "scenarios.json").read_text(encoding="utf-8"))
    scenarios: list[dict[str, object]] = fixture["scenarios"]
    results: list[dict[str, object]] = []
    retrieval_recall = retrieval_mrr = retrieval_top_n = temporal = abstention = 0.0
    retrieval_count = temporal_count = abstention_count = 0

    for scenario in scenarios:
        hits = search_vault(root / "corpus", str(scenario["query"]), int(scenario["k"]))
        paths = [hit.relative_path for hit in hits]
        relevant = set(scenario["relevant_paths"])
        kind = str(scenario["kind"])
        passed = False
        top_n = 0
        top_n_hit = False
        if kind == "retrieval":
            top_n = int(str(scenario["top_n"]))
            if not 1 <= top_n <= int(str(scenario["k"])):
                raise ValueError("retrieval top_n must be between 1 and k")
            retrieval_count += 1
            retrieval_recall += len(relevant.intersection(paths)) / len(relevant)
            top_n_hit = bool(relevant.intersection(paths[:top_n]))
            retrieval_top_n += float(top_n_hit)
            for rank, path in enumerate(paths, 1):
                if path in relevant:
                    retrieval_mrr += 1 / rank
                    break
            passed = bool(relevant.intersection(paths))
        elif kind == "temporal":
            temporal_count += 1
            passed = bool(paths) and paths[0] in relevant
            temporal += float(passed)
        elif kind == "abstention":
            abstention_count += 1
            passed = not paths
            abstention += float(passed)
        else:
            raise ValueError(f"unsupported scenario kind: {kind}")
        result = {"id": scenario["id"], "kind": kind, "passed": passed, "paths": paths}
        if kind == "retrieval":
            result.update({"top_n": top_n, "top_n_hit": top_n_hit})
        results.append(result)

    metrics = {
        "retrieval_recall_at_k": round(retrieval_recall / retrieval_count, 3),
        "retrieval_mrr": round(retrieval_mrr / retrieval_count, 3),
        "retrieval_top_n_hit_rate": round(retrieval_top_n / retrieval_count, 3),
        "temporal_accuracy": round(temporal / temporal_count, 3),
        "abstention_accuracy": round(abstention / abstention_count, 3),
    }
    return {"schema_version": fixture["schema_version"], "dataset": fixture["dataset"], "retriever": fixture["retriever"], "scenarios": results, "metrics": metrics}


def compare_metrics(baseline: dict[str, float], candidate: dict[str, float], *, target_metric: str) -> dict[str, object]:
    """Require non-regression everywhere plus strict target improvement."""
    for metric in METRICS:
        if candidate[metric] < baseline[metric]:
            return {"improved": False, "reason": f"metric_regressed:{metric}"}
    if candidate[target_metric] <= baseline[target_metric]:
        return {"improved": False, "reason": "target_not_improved"}
    return {"improved": True, "reason": "all_metrics_non_regressing_and_target_improved"}
