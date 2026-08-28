from __future__ import annotations

import unittest

from cited_vault_recall.lifecycle import CorrectionRequest, LifecycleAction


class LifecycleTests(unittest.TestCase):
    def test_correction_is_explicit_and_supersedes_one_identified_target(self):
        request = CorrectionRequest(
            target_id="decision-1",
            action=LifecycleAction.CORRECT,
            evidence_id="note.md#2",
            replacement_value="Use explicit local staging.",
        )
        self.assertEqual("decision-1", request.target_id)
        self.assertEqual("note.md#2", request.evidence_id)
        self.assertFalse(hasattr(request, "apply"))
        self.assertEqual(
            {"target_id": "decision-1", "action": "correct", "evidence_id": "note.md#2", "replacement_value": "Use explicit local staging.", "expires_at": None},
            request.to_dict(),
        )

    def test_correction_requires_replacement_value(self):
        with self.assertRaisesRegex(ValueError, "replacement_value"):
            CorrectionRequest("decision-1", LifecycleAction.CORRECT, "note.md#2")

    def test_expiry_requires_explicit_timestamp(self):
        with self.assertRaisesRegex(ValueError, "explicit expires_at"):
            CorrectionRequest("decision-1", LifecycleAction.EXPIRE, "note.md#2")


if __name__ == "__main__":
    unittest.main()
