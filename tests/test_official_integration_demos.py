from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DEMO = ROOT / "examples" / "official-integration-demos.py"
ENVIRONMENT = {**os.environ, "PYTHONPATH": "src"}


class OfficialIntegrationDemosTests(unittest.TestCase):
    def test_synthetic_cli_mcp_and_hermes_plan_demos_have_expected_results(self):
        result = subprocess.run(
            [sys.executable, str(DEMO)],
            cwd=ROOT,
            env=ENVIRONMENT,
            text=True,
            capture_output=True,
            timeout=20,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            {
                "cli": {"query": "privacy", "relative_path": "privacy.md"},
                "mcp": {"tools": ["search"], "query": "privacy", "relative_path": "privacy.md"},
                "hermes_plan": {"status": "ready", "configuration_plan_only": True, "commands_emitted": 4},
            },
            payload,
        )
        self.assertNotIn(str(ROOT), result.stdout)

    def test_public_docs_link_the_demo_and_label_hermes_as_non_executing(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        brief = (ROOT / "examples" / "agent-brief.md").read_text(encoding="utf-8")

        self.assertIn("official-integration-demos.py", readme)
        self.assertIn("official-integration-demos.py", brief)
        self.assertIn("configuration-plan-only", readme)
        self.assertIn("configuration-plan-only", brief)


if __name__ == "__main__":
    unittest.main()
