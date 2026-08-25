from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class CommunityFilesTests(unittest.TestCase):
    def test_public_contribution_surface_exists(self):
        expected = (
            "CODE_OF_CONDUCT.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
            ".github/pull_request_template.md",
        )
        for path in expected:
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
