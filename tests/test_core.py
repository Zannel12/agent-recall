import json
import tempfile
import unittest
from pathlib import Path

from agent_recall.core import render_packet, search_vault


class SearchVaultTests(unittest.TestCase):
    def test_search_ranks_title_match_and_keeps_relative_source_path(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "notes").mkdir()
            (vault / "notes" / "agent-memory.md").write_text(
                "# Agent Memory\n\nProgressive retrieval keeps AI context scoped and cited.\n",
                encoding="utf-8",
            )
            (vault / "notes" / "other.md").write_text(
                "# Other\n\nMemory is mentioned once.\n",
                encoding="utf-8",
            )

            hits = search_vault(vault, "agent memory", limit=2)

            self.assertEqual("notes/agent-memory.md", hits[0].relative_path)
            self.assertEqual("Agent Memory", hits[0].title)
            self.assertNotIn(str(vault), hits[0].relative_path)

    def test_packet_includes_query_relative_path_and_excerpt(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text(
                "# Privacy Model\n\nKeep the vault local and send only selected excerpts to an agent.\n",
                encoding="utf-8",
            )

            packet = render_packet("privacy", search_vault(vault, "privacy"))

            self.assertIn("# Librarian Context Packet — privacy", packet)
            self.assertIn("privacy.md", packet)
            self.assertIn("Keep the vault local", packet)
            self.assertNotIn(str(vault), packet)


if __name__ == "__main__":
    unittest.main()
