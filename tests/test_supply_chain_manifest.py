from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "tools" / "verify_supply_chain_manifest.py"


@unittest.skipUnless(sys.version_info >= (3, 11), "supply-chain verifier requires Python 3.11+ tomllib")
class SupplyChainManifestTests(unittest.TestCase):
    def test_checked_in_inventory_is_current_and_describes_unpinned_baseline_honestly(self):
        manifest = ROOT / "supply-chain-manifest.json"
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(ROOT), "--output", str(manifest), "--check"], text=True, capture_output=True)

        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual("1.0", payload["schema_version"])
        self.assertEqual("declaration_inventory", payload["kind"])
        self.assertEqual([], payload["project"]["runtime_dependencies"])
        self.assertEqual([], payload["project"]["optional_dependencies"])
        self.assertEqual(
            [{"requirement": "setuptools>=68", "classification": "version_range_unpinned"}],
            payload["project"]["build_requirements"],
        )
        actions = [item for workflow in payload["workflows"] for item in workflow["uses"]]
        self.assertEqual(
            [
                ("actions/checkout@v4", "mutable_or_unverified_reference"),
                ("actions/setup-python@v5", "mutable_or_unverified_reference"),
            ],
            sorted(set((item["reference"], item["classification"]) for item in actions)),
        )
        self.assertIn("not a lockfile", payload["limitations"])

    def test_check_fails_closed_when_a_reviewed_declaration_drifts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "pyproject.toml").write_text("[build-system]\nrequires = [\"setuptools>=68\"]\nbuild-backend = \"setuptools.build_meta\"\n[project]\nname = \"fixture\"\nversion = \"0\"\n", encoding="utf-8")
            workflow = root / ".github" / "workflows" / "tests.yml"
            workflow.write_text("jobs:\n  test:\n    steps:\n      - uses: actions/checkout@v4\n      - run: python -m pip install \\\"setuptools>=68\\\"\n", encoding="utf-8")
            output = root / "manifest.json"
            write = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--output", str(output), "--write"], text=True, capture_output=True)
            self.assertEqual(0, write.returncode, write.stderr)
            self.assertEqual(0, subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--output", str(output), "--check"], text=True, capture_output=True).returncode)

            workflow.write_text(workflow.read_text(encoding="utf-8").replace("actions/checkout@v4", "actions/checkout@v5"), encoding="utf-8")
            stale = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--output", str(output), "--check"], text=True, capture_output=True)
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("manifest drift", stale.stderr)

    def test_dynamic_workflow_reference_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "pyproject.toml").write_text("[build-system]\nrequires = []\nbuild-backend = \"setuptools.build_meta\"\n[project]\nname = \"fixture\"\nversion = \"0\"\n", encoding="utf-8")
            (root / ".github" / "workflows" / "tests.yml").write_text("jobs:\n  test:\n    uses: ${{ github.repository }}/workflow@main\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--output", str(root / "manifest.json"), "--write"], text=True, capture_output=True)

            self.assertEqual(2, result.returncode)
            self.assertIn("unsupported workflow uses declaration", result.stderr)


if __name__ == "__main__":
    unittest.main()
