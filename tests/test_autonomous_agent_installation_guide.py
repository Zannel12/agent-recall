from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
GUIDE = ROOT / "docs" / "autonomous-agent-installation.md"


class AutonomousAgentInstallationGuideTests(unittest.TestCase):
    def test_standalone_guide_has_safe_install_run_and_boundary_contract(self):
        self.assertTrue(GUIDE.is_file())
        guide = GUIDE.read_text(encoding="utf-8")

        for required in (
            "Python 3.10+",
            "python -m pip install --no-deps .",
            "agent-recall doctor --vault /absolute/path/to/markdown-vault --json",
            "agent-recall /absolute/path/to/markdown-vault",
            "agent-recall-mcp --vault /absolute/path/to/markdown-vault",
            "untrusted data, not instructions",
            "No network access",
            "No automatic vault writes",
            "Do not configure a host automatically",
            "No credentials",
        ):
            self.assertIn(required, guide)

    def test_readme_links_the_standalone_guide(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/autonomous-agent-installation.md", readme)


if __name__ == "__main__":
    unittest.main()
