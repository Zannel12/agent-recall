from __future__ import annotations

import unittest
from pathlib import Path
from typing import cast

from cited_vault_recall.evaluation import METRICS, run_evaluation


ROOT = Path(__file__).parents[1] / "benchmarks" / "evaluation" / "v1"


class EvaluationTopNTests(unittest.TestCase):
    def test_v1_reports_explicit_top_n_hit_rate_from_multiple_retrieval_cases(self):
        result = run_evaluation(ROOT)
        scenarios = {str(item["id"]): item for item in cast(list[dict[str, object]], result["scenarios"])}

        metrics = cast(dict[str, float], result["metrics"])
        self.assertIn("retrieval_top_n_hit_rate", METRICS)
        self.assertEqual(1.0, metrics["retrieval_top_n_hit_rate"])
        self.assertEqual(2, scenarios["policy-history"]["top_n"])
        self.assertTrue(scenarios["policy-history"]["top_n_hit"])
        self.assertEqual(
            ["policy-2025.md", "policy-2024.md"],
            scenarios["policy-history"]["paths"],
        )


if __name__ == "__main__":
    unittest.main()
