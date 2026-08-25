from __future__ import annotations

import unittest
from pathlib import Path


WORKFLOW = Path(__file__).parents[1] / ".github" / "workflows" / "tests.yml"


class CiWorkflowContractTests(unittest.TestCase):
    def test_ci_covers_all_pushes_pull_requests_and_supported_python_versions(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("  push:\n  pull_request:\n", workflow)
        self.assertIn('python-version: ["3.10", "3.11", "3.12", "3.13"]', workflow)

    def test_ci_has_a_separate_clean_install_smoke_job(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("  smoke:\n", workflow)
        self.assertIn("tests.test_clean_install_e2e_smoke", workflow)


if __name__ == "__main__":
    unittest.main()
