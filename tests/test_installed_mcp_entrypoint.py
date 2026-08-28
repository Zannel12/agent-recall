from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DEMO_VAULT = ROOT / "examples" / "demo-vault"


class InstalledMcpEntrypointTests(unittest.TestCase):
    def test_editable_install_exports_mcp_console_script_that_serves_tools_list(self):
        with tempfile.TemporaryDirectory() as directory:
            venv = Path(directory) / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, text=True)
            scripts = venv / ("Scripts" if sys.platform == "win32" else "bin")
            python = scripts / ("python.exe" if sys.platform == "win32" else "python")
            mcp = scripts / ("cited-vault-recall-mcp.exe" if sys.platform == "win32" else "cited-vault-recall-mcp")
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-deps", "-e", str(ROOT)],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
            result = subprocess.run(
                [str(mcp), "--vault", str(DEMO_VAULT)],
                input=json.dumps(request) + "\n",
                check=True,
                capture_output=True,
                text=True,
                timeout=15,
            )
            response = json.loads(result.stdout)
            self.assertEqual(1, response["id"])
            self.assertEqual(["search"], [tool["name"] for tool in response["result"]["tools"]])


if __name__ == "__main__":
    unittest.main()
