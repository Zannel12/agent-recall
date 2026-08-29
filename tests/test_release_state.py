from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ReleaseStateTests(unittest.TestCase):
    def test_untagged_020_candidate_metadata_docs_and_changelog_are_consistent(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        mcp = (ROOT / "src" / "cited_vault_recall" / "mcp.py").read_text(encoding="utf-8")

        self.assertIn('version = "0.2.0"', pyproject)
        self.assertIn('SERVER_VERSION = "0.2.0"', mcp)
        self.assertIn("## [0.2.0] — Release candidate, untagged", changelog)
        self.assertIn("Local stdio MCP", changelog)
        self.assertIn("Hermes", changelog)
        self.assertIn("`doctor`", changelog)
        self.assertIn("`0.2.0`", readme)
        self.assertIn("No GitHub Release or tag", readme)
        self.assertIn("untagged, unpublished release-candidate package version", readme)
        self.assertIn("earlier `0.2.0.dev0` artifacts", readme)
        self.assertIn("earlier `0.2.0.dev0` artifacts", changelog)


if __name__ == "__main__":
    unittest.main()
