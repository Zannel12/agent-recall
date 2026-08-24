import json
import tempfile
import unittest
from pathlib import Path

from agent_recall.core import normalize_text, render_packet, search_vault


class SearchVaultTests(unittest.TestCase):
    def test_normalize_text_uses_nfc_and_casefold(self):
        self.assertEqual("café strasse", normalize_text("Cafe\u0301 STRAẞE"))

    def test_search_matches_decomposed_query_against_composed_source(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "cafe.md").write_text(
                "# Café\n\nThe source uses composed Unicode text.\n",
                encoding="utf-8",
            )

            hits = search_vault(vault, "Cafe\u0301", limit=1)

            self.assertEqual(["cafe.md"], [hit.relative_path for hit in hits])

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

    def test_search_exposes_bm25_and_explicit_boost_components(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "notes").mkdir()
            (vault / "notes" / "retrieval-guide.md").write_text(
                "# Retrieval Guide\n\nSparse retrieval returns cited local sources.\n",
                encoding="utf-8",
            )
            (vault / "notes" / "background.md").write_text(
                "# Background\n\nThis note mentions retrieval once.\n",
                encoding="utf-8",
            )

            hit = search_vault(vault, "retrieval", limit=1)[0]

            self.assertEqual("notes/retrieval-guide.md", hit.relative_path)
            self.assertEqual({"bm25", "title_boost", "path_boost"}, set(hit.score_components))
            self.assertGreater(hit.score_components["bm25"], 0)
            self.assertGreater(hit.score_components["title_boost"], 0)
            self.assertGreater(hit.score_components["path_boost"], 0)
            self.assertAlmostEqual(hit.score, sum(hit.score_components.values()))

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
            self.assertIn("- Score details: bm25=", packet)
            self.assertIn("Keep the vault local", packet)
            self.assertNotIn(str(vault), packet)


if __name__ == "__main__":
    unittest.main()
