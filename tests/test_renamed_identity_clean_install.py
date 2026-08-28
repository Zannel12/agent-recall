from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class RenamedIdentityCleanInstallTests(unittest.TestCase):
    def test_clean_install_exports_only_cited_vault_recall_commands_and_import(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            clone = workspace / "cited-vault-recall"
            venv = workspace / "venv"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "*.egg-info", "__pycache__"))
            subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, text=True)
            commands = venv / "bin"
            python = commands / "python"
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-deps", "-e", str(clone)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue((commands / "cited-vault-recall").is_file())
            self.assertTrue((commands / "cited-vault-recall-mcp").is_file())
            self.assertFalse((commands / "agent-recall").exists())
            self.assertFalse((commands / "agent-recall-mcp").exists())
            imported = subprocess.run(
                [str(python), "-c", "import cited_vault_recall; print(cited_vault_recall.__name__)"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual("cited_vault_recall", imported.stdout.strip())

            vault = clone / "examples" / "demo-vault"
            cli = subprocess.run(
                [str(commands / "cited-vault-recall"), str(vault), "privacy", "--format", "json"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual("privacy.md", json.loads(cli.stdout)["hits"][0]["relative_path"])
            mcp = subprocess.run(
                [str(commands / "cited-vault-recall-mcp"), "--help"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("--vault", mcp.stdout)


if __name__ == "__main__":
    unittest.main()
