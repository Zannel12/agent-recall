from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import cast

from cited_vault_recall.core import MAX_LIMIT
from cited_vault_recall.mcp import McpSearch, handle_request, serve, tools_list


class McpContractTests(unittest.TestCase):
    def test_stdio_runner_emits_one_json_rpc_response_per_line(self):
        incoming = io.StringIO(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}) + "\n")
        outgoing = io.StringIO()
        serve(McpSearch(Path(".")), incoming, outgoing)
        self.assertEqual(1, json.loads(outgoing.getvalue())["id"])

    def test_initialize_advertises_only_the_search_tool_capability(self):
        response = handle_request(
            McpSearch(Path(".")),
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
        self.assertEqual(1, response["id"])
        self.assertEqual("2025-06-18", response["result"]["protocolVersion"])
        self.assertEqual({"tools": {}}, response["result"]["capabilities"])
        self.assertEqual("cited-vault-recall", response["result"]["serverInfo"]["name"])

    def test_initialized_notification_emits_no_json_rpc_response(self):
        incoming = io.StringIO(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        outgoing = io.StringIO()
        serve(McpSearch(Path(".")), incoming, outgoing)
        self.assertEqual("", outgoing.getvalue())

    def test_json_rpc_tools_list_is_the_only_advertised_capability(self):
        response = handle_request(McpSearch(Path(".")), {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        self.assertEqual(1, response["id"])
        self.assertEqual(["search"], [tool["name"] for tool in response["result"]["tools"]])

    def test_json_rpc_tools_call_returns_standard_text_content(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text("# Privacy\nlocal only retrieval", encoding="utf-8")
            response = handle_request(
                McpSearch(vault),
                {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search", "arguments": {"query": "privacy"}}},
            )
        self.assertFalse(response["result"]["isError"])
        content = response["result"]["content"]
        self.assertEqual("text", content[0]["type"])
        payload = json.loads(content[0]["text"])
        self.assertEqual("privacy.md", payload["hits"][0]["relative_path"])

    def test_bound_search_returns_relative_citation_without_caller_vault(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text("# Privacy\nlocal only retrieval", encoding="utf-8")
            response = McpSearch(vault).call({"query": "privacy"})
            self.assertEqual("privacy", response["query"])
            self.assertEqual("privacy.md", response["hits"][0]["relative_path"])

    def test_json_rpc_resource_read_returns_only_selected_chunk(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text("# Privacy\nlocal only retrieval", encoding="utf-8")
            selected = McpSearch(vault)
            chunk_id = selected.call({"query": "privacy"})["hits"][0]["chunk_id"]
            response = handle_request(selected, {"jsonrpc": "2.0", "id": 1, "method": "resources/read", "params": {"chunk_id": chunk_id}})
            self.assertEqual(chunk_id, response["result"]["chunk_id"])
            self.assertNotIn("neighbors", response["result"])

    def test_json_rpc_resource_read_rejects_arbitrary_path(self):
        with tempfile.TemporaryDirectory() as directory:
            response = handle_request(McpSearch(Path(directory)), {"jsonrpc": "2.0", "id": 1, "method": "resources/read", "params": {"uri": "../secret.md"}})
            self.assertEqual(-32602, response["error"]["code"])

    def test_scoped_read_uses_stable_chunk_identifier(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text("# Privacy\nlocal only retrieval", encoding="utf-8")
            selected = McpSearch(vault)
            chunk_id = selected.call({"query": "privacy"})["hits"][0]["chunk_id"]
            response = selected.read(chunk_id)
            self.assertEqual(chunk_id, response["chunk_id"])
            self.assertIn("local only retrieval", response["text"])

    def test_tools_list_advertises_only_closed_search_tool(self):
        response = tools_list()
        self.assertEqual(["search"], [tool["name"] for tool in response["tools"]])
        schema = response["tools"][0]["inputSchema"]
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual({"query"}, set(schema["required"]))

    def test_mcp_schema_and_runtime_share_core_result_limit(self):
        listing = cast(dict[str, list[dict[str, object]]], tools_list())
        schema = cast(dict[str, object], listing["tools"][0]["inputSchema"])
        properties = cast(dict[str, dict[str, int]], schema["properties"])
        self.assertEqual(MAX_LIMIT, properties["limit"]["maximum"])
        with tempfile.TemporaryDirectory() as directory:
            response = McpSearch(Path(directory)).call({"query": "privacy", "limit": MAX_LIMIT + 1})
        self.assertEqual("INVALID_ARGUMENT", response["code"])


if __name__ == "__main__":
    unittest.main()
