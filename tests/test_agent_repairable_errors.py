from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_recall.mcp import McpSearch


ROOT = Path(__file__).parents[1]
ENVIRONMENT = {**os.environ, "PYTHONPATH": "src"}


class AgentRepairableErrorTests(unittest.TestCase):
    def test_protocol_error_schema_requires_safe_machine_readable_next_step(self):
        schema = json.loads((ROOT / "protocol" / "v1" / "error.schema.json").read_text(encoding="utf-8"))

        self.assertEqual(
            {"schema_version", "code", "message", "next_step", "retryable"},
            set(schema["required"]),
        )
        self.assertEqual(
            {"CHECK_ARGUMENTS", "CHECK_EXPLICIT_VAULT", "SEARCH_AGAIN"},
            set(schema["properties"]["next_step"]["enum"]),
        )

    def test_json_cli_missing_vault_returns_closed_repairable_error_without_path_leak(self):
        missing = Path(tempfile.gettempdir()) / "agent-recall-private-repairable-vault"
        result = subprocess.run(
            [sys.executable, "-m", "agent_recall.cli", str(missing), "privacy", "--format", "json"],
            cwd=ROOT,
            env=ENVIRONMENT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            {
                "schema_version": "1.0",
                "code": "VAULT_NOT_FOUND",
                "message": "Selected vault directory is unavailable",
                "next_step": "CHECK_EXPLICIT_VAULT",
                "retryable": False,
            },
            payload,
        )
        self.assertNotIn(str(missing), result.stdout)

    def test_mcp_invalid_search_arguments_return_the_same_closed_error_shape(self):
        response = McpSearch(Path(".")).call({"query": "privacy", "limit": "not-an-int"})

        self.assertEqual(
            {
                "schema_version": "1.0",
                "code": "INVALID_ARGUMENT",
                "message": "Invalid search arguments.",
                "next_step": "CHECK_ARGUMENTS",
                "retryable": False,
            },
            response,
        )


if __name__ == "__main__":
    unittest.main()
