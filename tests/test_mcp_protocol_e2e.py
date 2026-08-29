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
                [sys.executable, "-m", "cited_vault_recall.mcp", "--vault", str(vault)],
                cwd=ROOT,
                env=ENVIRONMENT,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                initialize = self._request(
                    server,
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2025-06-18",
                            "capabilities": {},
                            "clientInfo": {"name": "synthetic-client", "version": "1.0"},
                        },
                    },
                )
                self.assertEqual("2025-06-18", initialize["result"]["protocolVersion"])
                self.assertEqual({"tools": {}}, initialize["result"]["capabilities"])
                self._notify(server, {"jsonrpc": "2.0", "method": "notifications/initialized"})
                listing = self._request(server, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
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
                payload = json.loads(search["result"]["content"][0]["text"])
                hit = payload["hits"][0]
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

    def _notify(self, server: subprocess.Popen[str], notification: dict[str, object]) -> None:
        assert server.stdin is not None
        server.stdin.write(json.dumps(notification) + "\n")
        server.stdin.flush()

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
