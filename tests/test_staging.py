from __future__ import annotations

import json
import tempfile
import unittest

from pathlib import Path

from agent_recall.staging import MemoryCandidate, ReviewDecision, append_candidate, is_memory_worthy


class StagingTests(unittest.TestCase):
    def test_append_only_staging_keeps_existing_entries(self):
        candidate = MemoryCandidate("decision", "Use explicit staging.", "note.md#1", True)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "staging.jsonl"
            append_candidate(destination, candidate)
            append_candidate(destination, candidate)
            self.assertEqual(2, len(destination.read_text(encoding="utf-8").splitlines()))
            self.assertEqual("decision", json.loads(destination.read_text(encoding="utf-8").splitlines()[0])["kind"])

    def test_review_decision_is_explicit_and_preserves_candidate_evidence(self):
        candidate = MemoryCandidate("decision", "Use explicit staging.", "note.md#1", True)
        decision = ReviewDecision(candidate, "approved")
        self.assertEqual("approved", decision.outcome)
        self.assertEqual("note.md#1", decision.candidate.source_id)
        self.assertFalse(hasattr(decision, "promote"))
        self.assertEqual({"outcome": "approved", "candidate": candidate.to_dict()}, decision.to_dict())

    def test_review_rejects_unknown_outcome(self):
        candidate = MemoryCandidate("decision", "Use explicit staging.", "note.md#1", True)
        with self.assertRaisesRegex(ValueError, "approved or rejected"):
            ReviewDecision(candidate, "deferred")

    def test_staging_rejects_ineligible_candidate_without_creating_destination(self):
        candidate = MemoryCandidate("chat", "Temporary message", "note.md#1", True)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "staging.jsonl"
            with self.assertRaises(ValueError):
                append_candidate(destination, candidate)
            self.assertFalse(destination.exists())

    def test_only_durable_sourced_facts_qualify_as_candidates(self):
        self.assertTrue(is_memory_worthy(kind="decision", durable=True, source_id="note.md#1"))
        self.assertFalse(is_memory_worthy(kind="chat", durable=True, source_id="note.md#1"))
        self.assertFalse(is_memory_worthy(kind="decision", durable=False, source_id="note.md#1"))
        self.assertFalse(is_memory_worthy(kind="decision", durable=True, source_id=""))


if __name__ == "__main__":
    unittest.main()
