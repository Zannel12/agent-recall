from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TextIO

from .core import MAX_LIMIT, RecallError, error_payload, follow_evidence, search_response_payload, search_vault


SERVER_NAME = "cited-vault-recall"
SERVER_VERSION = "0.2.0"


class McpSearch:
    """A search-only adapter permanently bound to one explicit vault."""

    def __init__(self, vault: Path) -> None:
        self._vault = vault

    def read(self, chunk_id: str) -> dict[str, object]:
        try:
            chunks = follow_evidence(self._vault, chunk_id, neighbor_limit=0)
        except (RecallError, ValueError):
            return error_payload("INVALID_EVIDENCE_ID", "Evidence is unavailable.")
        chunk = chunks[0]
        return {"schema_version": "1.0", "chunk_id": chunk.chunk_id, "relative_path": chunk.relative_path, "text": chunk.body}

    def call(self, arguments: dict[str, object]) -> dict[str, object]:
        if set(arguments) - {"query", "limit"} or not isinstance(arguments.get("query"), str):
            return error_payload("INVALID_ARGUMENT", "Invalid search arguments.")
        limit = arguments.get("limit", 8)
        if not isinstance(limit, int):
            return error_payload("INVALID_ARGUMENT", "Invalid search arguments.")
        diagnostics: dict[str, int] = {}
        try:
            hits = search_vault(self._vault, arguments["query"], limit, diagnostics)
        except (RecallError, ValueError) as error:
            code = error.code if isinstance(error, RecallError) else "INVALID_ARGUMENT"
            return error_payload(code, "Search request rejected.")
        return search_response_payload(str(arguments["query"]), hits, diagnostics)


def serve(search: McpSearch, incoming: TextIO, outgoing: TextIO) -> None:
    """Serve newline-delimited JSON-RPC over caller-provided stdio streams."""
    for line in incoming:
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            response: dict[str, object] | None = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            response = handle_request(search, request) if isinstance(request, dict) else {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        if response is not None:
            outgoing.write(json.dumps(response, sort_keys=True) + "\n")
            outgoing.flush()


def handle_request(search: McpSearch, request: dict[str, object]) -> dict[str, object] | None:
    request_id = request.get("id")
    if request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32600, "message": "Invalid Request"}}
    if request["method"] == "initialize":
        params = request.get("params")
        if not isinstance(params, dict) or not isinstance(params.get("protocolVersion"), str) or not params["protocolVersion"]:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": "Invalid params"}}
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": params["protocolVersion"],
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        }
    if request["method"] == "notifications/initialized" and "id" not in request:
        return None
    if request["method"] == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": tools_list()}
    if request["method"] == "resources/read":
        params = request.get("params")
        if not isinstance(params, dict) or set(params) != {"chunk_id"} or not isinstance(params.get("chunk_id"), str):
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": "Invalid params"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": search.read(params["chunk_id"])}
    if request["method"] == "tools/call":
        params = request.get("params")
        if not isinstance(params, dict) or params.get("name") != "search" or not isinstance(params.get("arguments"), dict):
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": "Invalid params"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": tool_result(search.call(params["arguments"]))}
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found"}}


def tool_result(payload: dict[str, object]) -> dict[str, object]:
    """Encode a bounded search response in the MCP ToolResult content envelope."""
    return {
        "content": [{"type": "text", "text": json.dumps(payload, sort_keys=True)}],
        "isError": "code" in payload,
    }


def tools_list() -> dict[str, object]:
    """Return the only capability exposed by the local stdio prototype."""
    return {
        "tools": [
            {
                "name": "search",
                "description": "Search the explicitly configured local Markdown vault.",
                "inputSchema": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string", "minLength": 1, "maxLength": 4096},
                        "limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIMIT},
                    },
                },
            }
        ]
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Cited Vault Recall MCP search over stdio.")
    parser.add_argument("--vault", required=True, type=Path, help="Explicit local Markdown vault")
    args = parser.parse_args(argv)
    if not args.vault.is_dir():
        parser.error("INVALID_ARGUMENT: selected vault is unavailable")
    serve(McpSearch(args.vault), sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
