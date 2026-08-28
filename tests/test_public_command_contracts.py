from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PUBLIC_COMMAND_DOCS = (
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "examples" / "agent-brief.md",
    ROOT / "docs" / "compatibility.md",
    ROOT / "docs" / "hermes-mcp-adapter-plan.md",
)


class PublicCommandContractTests(unittest.TestCase):
    def test_public_docs_do_not_advertise_removed_search_subcommand(self):
        for path in PUBLIC_COMMAND_DOCS:
            self.assertNotIn("cited-vault-recall search", path.read_text(encoding="utf-8"), path)

    def test_public_docs_describe_canonical_cli_and_mcp_forms(self):
        compatibility = (ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8")
        hermes_plan = (ROOT / "docs" / "hermes-mcp-adapter-plan.md").read_text(encoding="utf-8")
        self.assertIn("cited-vault-recall <vault> <query>", compatibility)
        self.assertIn("cited-vault-recall-mcp --vault <vault>", compatibility)
        self.assertIn("cited-vault-recall <caller-selected-vault> <query> --format json", hermes_plan)


if __name__ == "__main__":
    unittest.main()
