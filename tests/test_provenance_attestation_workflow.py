from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "provenance-attestation.yml"
SOURCE_COMMIT = "037f90437a05ae93a700d321d584b85abbb9e569"
CHECKOUT_SHA = "11d5960a326750d5838078e36cf38b85af677262"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"
UPLOAD_SHA = "ea165f8d65b6e75b540449e92b4886f43607fa02"
DOWNLOAD_SHA = "d3f86a106a0bac45b974a628896c90dbdf5c8093"
ATTEST_SHA = "1e69f48acb82d1966a394da916b4c1698aa569d6"


class ProvenanceAttestationWorkflowTests(unittest.TestCase):
    def test_c6b_workflow_is_manual_pinned_and_separates_privileged_attestation(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("push:", text)
        self.assertNotIn("pull_request:", text)
        self.assertIn("permissions: {}", text)
        self.assertIn(f"actions/checkout@{CHECKOUT_SHA}", text)
        self.assertIn(f"ref: {SOURCE_COMMIT}", text)
        self.assertIn(f"actions/setup-python@{SETUP_PYTHON_SHA}", text)
        self.assertIn(f"actions/upload-artifact@{UPLOAD_SHA}", text)
        self.assertIn("retention-days: 1", text)
        self.assertIn(f"actions/download-artifact@{DOWNLOAD_SHA}", text)
        self.assertIn(f"actions/attest@{ATTEST_SHA}", text)
        self.assertIn("contents: read", text)
        self.assertIn("attestations: write", text)
        self.assertIn("id-token: write", text)
        self.assertIn("subject-checksums:", text)
        self.assertNotIn("subject-path:", text)
        self.assertNotIn("sbom-path:", text)
        self.assertNotIn("push-to-registry:", text)

    def test_c6b_contract_keeps_oidc_out_of_the_repository_build_job(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        build, attest = text.split("  attest:", maxsplit=1)
        self.assertIn("  build:", build)
        self.assertNotIn("id-token: write", build)
        self.assertNotIn("attestations: write", build)
        self.assertIn("id-token: write", attest)
        self.assertIn("attestations: write", attest)
        self.assertNotIn("actions/checkout@", attest)
        self.assertIn("Verify transferred checksums", attest)
        self.assertIn("release-candidate-manifest.json", build)
        self.assertIn("SHA256SUMS", build)


if __name__ == "__main__":
    unittest.main()
