from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ReleaseStateTests(unittest.TestCase):
    def test_published_020_metadata_docs_and_changelog_are_consistent(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readiness = (ROOT / "docs" / "release-readiness.md").read_text(encoding="utf-8")
        mcp = (ROOT / "src" / "cited_vault_recall" / "mcp.py").read_text(encoding="utf-8")

        self.assertIn('version = "0.2.0"', pyproject)
        self.assertIn('SERVER_VERSION = "0.2.0"', mcp)
        self.assertIn("## [0.2.0] — 2026-08-29", changelog)
        self.assertIn("GitHub Release [`v0.2.0`](https://github.com/Zannel12/agent-recall/releases/tag/v0.2.0) is published", changelog)
        self.assertIn("`0.2.0` is the current published GitHub Release package version", readme)
        self.assertIn("PyPI publication remains pending", readme)
        self.assertIn("GitHub Release `v0.2.0` is published", readiness)
        self.assertIn("PyPI publication | `BLOCKED`", readiness)
        current_notes = changelog.split("## [0.1.0]", 1)[0]
        self.assertIn("All notable changes to Cited Vault Recall", changelog)
        self.assertIn("`cited-vault-recall-mcp --vault <vault>`", current_notes)
        self.assertIn("`cited-vault-recall <vault> <query>`", current_notes)
        self.assertIn("Integration-tested", current_notes)
        self.assertNotIn("`agent-recall-mcp --vault <vault>`", current_notes)
        self.assertNotIn("`agent-recall <vault> <query>`", current_notes)
        self.assertNotIn("Release candidate, untagged", current_notes)
        self.assertNotIn("No GitHub Release or tag", current_notes)
        self.assertIn("earlier `0.2.0.dev0` artifacts", changelog)


if __name__ == "__main__":
    unittest.main()
