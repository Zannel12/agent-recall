from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import cast

from agent_recall.evaluation import compare_metrics, run_evaluation


ROOT = Path(__file__).parents[1] / "benchmarks" / "evaluation" / "v1"


class EvaluationTests(unittest.TestCase):
    def test_versioned_synthetic_suite_records_retrieval_temporal_and_abstention_metrics(self):
        result = run_evaluation(ROOT)

        self.assertEqual(result["schema_version"], "1.0")
        self.assertEqual(result["dataset"], "synthetic-evaluation-v1")
        self.assertEqual(result["retriever"], "lexical-v0.1.0")
        baseline = json.loads((ROOT / "baseline.json").read_text(encoding="utf-8"))
        self.assertEqual(result["metrics"], baseline["metrics"])
        self.assertEqual(["retrieval", "retrieval", "temporal", "abstention"], [item["kind"] for item in cast(list[dict[str, object]], result["scenarios"])])

    def test_comparison_requires_non_regression_and_strict_target_improvement(self):
        baseline = {"retrieval_recall_at_k": 0.8, "retrieval_mrr": 0.7, "retrieval_top_n_hit_rate": 0.7, "temporal_accuracy": 0.6, "abstention_accuracy": 0.9}
        equal = compare_metrics(baseline, baseline, target_metric="retrieval_mrr")
        improved = compare_metrics(baseline, {**baseline, "retrieval_mrr": 0.8}, target_metric="retrieval_mrr")
        regressed = compare_metrics(baseline, {**baseline, "temporal_accuracy": 0.5, "retrieval_mrr": 0.8}, target_metric="retrieval_mrr")

        self.assertEqual(equal, {"improved": False, "reason": "target_not_improved"})
        self.assertEqual(improved, {"improved": True, "reason": "all_metrics_non_regressing_and_target_improved"})
        self.assertEqual(regressed, {"improved": False, "reason": "metric_regressed:temporal_accuracy"})


if __name__ == "__main__":
    unittest.main()
