from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DEMO_VAULT = ROOT / "examples" / "demo-vault"

from cited_vault_recall.hermes_adapter import PlanStatus, build_hermes_mcp_plan


class HermesAdapterPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Path("/synthetic/hermes-config.yaml")
        self.backup = Path("/synthetic/hermes-config.yaml.cited-vault-recall.bak")
        self.vault = Path("/synthetic/vault")

    def test_plan_requires_explicit_consent_before_emitting_commands(self):
        plan = build_hermes_mcp_plan(
            config_path=self.config,
            backup_path=self.backup,
            vault_path=self.vault,
            observed_server_names=set(),
            config_exists=True,
            consent=False,
        )

        self.assertEqual(plan.status, PlanStatus.CONSENT_REQUIRED)
        self.assertEqual(plan.commands, ())
        self.assertEqual(plan.cli_fallback, ("cited-vault-recall", str(self.vault)))

    def test_plan_is_apply_ready_only_with_distinct_backup_and_no_collision(self):
        plan = build_hermes_mcp_plan(
            config_path=self.config,
            backup_path=self.backup,
            vault_path=self.vault,
            observed_server_names={"other-server"},
            config_exists=True,
            consent=True,
        )

        self.assertEqual(plan.status, PlanStatus.READY)
        self.assertEqual(plan.config_entry["command"], "cited-vault-recall-mcp")
        self.assertEqual(plan.config_entry["args"], ["--vault", str(self.vault)])
        self.assertEqual(plan.config_entry["tools"], {"include": ["search"]})
        self.assertEqual(plan.config_entry["sampling"], {"enabled": False})
        self.assertEqual(plan.commands[0], ("cp", "--", str(self.config), str(self.backup)))
        self.assertIn(("hermes", "mcp", "remove", "cited-vault-recall"), plan.commands)

    def test_existing_cited_vault_recall_server_is_a_hard_collision(self):
        plan = build_hermes_mcp_plan(
            config_path=self.config,
            backup_path=self.backup,
            vault_path=self.vault,
            observed_server_names={"cited-vault-recall"},
            config_exists=True,
            consent=True,
        )

        self.assertEqual(plan.status, PlanStatus.NAME_COLLISION)
        self.assertEqual(plan.commands, ())

    def test_missing_config_observation_is_non_executing(self):
        plan = build_hermes_mcp_plan(
            config_path=self.config,
            backup_path=self.backup,
            vault_path=self.vault,
            observed_server_names=set(),
            config_exists=False,
            consent=True,
        )

        self.assertEqual(plan.status, PlanStatus.CONFIG_MISSING)
        self.assertEqual(plan.commands, ())

    def test_same_config_and_backup_paths_are_rejected(self):
        plan = build_hermes_mcp_plan(
            config_path=self.config,
            backup_path=self.config,
            vault_path=self.vault,
            observed_server_names=set(),
            config_exists=True,
            consent=True,
        )

        self.assertEqual(plan.status, PlanStatus.INVALID_BACKUP)
        self.assertEqual(plan.commands, ())

    def test_generated_cli_fallback_runs_in_an_isolated_editable_install(self):
        plan = build_hermes_mcp_plan(
            config_path=self.config,
            backup_path=self.backup,
            vault_path=DEMO_VAULT,
            observed_server_names=set(),
            config_exists=True,
            consent=True,
        )
        with tempfile.TemporaryDirectory() as directory:
            venv = Path(directory) / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, text=True)
            scripts = venv / ("Scripts" if sys.platform == "win32" else "bin")
            python = scripts / ("python.exe" if sys.platform == "win32" else "python")
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-deps", "-e", str(ROOT)],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            environment = {**os.environ, "PATH": str(scripts) + os.pathsep + os.environ.get("PATH", "")}
            result = subprocess.run(
                plan.cli_fallback + ("privacy", "--format", "json"),
                check=True,
                capture_output=True,
                text=True,
                timeout=15,
                env=environment,
            )
        payload = json.loads(result.stdout)
        self.assertEqual("privacy", payload["query"])
        self.assertTrue(payload["hits"])


if __name__ == "__main__":
    unittest.main()
