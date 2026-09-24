from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    def test_readiness_matrix_distinguishes_current_evidence_from_future_actions(self):
        document = ROOT / "docs" / "release-readiness.md"
        text = document.read_text(encoding="utf-8")

        self.assertIn("## Current readiness", text)
        self.assertIn("## Future external-action gates", text)
        self.assertIn("GitHub Release `v0.2.0` | `READY`", text)
        self.assertIn("PyPI publication | `BLOCKED`", text)
        self.assertIn("Trusted Publisher and a reviewed manual-only OIDC workflow are configured", text)
        self.assertIn("fresh explicit approval before dispatch", text)
        self.assertIn("Hosted production deployment | `BLOCKED`", text)
        self.assertIn("Semantic/vector decision gate | `READY`", text)
        self.assertIn("provenance", text)

    def test_readiness_matrix_prohibits_implicit_future_publication_or_deployment(self):
        text = (ROOT / "docs" / "release-readiness.md").read_text(encoding="utf-8")

        self.assertIn("PyPI Trusted Publisher", text)
        self.assertIn("one action per Goal turn", text)
        self.assertIn("no credentials in chat", text)
        self.assertIn("does not create a tag, release, publication, deployment, SBOM, or attestation", text)
        self.assertIn("Do not treat distribution publication as service deployment", text)


if __name__ == "__main__":
    unittest.main()
