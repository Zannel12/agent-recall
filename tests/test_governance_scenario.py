from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from agent_recall.cli import main
from agent_recall.lifecycle import CorrectionRequest, LifecycleAction
from agent_recall.mcp import McpSearch
from agent_recall.portability import DeletionRequest
from agent_recall.staging import MemoryCandidate, ReviewDecision, append_candidate


class GovernanceScenarioTests(unittest.TestCase):
    def test_synthetic_vault_governance_scenario(self):
        with tempfile.TemporaryDirectory() as temporary:
            vault = Path(temporary) / "vault"
            vault.mkdir()
            note = vault / "governance.md"
            note.write_text("# Governance\n\nExplicit vaults keep recall local.\n", encoding="utf-8")

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--vault", str(vault), "--json"]))
            doctor = json.loads(output.getvalue())
            self.assertTrue(doctor["install"]["ok"])
            self.assertTrue(doctor["vault"]["accessible"])
            self.assertFalse(doctor["local_state"]["discovered"])

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(0, main([str(vault), "explicit vault", "--format", "json"]))
            packet = json.loads(output.getvalue())
            self.assertEqual(1, len(packet["hits"]))
            self.assertNotIn(str(vault), output.getvalue())
            hit = packet["hits"][0]

            evidence = McpSearch(vault).read(hit["chunk_id"])
            self.assertEqual("governance.md", evidence["relative_path"])
            self.assertNotIn(str(vault), json.dumps(evidence))

            candidate = MemoryCandidate("safety_boundary", "Use explicit vaults", hit["chunk_id"], True)
            staging = Path(temporary) / "staging.jsonl"
            append_candidate(staging, candidate)
            self.assertEqual(candidate.to_dict(), json.loads(staging.read_text(encoding="utf-8")))
            self.assertEqual("approved", ReviewDecision(candidate, "approved").outcome)
            self.assertEqual("rejected", ReviewDecision(candidate, "rejected").outcome)

            correction = CorrectionRequest(hit["chunk_id"], LifecycleAction.CORRECT, hit["chunk_id"], "Use explicit vaults only")
            deletion = DeletionRequest(hit["chunk_id"], hit["chunk_id"])
            self.assertFalse(hasattr(correction, "apply"))
            self.assertFalse(hasattr(deletion, "delete"))
            self.assertTrue(note.exists())


if __name__ == "__main__":
    unittest.main()
