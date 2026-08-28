from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
POLICY = ROOT / "docs" / "production-evidence.md"


class ProductionEvidencePolicyTests(unittest.TestCase):
    def test_policy_requires_all_evidence_dimensions_before_any_production_claim(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "Owner",
            "Environment",
            "Rollback",
            "Privacy boundary",
            "Observability",
            "Evidence retention",
            "fresh explicit user approval",
            "synthetic",
            "not a deployment",
            "not proof of production",
        ):
            self.assertIn(required, text)

    def test_policy_rejects_unsupported_production_evidence_and_preserves_local_first_default(self):
        text = POLICY.read_text(encoding="utf-8")
        compatibility = (ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8")
        readiness = (ROOT / "docs" / "release-readiness.md").read_text(encoding="utf-8")

        self.assertIn("Reject as insufficient", text)
        self.assertIn("documentation-only", text)
        self.assertIn("No target is selected", text)
        self.assertIn("local-first", text)
        self.assertIn("No row currently reaches this level", compatibility)
        self.assertIn("production deployment evidence | `BLOCKED`", readiness)


if __name__ == "__main__":
    unittest.main()
