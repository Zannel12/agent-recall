from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class MigrationPolicyTests(unittest.TestCase):
    def test_public_policy_matches_adr_and_records_the_implemented_local_rename(self):
        policy = (ROOT / "docs" / "migration-and-deprecation.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("local ADR-0002 package/import/console migration is implemented", policy)
        self.assertIn("Cited Vault Recall", policy)
        self.assertIn("cited-vault-recall", policy)
        self.assertIn("must not be published", policy)
        self.assertIn("no compatibility alias", policy)
        self.assertIn("new protocol directory/version", policy)
        self.assertIn("migration-and-deprecation", readme)

    def test_policy_keeps_current_contracts_explicit_and_bounded(self):
        policy = (ROOT / "docs" / "migration-and-deprecation.md").read_text(encoding="utf-8")

        self.assertIn("cited-vault-recall <vault> <query>", policy)
        self.assertIn("cited-vault-recall-mcp --vault <vault>", policy)
        self.assertIn("SearchHit", policy)
        self.assertIn("render_packet", policy)
        self.assertIn("search_vault", policy)
        self.assertIn("no release, tag, publication", policy)


if __name__ == "__main__":
    unittest.main()
