from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
GATE = ROOT / "benchmarks" / "semantic-retrieval-decision-gate.json"


class SemanticRetrievalDecisionGateTests(unittest.TestCase):
    def test_gate_defers_implementation_until_all_reproducible_prerequisites_are_ready(self):
        gate = json.loads(GATE.read_text(encoding="utf-8"))

        self.assertEqual("1.0", gate["schema_version"])
        self.assertEqual("DEFER", gate["decision"])
        self.assertFalse(gate["implementation_allowed"])
        self.assertEqual("benchmarks/evaluation/v1/baseline.json", gate["lexical_baseline"])
        prerequisites = gate["prerequisites"]
        self.assertEqual(
            {
                "representative_synthetic_benchmark",
                "pinned_model_provenance",
                "offline_acquisition_contract",
                "quality_latency_memory_disk_comparison",
                "opt_in_citation_equivalence",
            },
            set(prerequisites),
        )
        self.assertTrue(all(item["status"] == "NOT_READY" for item in prerequisites.values()))

    def test_gate_forbids_unapproved_dense_dependencies_or_model_downloads(self):
        gate = json.loads(GATE.read_text(encoding="utf-8"))
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        guide = (ROOT / "docs" / "semantic-retrieval-gate.md").read_text(encoding="utf-8")

        for dependency in ("sentence-transformers", "transformers", "torch", "faiss"):
            self.assertNotIn(dependency, pyproject.lower())
        self.assertIn("no model download", guide)
        self.assertIn("no dependency change", guide)
        self.assertIn("real-vault quality claim", guide)
        self.assertIn("DEFER", gate["decision"])


if __name__ == "__main__":
    unittest.main()
