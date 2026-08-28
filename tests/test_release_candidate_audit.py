from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "tools" / "audit_release_candidate.py"


class ReleaseCandidateAuditTests(unittest.TestCase):
    def _repo(self, directory: Path, files: dict[str, str]) -> Path:
        repo = directory / "repo"
        repo.mkdir()
        for name, content in files.items():
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
        return repo

    def test_clean_synthetic_repository_has_a_redacted_passing_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = self._repo(root, {"README.md": "synthetic release candidate\n"})
            report = root / "audit.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--repository", str(repo), "--output", str(report)],
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("1.0", payload["schema_version"])
            self.assertEqual("PASS", payload["status"])
            self.assertTrue(payload["working_tree_clean"])
            self.assertEqual([], payload["findings"])
            self.assertNotIn("synthetic release candidate", result.stdout)

    def test_tracked_secret_like_value_is_rejected_without_echoing_value(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            secret = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            repo = self._repo(root, {"settings.py": f'TOKEN = "{secret}"\n'})
            report = root / "audit.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--repository", str(repo), "--output", str(report)],
                capture_output=True,
                text=True,
            )

            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(1, result.returncode)
            self.assertEqual("FAIL", payload["status"])
            self.assertEqual("secret-pattern", payload["findings"][0]["rule"])
            self.assertEqual("settings.py", payload["findings"][0]["path"])
            self.assertNotIn(secret, report.read_text(encoding="utf-8"))
            self.assertNotIn(secret, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
