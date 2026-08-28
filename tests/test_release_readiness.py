from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    def test_readiness_matrix_separates_local_gates_from_final_user_approval_actions(self):
        document = ROOT / "docs" / "release-readiness.md"
        text = document.read_text(encoding="utf-8")

        self.assertIn("## Current readiness", text)
        self.assertIn("## Final approval gates", text)
        self.assertIn("`READY`", text)
        self.assertIn("`NOT_READY`", text)
        self.assertIn("`BLOCKED`", text)
        for action in (
            "dependency/action SHA pinning",
            "semantic/vector/LLM retrieval",
            "real Hermes integration",
            "real Codex / Claude Code / Cursor / OpenClaw integration",
            "production deployment evidence",
            "SBOM",
            "provenance attestation",
            "Git tag",
            "GitHub Release",
            "PyPI publication",
        ):
            self.assertIn(action, text)

    def test_readiness_matrix_prohibits_implicit_release_or_publication(self):
        text = (ROOT / "docs" / "release-readiness.md").read_text(encoding="utf-8")

        self.assertIn("registry availability is deliberately unknown", text)
        self.assertIn("no PyPI upload", text)
        self.assertIn("fresh explicit user approval", text)
        self.assertIn("one final action per Goal turn", text)
        self.assertIn("does not create a tag, release, publication, deployment, SBOM, or attestation", text)


if __name__ == "__main__":
    unittest.main()
