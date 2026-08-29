from __future__ import annotations

import unittest
from pathlib import Path


class CompatibilityMatrixTests(unittest.TestCase):
    def test_matrix_declares_all_hosts_boundaries_and_evidence_status(self):
        matrix = Path(__file__).parents[1] / "docs" / "compatibility.md"
        text = matrix.read_text(encoding="utf-8")

        for host in ("Codex", "Claude Code", "Cursor", "Hermes", "OpenClaw", "CLI fallback"):
            self.assertIn(host, text)
        for field in ("Supported mode", "Data location", "Permission surface", "Evidence level", "Host version / source checked", "Test status"):
            self.assertIn(field, text)
        self.assertEqual(4, text.count("Not integration-tested"))
        self.assertIn("Integration-tested", text)
        self.assertIn("Real Hermes synthetic-vault MCP invocation passed", text)
        self.assertIn("Hermes Agent v0.20.5", text)
        self.assertIn("Local tests only", text)
        self.assertIn("https://developers.openai.com/codex/mcp", text)
        self.assertIn("https://code.claude.com/docs/en/mcp-quickstart", text)
        self.assertIn("https://cursor.com/docs/mcp", text)
        self.assertIn("https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes", text)
        self.assertIn("https://docs.openclaw.ai/cli/mcp", text)
        self.assertIn("Only Hermes has direct synthetic-host evidence", text)


if __name__ == "__main__":
    unittest.main()
