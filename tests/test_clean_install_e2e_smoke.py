from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]


class CleanInstallEndToEndSmokeTests(unittest.TestCase):
    def test_clean_clone_editable_install_cli_doctor_and_mcp_search(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            clone = workspace / "cited-vault-recall"
            venv = workspace / "venv"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "*.egg-info", "__pycache__"))
            subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, text=True)
            python = venv / "bin" / "python"
            commands = venv / "bin"
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-deps", "-e", str(clone)],
                check=True,
                capture_output=True,
                text=True,
            )
            vault = clone / "examples" / "demo-vault"

            cli = subprocess.run(
                [str(commands / "cited-vault-recall"), str(vault), "privacy", "--format", "json"],
                check=True,
                capture_output=True,
                text=True,
            )
            packet = json.loads(cli.stdout)
            hits = packet["hits"]
            self.assertTrue(hits)
            self.assertTrue(all(hit["relative_path"] == "privacy.md" for hit in hits))
            self.assertNotIn(str(vault), cli.stdout)

            doctor = subprocess.run(
                [str(commands / "cited-vault-recall"), "doctor", "--vault", str(vault), "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            doctor_payload = json.loads(doctor.stdout)
            self.assertTrue(doctor_payload["install"]["ok"])
            self.assertTrue(doctor_payload["vault"]["accessible"])

            server = subprocess.Popen(
                [str(commands / "cited-vault-recall-mcp"), "--vault", str(vault)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                listing = self._request(server, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
                tools = listing["result"]["tools"]
                self.assertEqual(["search"], [tool["name"] for tool in tools])
                searched = self._request(
                    server,
                    {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/call",
                        "params": {"name": "search", "arguments": {"query": "privacy", "limit": 1}},
                    },
                )
                result = searched["result"]
                self.assertEqual("privacy", result["query"])
                self.assertEqual("privacy.md", result["hits"][0]["relative_path"])
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
