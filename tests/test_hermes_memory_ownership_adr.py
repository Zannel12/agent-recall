from __future__ import annotations

import unittest
from pathlib import Path


class HermesMemoryOwnershipAdrTests(unittest.TestCase):
    def test_adr_declares_separate_authority_and_non_automation_rules(self):
        adr = Path(__file__).parents[1] / "docs" / "adr" / "0004-hermes-memory-provider-boundaries.md"
        text = adr.read_text(encoding="utf-8")

        for required in (
            "Status:** accepted",
            "Agent Recall is not a Hermes memory provider",
            "selected Markdown vault remains authoritative",
            "Built-in Hermes memory remains a compact profile and routing layer",
            "External provider is non-authoritative for Agent Recall",
            "do not synchronize",
            "do not merge",
            "explicit user approval",
            "No Hermes configuration is changed by this ADR",
            "not configure a provider",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
