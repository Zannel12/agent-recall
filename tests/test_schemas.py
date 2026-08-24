import json
import unittest
from dataclasses import asdict

from agent_recall.schemas import Citation, EvidenceItem, Source, derived_fact


class SchemaTests(unittest.TestCase):
    def test_derived_fact_preserves_provenance_and_wire_fields(self):
        source = Source("vault:privacy.md", "markdown", "untrusted", "privacy.md", "2026-08-24T00:00:00Z")
        citation = Citation(source.source_id, "privacy.md#privacy-1", 3, 3)
        fact = derived_fact("fact:privacy", "Privacy remains local.", 0.8, "2026-08-24T00:00:00Z", source, citation)

        self.assertFalse(fact.executable)
        self.assertEqual((source.source_id,), fact.provenance)
        self.assertEqual(citation, fact.citations[0])
        self.assertEqual("fact:privacy", json.loads(json.dumps(asdict(fact)))["fact_id"])

    def test_evidence_item_serializes_the_versioned_public_wire_contract(self):
        item = EvidenceItem(
            source_id="vault:privacy.md",
            path="privacy.md",
            chunk_id="privacy.md#privacy-1",
            relevance=0.75,
            trust="untrusted",
            freshness="observed",
            provenance=("vault:privacy.md",),
        )

        wire = item.to_wire()

        self.assertEqual(
            {
                "schema_version": "1.0",
                "source_id": "vault:privacy.md",
                "path": "privacy.md",
                "chunk_id": "privacy.md#privacy-1",
                "relevance": 0.75,
                "trust": "untrusted",
                "freshness": "observed",
                "provenance": ["vault:privacy.md"],
            },
            wire,
        )
        self.assertEqual(wire, json.loads(json.dumps(wire)))


if __name__ == "__main__":
    unittest.main()
