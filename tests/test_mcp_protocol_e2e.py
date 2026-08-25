from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]
ENVIRONMENT = {**os.environ, "PYTHONPATH": "src"}


class McpProtocolEndToEndTests(unittest.TestCase):
    def test_synthetic_stdio_handshake_tools_search_and_scoped_read(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory) / "demo-vault"
            vault.mkdir()
            (vault / "privacy.md").write_text("# Privacy\n\nLocal retrieval is read-only.", encoding="utf-8")
            server = subprocess.Popen(
                [sys.executable, "-m", "agent_recall.mcp", "--vault", str(vault)],
                cwd=ROOT,
                env=ENVIRONMENT,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                listing = self._request(server, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
                self.assertEqual(["search"], [tool["name"] for tool in listing["result"]["tools"]])
                search = self._request(
                    server,
                    {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/call",
                        "params": {"name": "search", "arguments": {"query": "privacy", "limit": 1}},
                    },
                )
                hit = search["result"]["hits"][0]
                self.assertEqual("privacy.md", hit["relative_path"])
                self.assertNotIn(str(vault), json.dumps(search))
                read = self._request(
                    server,
                    {"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"chunk_id": hit["chunk_id"]}},
                )
                self.assertEqual(hit["chunk_id"], read["result"]["chunk_id"])
                self.assertEqual("privacy.md", read["result"]["relative_path"])
            finally:
                server.terminate()
                server.wait(timeout=10)
                assert server.stdin is not None
                assert server.stdout is not None
                assert server.stderr is not None
                server.stdin.close()
                server.stdout.close()
                server.stderr.close()

    def _request(self, server: subprocess.Popen[str], request: dict[str, object]) -> dict[str, Any]:
        assert server.stdin is not None
        assert server.stdout is not None
        server.stdin.write(json.dumps(request) + "\n")
        server.stdin.flush()
        response = server.stdout.readline()
        self.assertTrue(response, "MCP server exited without a response")
        return json.loads(response)


if __name__ == "__main__":
    unittest.main()
