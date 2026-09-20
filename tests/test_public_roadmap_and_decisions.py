from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PublicRoadmapAndDecisionsTests(unittest.TestCase):
    def test_roadmap_and_decision_register_state_current_priorities_and_boundaries(self):
        roadmap = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
        decisions = (ROOT / "docs" / "decisions.md").read_text(encoding="utf-8")

        for required in (
            "v0.2.0",
            "PyPI publication remains pending",
            "local-first",
            "No hosted deployment",
            "synthetic",
            "DEFER",
        ):
            self.assertIn(required, roadmap)

        for required in (
            "Sparse lexical retrieval",
            "DEFER",
            "No hosted deployment",
            "PyPI Trusted Publishing",
            "not a hosted production service",
        ):
            self.assertIn(required, decisions)

    def test_readme_and_contributing_link_to_public_roadmap_and_decisions(self):
        for document in (ROOT / "README.md", ROOT / "CONTRIBUTING.md"):
            text = document.read_text(encoding="utf-8")
            self.assertIn("docs/roadmap.md", text)
            self.assertIn("docs/decisions.md", text)


if __name__ == "__main__":
    unittest.main()
