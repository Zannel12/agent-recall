from __future__ import annotations

import unittest

from agent_recall.policy import LifecyclePolicy, PostTurnDecision, PreTurnDecision
from agent_recall.staging import MemoryCandidate


class LifecyclePolicyTests(unittest.TestCase):
    def test_explicit_pre_turn_opt_in_creates_only_a_bounded_request(self):
        decision = LifecyclePolicy(pre_turn_opt_in=True, query="privacy boundary", limit=3).pre_turn()
        self.assertEqual(PreTurnDecision.REQUEST_RECALL, decision.action)
        self.assertEqual("privacy boundary", decision.query)
        self.assertEqual(3, decision.limit)
        self.assertFalse(hasattr(decision, "search"))

    def test_missing_opt_in_or_invalid_limit_means_no_pre_turn_action(self):
        self.assertEqual(PreTurnDecision.NO_ACTION, LifecyclePolicy().pre_turn().action)
        with self.assertRaisesRegex(ValueError, "limit"):
            LifecyclePolicy(pre_turn_opt_in=True, query="x", limit=0)

    def test_post_turn_accepts_only_already_qualified_candidate(self):
        candidate = MemoryCandidate("decision", "keep explicit vault", "note.md#1", True)
        decision = LifecyclePolicy().post_turn(candidate)
        self.assertEqual(PostTurnDecision.STAGE_CANDIDATE, decision.action)
        self.assertIs(candidate, decision.candidate)
        self.assertFalse(hasattr(decision, "append"))
    def test_post_turn_rejects_nonqualified_candidate(self):
        candidate = MemoryCandidate("note", "ephemeral", "note.md#1", False)
        with self.assertRaisesRegex(ValueError, "qualified"):
            LifecyclePolicy().post_turn(candidate)


if __name__ == "__main__":
    unittest.main()
