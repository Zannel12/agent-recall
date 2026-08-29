from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CHECKOUT_SHA = "11d5960a326750d5838078e36cf38b85af677262"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"


class WorkflowShaPinningTests(unittest.TestCase):
    def test_existing_workflow_actions_are_pinned_to_verified_full_shas_without_permission_change(self):
        workflow = (ROOT / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")

        self.assertEqual(2, workflow.count(f"uses: actions/checkout@{CHECKOUT_SHA}"))
        self.assertEqual(2, workflow.count(f"uses: actions/setup-python@{SETUP_PYTHON_SHA}"))
        self.assertNotIn("actions/checkout@v4", workflow)
        self.assertNotIn("actions/setup-python@v5", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)

    def test_inventory_and_evidence_record_the_exact_source_mapping(self):
        manifest = json.loads((ROOT / "supply-chain-manifest.json").read_text(encoding="utf-8"))
        uses = [item for workflow in manifest["workflows"] for item in workflow["uses"]]
        self.assertEqual(
            {
                (f"actions/checkout@{CHECKOUT_SHA}", "full_sha_format_unverified"),
                (f"actions/setup-python@{SETUP_PYTHON_SHA}", "full_sha_format_unverified"),
                ("actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02", "full_sha_format_unverified"),
                ("actions/download-artifact@d3f86a106a0bac45b974a628896c90dbdf5c8093", "full_sha_format_unverified"),
                ("actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6", "full_sha_format_unverified"),
            },
            {(item["reference"], item["classification"]) for item in uses},
        )
        evidence = (ROOT / "docs" / "supply-chain-pinning.md").read_text(encoding="utf-8")
        self.assertIn("git/ref/tags/v4", evidence)
        self.assertIn("git/ref/tags/v5", evidence)
        self.assertIn(CHECKOUT_SHA, evidence)
        self.assertIn(SETUP_PYTHON_SHA, evidence)
        self.assertIn("not a lockfile", evidence)
        self.assertIn("not an SBOM", evidence)


if __name__ == "__main__":
    unittest.main()
