from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class HermesIntegrationEvidenceTests(unittest.TestCase):
    def test_required_synthetic_protocol_e2e_is_a_separate_test_artifact(self):
        protocol_test = ROOT / "tests" / "test_mcp_protocol_e2e.py"
        self.assertTrue(protocol_test.is_file())
        self.assertIn("tools/list", protocol_test.read_text(encoding="utf-8"))
        self.assertIn("resources/read", protocol_test.read_text(encoding="utf-8"))

    def test_docs_distinguish_required_synthetic_evidence_from_manual_hermes_evidence(self):
        plan = (ROOT / "docs" / "hermes-mcp-adapter-plan.md").read_text(encoding="utf-8")
        matrix = (ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8")

        self.assertIn("Synthetic MCP protocol E2E (required)", plan)
        self.assertIn("Real Hermes verification (manual opt-in)", plan)
        self.assertIn("No real Hermes host was configured or connected", plan)
        self.assertIn("Synthetic MCP protocol E2E", matrix)
        self.assertIn("Real Hermes synthetic-vault MCP invocation passed", matrix)
    def test_documented_real_hermes_synthetic_smoke_is_bounded_and_not_production_evidence(self):
        evidence = (ROOT / "docs" / "hermes-integration-evidence.md").read_text(encoding="utf-8")

        for required in (
            "Integration-tested",
            "Hermes Agent v0.20.5",
            "privacy.md#privacy",
            "synthetic vault",
            "C3-cleanup",
            "not Production-tested",
        ):
            self.assertIn(required, evidence)
        self.assertNotIn("/home/hermes", evidence)


if __name__ == "__main__":
    unittest.main()
