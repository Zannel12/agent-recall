from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CHECKLIST = ROOT / "docs" / "maintainer-release-checklist.md"


class MaintainerReleaseChecklistTests(unittest.TestCase):
    def test_checklist_orders_exact_artifacts_before_each_separate_external_action(self):
        text = CHECKLIST.read_text(encoding="utf-8")

        for required in (
            "Version and release notes",
            "Focused and full verification",
            "Exact artifacts and checksums",
            "SPDX SBOM",
            "GitHub provenance attestation",
            "Annotated Git tag",
            "GitHub Release",
            "PyPI publication",
            "one external action per Goal turn",
            "fresh preflight",
            "read back",
            "Never paste or store credentials",
        ):
            self.assertIn(required, text)

        self.assertLess(text.index("Exact artifacts and checksums"), text.index("SPDX SBOM"))
        self.assertLess(text.index("SPDX SBOM"), text.index("GitHub provenance attestation"))
        self.assertLess(text.index("GitHub provenance attestation"), text.index("Annotated Git tag"))
        self.assertLess(text.index("Annotated Git tag"), text.index("GitHub Release"))
        self.assertLess(text.index("GitHub Release"), text.index("PyPI publication"))

    def test_contributor_and_readiness_docs_link_to_the_checklist(self):
        for document in (ROOT / "CONTRIBUTING.md", ROOT / "docs" / "release-readiness.md"):
            self.assertIn("maintainer-release-checklist.md", document.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
