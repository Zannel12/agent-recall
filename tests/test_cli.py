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
                [sys.executable, "-m", "agent_recall.cli", str(vault), "privacy", "--format", "json"],
                cwd=Path(__file__).parents[1],
                env=environment,
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("privacy", payload["query"])
            self.assertEqual("privacy.md", payload["hits"][0]["relative_path"])


if __name__ == "__main__":
    unittest.main()
