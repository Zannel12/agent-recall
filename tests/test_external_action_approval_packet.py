from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PACKET = ROOT / "docs" / "external-action-approval-packet.md"


class ExternalActionApprovalPacketTests(unittest.TestCase):
    def test_packet_keeps_each_external_action_independent_and_denied_by_default(self):
        text = PACKET.read_text(encoding="utf-8")
        for item in (
            "C1 — dependency/action SHA pinning",
            "C2 — semantic/vector/LLM retrieval",
            "C3 — real Hermes integration",
            "C4 — one named Codex, Claude Code, Cursor, or OpenClaw integration",
            "C5 — production deployment evidence",
            "C6a — SBOM generation",
            "C6b — provenance attestation",
            "C7a — Git tag",
            "C7b — GitHub Release",
            "C8 — PyPI publication",
        ):
            self.assertIn(item, text)
        self.assertIn("Default: DENY / no action", text)
        self.assertIn("exactly one", text)
        self.assertIn("fresh explicit user approval", text)
        self.assertIn("No action is authorized by this document", text)

    def test_packet_requires_a_fresh_candidate_snapshot_and_never_handles_credentials(self):
        text = PACKET.read_text(encoding="utf-8")
        for requirement in (
            "must be refreshed",
            "B1 audit",
            "candidate commit",
            "artifact checksums",
            "CI run",
            "credentials",
            "2FA",
            "owner completes",
            "APPROVE C1",
            "DENY C1",
        ):
            self.assertIn(requirement, text)
        self.assertNotIn("APPROVE ALL", text)


if __name__ == "__main__":
    unittest.main()
