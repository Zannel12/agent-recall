from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class DependencyPolicyTests(unittest.TestCase):
    def test_runtime_dependency_baseline_is_empty_and_policy_requires_explicit_review(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        policy = (ROOT / "docs" / "dependency-policy.md").read_text(encoding="utf-8")

        self.assertNotIn("dependencies =", pyproject)
        self.assertNotIn("[project.optional-dependencies]", pyproject)
        for required in (
            "Explicit dependency review",
            "network-capable runtime dependency",
            "mandatory model download",
            "no silent network access",
            "supply-chain-manifest.json",
            "semantic-retrieval-gate.md",
        ):
            self.assertIn(required, policy)

    def test_policy_lists_currently_forbidden_dense_runtime_dependencies(self):
        project_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
        policy = (ROOT / "docs" / "dependency-policy.md").read_text(encoding="utf-8")

        for dependency in ("sentence-transformers", "transformers", "torch", "faiss"):
            self.assertNotIn(dependency, project_text)
            self.assertIn(dependency, policy)


if __name__ == "__main__":
    unittest.main()
