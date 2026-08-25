from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "benchmarks" / "index" / "scale_benchmark.py"


class DerivedIndexBenchmarkTests(unittest.TestCase):
    def test_synthetic_scale_benchmark_records_lifecycle_only_decision(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": "src"},
            text=True,
            capture_output=True,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual("synthetic-derived-index-v1", report["dataset"])
        self.assertEqual(240, report["source_count"])
        self.assertEqual(["scale/note-0173.md"], report["direct_search"]["relative_paths"])
        self.assertEqual("not_implemented", report["derived_index"]["query_path"])
        self.assertFalse(report["derived_index"]["can_answer_query"])
        self.assertEqual("lifecycle_only", report["decision"])
        self.assertGreater(report["direct_search"]["median_ns"], 0)
        self.assertGreater(report["derived_index"]["build_ns"], 0)

    def test_benchmark_documentation_preserves_authority_and_decision(self):
        guide = (ROOT / "benchmarks" / "index" / "README.md").read_text(encoding="utf-8")
        self.assertIn("lifecycle-only", guide)
        self.assertIn("Markdown remains authoritative", guide)
        self.assertIn("not a performance claim", guide)


if __name__ == "__main__":
    unittest.main()
