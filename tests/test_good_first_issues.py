from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class GoodFirstIssuesTests(unittest.TestCase):
    def test_backlog_lists_current_small_contributor_tasks_with_boundaries(self):
        document = (ROOT / "docs" / "good-first-issues.md").read_text(encoding="utf-8")

        for heading in (
            "Add a checked-in Markdown link contract",
            "Add an unreadable-vault doctor remediation",
            "Document PowerShell explicit-vault setup",
            "Add a synthetic paraphrase evaluation fixture",
        ):
            self.assertIn(heading, document)
        for required_boundary in (
            "No real vault",
            "No network",
            "No model download",
            "Do not create GitHub issues",
        ):
            self.assertIn(required_boundary, document)

    def test_backlog_is_linked_from_public_contributor_documents(self):
        for path in (ROOT / "README.md", ROOT / "CONTRIBUTING.md"):
            self.assertIn("docs/good-first-issues.md", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
