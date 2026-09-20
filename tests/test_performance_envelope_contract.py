from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PerformanceEnvelopeContractTests(unittest.TestCase):
    def test_performance_envelope_qualifies_synthetic_observations(self):
        document = (ROOT / "docs" / "performance-envelope.md").read_text(encoding="utf-8")

        for required in (
            "240-source",
            "1,000-source",
            "synthetic",
            "machine-independent",
            "No hard global timing threshold",
            "PYTHONPATH=src python3 benchmarks/index/scale_benchmark.py",
            "PYTHONPATH=src python3 benchmarks/retrieval/scale_benchmark.py",
            "not a production performance claim",
        ):
            self.assertIn(required, document)


if __name__ == "__main__":
    unittest.main()
