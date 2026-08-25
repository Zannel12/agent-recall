from __future__ import annotations

import unittest
from pathlib import Path


class CompatibilityMatrixTests(unittest.TestCase):
    def test_matrix_declares_all_hosts_boundaries_and_evidence_status(self):
        matrix = Path(__file__).parents[1] / "docs" / "compatibility.md"
        text = matrix.read_text(encoding="utf-8")

        for host in ("Codex", "Claude Code", "Cursor", "Hermes", "OpenClaw", "CLI fallback"):
            self.assertIn(host, text)
        for field in ("Supported mode", "Data location", "Permission surface", "Test status"):
            self.assertIn(field, text)
        self.assertEqual(4, text.count("Not integration-tested"))
        self.assertIn("Synthetic MCP protocol E2E; real Hermes not integration-tested", text)
        self.assertIn("Local tests only", text)
        self.assertIn("https://developers.openai.com/codex/mcp", text)
        self.assertIn("https://docs.anthropic.com/en/docs/claude-code/mcp", text)
        self.assertIn("https://docs.cursor.com/en/guides/tutorials/building-mcp-server", text)
        self.assertIn("https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes", text)
        self.assertIn("https://docs.openclaw.ai/cli/mcp", text)
        self.assertIn("No host was installed, configured, authenticated, or connected", text)


if __name__ == "__main__":
    unittest.main()
