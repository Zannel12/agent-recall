import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
ENVIRONMENT = {**os.environ, "PYTHONPATH": "src"}


class DoctorReadinessTests(unittest.TestCase):
    def _doctor(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "cited_vault_recall.cli", "doctor", *arguments, "--json"],
            cwd=ROOT,
            env=ENVIRONMENT,
            text=True,
            capture_output=True,
        )

    def test_doctor_reports_bounded_ready_checks_for_an_explicit_synthetic_vault(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory) / "vault"
            vault.mkdir()
            (vault / "privacy.md").write_text("# Privacy\n\nLocal retrieval is read-only.", encoding="utf-8")
            (vault / "ignored.md").write_text("# Ignored\n\nprivate", encoding="utf-8")
            (vault / ".recallignore").write_text("ignored.md\n", encoding="utf-8")

            result = self._doctor("--vault", str(vault))

            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("READY", payload["status"])
            self.assertEqual("READY", payload["install"]["code"])
            self.assertEqual({"configured": True, "accessible": True, "readable": True, "code": "READY"}, payload["vault"])
            self.assertEqual({"configured": True, "code": "READY", "skipped_files": 1}, payload["ignore"])
            self.assertEqual({"code": "READY", "hits": 1}, payload["search"])
            self.assertEqual({"discovered": False}, payload["local_state"])
            self.assertNotIn(str(vault), result.stdout)

    def test_doctor_uses_a_stable_missing_vault_code_without_discovery_or_path_leak(self):
        missing = Path(tempfile.gettempdir()) / "cited-vault-recall-private-doctor-vault"
        result = self._doctor("--vault", str(missing))

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("NOT_READY", payload["status"])
        self.assertEqual("VAULT_NOT_FOUND", payload["vault"]["code"])
        self.assertEqual("NOT_RUN", payload["ignore"]["code"])
        self.assertEqual("NOT_RUN", payload["search"]["code"])
        self.assertFalse(payload["local_state"]["discovered"])
        self.assertNotIn(str(missing), result.stdout)


if __name__ == "__main__":
    unittest.main()
