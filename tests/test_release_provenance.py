from __future__ import annotations

import unittest
from pathlib import Path


class ReleaseProvenancePolicyTests(unittest.TestCase):
    def test_policy_keeps_releases_github_only_and_defines_required_evidence(self):
        policy = Path(__file__).parents[1] / "docs" / "release-provenance.md"
        text = policy.read_text(encoding="utf-8")
        for required in (
            "GitHub-only",
            "No PyPI upload",
            "tag must match",
            "PATCH",
            "MINOR",
            "MAJOR",
            "clean-tree",
            "full test suite",
            "SBOM",
            "provenance attestation",
            "UPSTREAMS.md",
            "ADAPTATIONS.md",
            "No release, tag, artifact, or attestation is created by this policy",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
