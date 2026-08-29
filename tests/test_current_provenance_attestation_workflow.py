from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "provenance-attestation-current.yml"
SOURCE_COMMIT = "70e358022e507279939b4cc9435d185e84474433"
CHECKOUT_SHA = "11d5960a326750d5838078e36cf38b85af677262"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"
UPLOAD_SHA = "ea165f8d65b6e75b540449e92b4886f43607fa02"
DOWNLOAD_SHA = "d3f86a106a0bac45b974a628896c90dbdf5c8093"
ATTEST_SHA = "1e69f48acb82d1966a394da916b4c1698aa569d6"


class CurrentProvenanceAttestationWorkflowTests(unittest.TestCase):
    def test_manual_one_shot_workflow_attests_only_exact_020_subjects(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("push:", text)
        self.assertNotIn("pull_request:", text)
        self.assertIn("permissions: {}", text)
        self.assertIn(f"ref: {SOURCE_COMMIT}", text)
        self.assertIn('cited_vault_recall-0.2.0-py3-none-any.whl', text)
        self.assertIn('cited_vault_recall-0.2.0.tar.gz', text)
        self.assertIn(f"actions/checkout@{CHECKOUT_SHA}", text)
        self.assertIn(f"actions/setup-python@{SETUP_PYTHON_SHA}", text)
        self.assertIn(f"actions/upload-artifact@{UPLOAD_SHA}", text)
        self.assertIn(f"actions/download-artifact@{DOWNLOAD_SHA}", text)
        self.assertIn(f"actions/attest@{ATTEST_SHA}", text)
        self.assertIn("attestations: write", text)
        self.assertIn("id-token: write", text)
        self.assertIn("retention-days: 1", text)
        self.assertIn("without repository checkout", text)
        self.assertIn("subject-checksums:", text)


if __name__ == "__main__":
    unittest.main()
