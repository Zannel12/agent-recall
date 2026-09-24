from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "pypi-publish.yml"
PUBLISH_ACTION_SHA = "dc37677b2e1c63e2034f94d8a5b11f265b73ba33"
WHEEL = "cited_vault_recall-0.2.0-py3-none-any.whl"
SDIST = "cited_vault_recall-0.2.0.tar.gz"
WHEEL_SHA256 = "409d8ce7e5480e1649e1c307ca8baf3dfdfb8feaaeb3fcb3620ca2d6ed4527d2"
SDIST_SHA256 = "f9291b7c9ea46241f8dbc38bff38e438229d6b089b3bbade5a5eea58316a7eb1"


class PyPiPublishWorkflowContractTests(unittest.TestCase):
    def test_workflow_is_manual_exact_artifact_pinned_and_requires_explicit_confirmation(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:\n", workflow)
        self.assertNotIn("  push:\n", workflow)
        self.assertNotIn("  pull_request:\n", workflow)
        self.assertIn("confirmation:\n", workflow)
        self.assertIn("PUBLISH_CITED_VAULT_RECALL_0_2_0", workflow)
        self.assertIn("if: ${{ inputs.confirmation == 'PUBLISH_CITED_VAULT_RECALL_0_2_0' }}", workflow)
        self.assertIn("environment:\n      name: pypi", workflow)
        self.assertIn("permissions: {}", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertNotIn("actions/checkout", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("password:", workflow)
        self.assertIn(WHEEL, workflow)
        self.assertIn(SDIST, workflow)
        self.assertIn(WHEEL_SHA256, workflow)
        self.assertIn(SDIST_SHA256, workflow)
        self.assertIn(f"pypa/gh-action-pypi-publish@{PUBLISH_ACTION_SHA}", workflow)


if __name__ == "__main__":
    unittest.main()
