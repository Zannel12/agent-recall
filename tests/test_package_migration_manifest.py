from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PackageMigrationManifestTests(unittest.TestCase):
    def test_manifest_accounts_for_every_identity_surface_before_a_rename(self):
        manifest = ROOT / "docs" / "package-migration-manifest.md"
        text = manifest.read_text(encoding="utf-8")

        self.assertIn("## Current identity", text)
        self.assertIn("## Future target", text)
        self.assertIn("## Migration inventory", text)
        self.assertIn("## Deliberate non-actions", text)
        for required in (
            "`agent-recall`",
            "`agent_recall`",
            "`cited-vault-recall`",
            "`cited_vault_recall`",
            "`cited-vault-recall-mcp`",
            "`pyproject.toml`",
            "`src/agent_recall/`",
            "`tests/`",
            "`docs/`",
            "`.github/workflows/tests.yml`",
            "`protocol/v1/*.schema.json`",
        ):
            self.assertIn(required, text)

    def test_manifest_preserves_local_only_boundaries_and_defers_external_actions(self):
        text = (ROOT / "docs" / "package-migration-manifest.md").read_text(encoding="utf-8")

        self.assertIn("no registry lookup", text)
        self.assertIn("no package publication", text)
        self.assertIn("no GitHub repository rename", text)
        self.assertIn("no Git tag or GitHub Release", text)
        self.assertIn("no compatibility alias", text)
        self.assertIn("No real vault, host configuration, or credential", text)


if __name__ == "__main__":
    unittest.main()
