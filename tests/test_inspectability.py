from __future__ import annotations

import unittest

from agent_recall.inspectability import InspectableMemory, MutationIntent


class InspectabilityTests(unittest.TestCase):
    def test_inspectable_memory_exposes_value_status_and_evidence_without_mutation(self):
        view = InspectableMemory("decision-1", "Use local-only retrieval.", "current", "note.md#1")
        self.assertEqual({"id": "decision-1", "value": "Use local-only retrieval.", "status": "current", "evidence_id": "note.md#1"}, view.to_dict())
        self.assertFalse(hasattr(view, "delete"))
    def test_mutation_intent_is_explicit_and_non_executing(self):
        intent = MutationIntent("correct", "decision-1", "Updated local-only wording.")
        self.assertEqual("correct", intent.action)
        self.assertFalse(hasattr(intent, "apply"))


if __name__ == "__main__":
    unittest.main()
