import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_json_mode_returns_source_linked_hits(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "privacy.md").write_text(
                "# Privacy\n\nLocal-first memory keeps source context scoped.\n",
                encoding="utf-8",
            )
            environment = {**os.environ, "PYTHONPATH": "src"}
            result = subprocess.run(
                [sys.executable, "-m", "cited_vault_recall.cli", str(vault), "privacy", "--format", "json"],
                cwd=Path(__file__).parents[1],
                env=environment,
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual({"schema_version", "query", "hits", "diagnostics"}, set(payload))
            self.assertEqual("1.0", payload["schema_version"])
            self.assertEqual("privacy", payload["query"])
            self.assertEqual({"skipped_files": 0}, payload["diagnostics"])
            self.assertEqual(
                {"source_id", "score", "score_components", "title", "relative_path", "chunk_id", "heading", "excerpt"},
                set(payload["hits"][0]),
            )
            self.assertEqual("privacy.md", payload["hits"][0]["relative_path"])
            self.assertNotIn(str(vault), result.stdout)
    def test_doctor_uses_user_supplied_config_without_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            config = root / "recall.json"
            config.write_text(json.dumps({"vault": str(vault)}), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "cited_vault_recall.cli", "doctor", "--config", str(config), "--json"],
                cwd=Path(__file__).parents[1], env={**os.environ, "PYTHONPATH": "src"}, text=True, capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(json.loads(result.stdout)["vault"]["accessible"])

    def test_doctor_json_reports_explicit_vault_without_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            result = subprocess.run(
                [sys.executable, "-m", "cited_vault_recall.cli", "doctor", "--vault", str(vault), "--json"],
                cwd=Path(__file__).parents[1], env={**os.environ, "PYTHONPATH": "src"}, text=True, capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual({"status", "install", "vault", "ignore", "search", "local_state"}, set(payload))
            self.assertEqual("READY", payload["status"])
            self.assertFalse(payload["local_state"]["discovered"])

    def test_cli_missing_vault_uses_stable_code_without_path_leak(self):
        missing = Path(tempfile.gettempdir()) / "cited-vault-recall-private-missing-vault"
        result = subprocess.run(
            [sys.executable, "-m", "cited_vault_recall.cli", str(missing), "privacy"],
            cwd=Path(__file__).parents[1], env={**os.environ, "PYTHONPATH": "src"}, text=True, capture_output=True,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("VAULT_NOT_FOUND", result.stderr)
        self.assertNotIn(str(missing), result.stderr)


if __name__ == "__main__":
    unittest.main()
