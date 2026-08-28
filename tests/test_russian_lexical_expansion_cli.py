from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class RussianLexicalExpansionCliTests(unittest.TestCase):
    def test_expansion_is_cli_opt_in_and_recovers_the_synthetic_morphology_case(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "memory.md").write_text("# Локальная память\n\nЛокальная память остаётся в vault.", encoding="utf-8")
            command = [sys.executable, "-m", "cited_vault_recall.cli", str(vault), "локальную", "--format", "json"]
            environment = {**os.environ, "PYTHONPATH": "src"}

            default = subprocess.run(command, cwd=ROOT, env=environment, text=True, capture_output=True, check=True)
            expanded = subprocess.run(
                [*command, "--russian-lexical-expansion"],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=True,
            )

            self.assertEqual([], json.loads(default.stdout)["hits"])
            self.assertEqual("memory.md", json.loads(expanded.stdout)["hits"][0]["relative_path"])


if __name__ == "__main__":
    unittest.main()
