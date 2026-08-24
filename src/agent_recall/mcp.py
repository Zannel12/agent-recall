from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TextIO

from .core import RecallError, search_vault


class McpSearch:
    """A search-only adapter permanently bound to one explicit vault."""

    def __init__(self, vault: Path) -> None:
        self._vault = vault

    def call(self, arguments: dict[str, object]) -> dict[str, object]:
        if set(arguments) - {"query", "limit"} or not isinstance(arguments.get("query"), str):
            return {"schema_version": "1.0", "code": "INVALID_ARGUMENT", "message": "Invalid search arguments."}
        limit = arguments.get("limit", 8)
        if not isinstance(limit, int):
            return {"schema_version": "1.0", "code": "INVALID_ARGUMENT", "message": "Invalid search arguments."}
        diagnostics: dict[str, int] = {}
        try:
            hits = search_vault(self._vault, arguments["query"], limit, diagnostics)
        except (RecallError, ValueError):
            return {"schema_version": "1.0", "code": "INVALID_ARGUMENT", "message": "Search request rejected."}
        return {"schema_version": "1.0", "query": arguments["query"], "hits": [hit.__dict__ for hit in hits], "diagnostics": diagnostics}


def serve(search: McpSearch, incoming: TextIO, outgoing: TextIO) -> None:
    """Serve newline-delimited JSON-RPC over caller-provided stdio streams."""
    for line in incoming:
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            response = handle_request(search, request) if isinstance(request, dict) else {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        outgoing.write(json.dumps(response, sort_keys=True) + "\n")
        outgoing.flush()


def handle_request(search: McpSearch, request: dict[str, object]) -> dict[str, object]:
    request_id = request.get("id")
    if request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32600, "message": "Invalid Request"}}
    if request["method"] == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": tools_list()}
    if request["method"] == "tools/call":
        params = request.get("params")
        if not isinstance(params, dict) or params.get("name") != "search" or not isinstance(params.get("arguments"), dict):
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": "Invalid params"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": search.call(params["arguments"])}
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found"}}

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
                        "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                    },
                },
            }
        ]
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Agent Recall MCP search over stdio.")
    parser.add_argument("--vault", required=True, type=Path, help="Explicit local Markdown vault")
    args = parser.parse_args(argv)
    if not args.vault.is_dir():
        parser.error("INVALID_ARGUMENT: selected vault is unavailable")
    serve(McpSearch(args.vault), sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
