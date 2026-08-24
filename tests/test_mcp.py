from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from agent_recall.mcp import McpSearch, handle_request, serve, tools_list


class McpContractTests(unittest.TestCase):
    def test_stdio_runner_emits_one_json_rpc_response_per_line(self):
        incoming = io.StringIO(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}) + "\n")
        outgoing = io.StringIO()
        serve(McpSearch(Path(".")), incoming, outgoing)
        self.assertEqual(1, json.loads(outgoing.getvalue())["id"])

    def test_json_rpc_tools_list_is_the_only_advertised_capability(self):
        response = handle_request(McpSearch(Path(".")), {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        self.assertEqual(1, response["id"])
        self.assertEqual(["search"], [tool["name"] for tool in response["result"]["tools"]])

    def test_bound_search_returns_relative_citation_without_caller_vault(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text("# Privacy\nlocal only retrieval", encoding="utf-8")
            response = McpSearch(vault).call({"query": "privacy"})
            self.assertEqual("privacy", response["query"])
            self.assertEqual("privacy.md", response["hits"][0]["relative_path"])

    def test_tools_list_advertises_only_closed_search_tool(self):
        response = tools_list()
        self.assertEqual(["search"], [tool["name"] for tool in response["tools"]])
        schema = response["tools"][0]["inputSchema"]
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual({"query"}, set(schema["required"]))


if __name__ == "__main__":
    unittest.main()
