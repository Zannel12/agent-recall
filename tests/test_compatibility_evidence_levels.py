from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class CompatibilityEvidenceLevelsTests(unittest.TestCase):
    def test_matrix_defines_closed_evidence_levels_and_source_check_dates(self):
        text = (ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8")

        self.assertIn("## Evidence levels", text)
        for level in ("Documented", "Smoke-tested", "Integration-tested", "Production-tested"):
            self.assertIn(f"**{level}**", text)
        self.assertIn("Host version / source checked", text)
        self.assertEqual(5, text.count("version not recorded; docs checked 2026-08-28"))
        self.assertIn("smoke-tested", text.lower())
        self.assertNotIn("production-tested evidence exists", text.lower())

    def test_matrix_uses_current_verified_host_docs_and_keeps_host_claims_bounded(self):
        text = (ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8")

        self.assertIn("https://code.claude.com/docs/en/mcp-quickstart", text)
        self.assertIn("https://cursor.com/docs/mcp", text)
        self.assertIn("documentation-only host evidence", text)
        self.assertIn("No host was installed, configured, authenticated, or connected", text)


if __name__ == "__main__":
    unittest.main()
