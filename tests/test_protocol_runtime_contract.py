from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from cited_vault_recall.cli import main
from cited_vault_recall.mcp import McpSearch


ROOT = Path(__file__).parents[1]


class ProtocolRuntimeContractTests(unittest.TestCase):
    def test_cli_and_mcp_search_emit_the_same_versioned_source_provenance_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text("# Privacy\n\nLocal privacy boundary.\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(0, main([str(vault), "privacy", "--format", "json"]))
            cli_payload = json.loads(output.getvalue())
            mcp_payload = McpSearch(vault).call({"query": "privacy", "limit": 1})

            self.assertEqual("1.0", cli_payload["schema_version"])
            self.assertEqual(cli_payload, mcp_payload)
            self.assertEqual({"schema_version", "query", "hits", "diagnostics"}, set(cli_payload))
            hit = cli_payload["hits"][0]
            self.assertEqual(
                {"source_id", "relative_path", "chunk_id", "excerpt", "score", "score_components", "title", "heading"},
                set(hit),
            )
            self.assertEqual("privacy.md", hit["source_id"])
            self.assertEqual(hit["source_id"], hit["relative_path"])
            self.assertNotIn(str(vault), json.dumps(cli_payload))

    def test_protocol_schema_matches_the_runtime_search_envelope(self):
        schema = json.loads((ROOT / "protocol" / "v1" / "citation.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {"source_id", "relative_path", "chunk_id", "excerpt", "score", "score_components", "title", "heading"},
            set(schema["required"]),
        )


if __name__ == "__main__":
    unittest.main()
