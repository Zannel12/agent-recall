from __future__ import annotations

import unittest
from pathlib import Path


class AdapterPortfolioAdrTests(unittest.TestCase):
    def test_adr_selects_only_hermes_stdio_mcp_and_defers_other_surfaces(self):
        adr = Path(__file__).parents[1] / "docs" / "adr" / "0005-hermes-adapter-portfolio.md"
        text = adr.read_text(encoding="utf-8")

        for required in (
            "Status:** accepted",
            "Hermes local stdio MCP is the sole selected next host surface",
            "Native provider: not selected",
            "Hooks: not selected",
            "Skills: not selected",
            "Other hosts: deferred",
            "No Hermes configuration is changed by this ADR",
            "does not install dependencies",
            "does not start a server",
            "does not authenticate",
            "B05.4",
            "explicit user consent",
            "deterministic CLI fallback",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
