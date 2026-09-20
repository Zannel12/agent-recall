from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "docs" / "releases" / "0.2.0-evidence.md"


class ReleaseEvidenceIndexTests(unittest.TestCase):
    def test_current_release_evidence_index_links_exact_assets_and_limits(self):
        text = EVIDENCE.read_text(encoding="utf-8")

        for required in (
            "https://github.com/Zannel12/agent-recall/releases/tag/v0.2.0",
            "https://github.com/Zannel12/agent-recall/attestations/43887002",
            "409d8ce7e5480e1649e1c307ca8baf3dfdfb8feaaeb3fcb3620ca2d6ed4527d2",
            "f9291b7c9ea46241f8dbc38bff38e438229d6b089b3bbade5a5eea58316a7eb1",
            "d1192ff9f1913d807efe9568338d11189d8f2840b42357d2c53afe8e1781fea3",
            "SPDX-2.3",
            "does not prove a hosted production deployment",
            "does not publish the package to PyPI",
            "does not make any host integration Production-tested",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
