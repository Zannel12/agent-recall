#!/usr/bin/env python3
"""Run synthetic expected-result CLI, MCP, and Hermes-plan integration demos."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]
DEMO_VAULT = ROOT / "examples" / "demo-vault"
ENVIRONMENT = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def _request(server: subprocess.Popen[str], request: dict[str, object]) -> dict[str, Any]:
    assert server.stdin is not None
    assert server.stdout is not None
    server.stdin.write(json.dumps(request) + "\n")
    server.stdin.flush()
    response = server.stdout.readline()
    if not response:
        raise RuntimeError("Synthetic MCP demo server exited without a response")
    return json.loads(response)


def cli_demo() -> dict[str, str]:
    result = subprocess.run(
        [sys.executable, "-m", "agent_recall.cli", str(DEMO_VAULT), "privacy", "--format", "json"],
        cwd=ROOT,
        env=ENVIRONMENT,
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    payload = json.loads(result.stdout)
    return {"query": payload["query"], "relative_path": payload["hits"][0]["relative_path"]}


def mcp_demo() -> dict[str, object]:
    server = subprocess.Popen(
        [sys.executable, "-m", "agent_recall.mcp", "--vault", str(DEMO_VAULT)],
        cwd=ROOT,
        env=ENVIRONMENT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        listing = _request(server, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        search = _request(
            server,
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search", "arguments": {"query": "privacy", "limit": 1}}},
        )
        return {
            "tools": [tool["name"] for tool in listing["result"]["tools"]],
            "query": search["result"]["query"],
            "relative_path": search["result"]["hits"][0]["relative_path"],
        }
    finally:
        server.terminate()
        server.wait(timeout=10)
        assert server.stdin is not None
        assert server.stdout is not None
        assert server.stderr is not None
        server.stdin.close()
        server.stdout.close()
        server.stderr.close()


def hermes_plan_demo() -> dict[str, object]:
    from agent_recall.hermes_adapter import build_hermes_mcp_plan

    plan = build_hermes_mcp_plan(
        config_path=Path("/synthetic/hermes-config.yaml"),
        backup_path=Path("/synthetic/hermes-config.yaml.agent-recall.bak"),
        vault_path=Path("/synthetic/demo-vault"),
        observed_server_names=set(),
        config_exists=True,
        consent=True,
    )
    return {"status": plan.status.value, "configuration_plan_only": True, "commands_emitted": len(plan.commands)}


def main() -> int:
    print(json.dumps({"cli": cli_demo(), "mcp": mcp_demo(), "hermes_plan": hermes_plan_demo()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
