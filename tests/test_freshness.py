from __future__ import annotations

import json
import unittest
from pathlib import Path

from cited_vault_recall.freshness import EvidenceRecord, EvidenceStatus, classify_evidence


class FreshnessTests(unittest.TestCase):
    def test_classifies_current_historical_superseded_and_conflicting_evidence(self):
        self.assertEqual(EvidenceStatus.CURRENT, classify_evidence(is_current=True))
        self.assertEqual(EvidenceStatus.HISTORICAL, classify_evidence(is_current=False))
        self.assertEqual(EvidenceStatus.SUPERSEDED, classify_evidence(is_current=False, superseded_by="new-id"))
        self.assertEqual(EvidenceStatus.CONFLICTING, classify_evidence(is_current=True, conflicts_with=("other-id",)))
    def test_fixture_records_round_trip_without_status_inference(self):
        fixture = Path(__file__).parent / "fixtures" / "freshness.json"
        records = [EvidenceRecord.from_dict(item) for item in json.loads(fixture.read_text(encoding="utf-8"))]
        self.assertEqual(["current", "historical", "superseded", "conflicting"], [record.status.value for record in records])
        self.assertEqual(json.loads(fixture.read_text(encoding="utf-8")), [record.to_dict() for record in records])

    def test_record_rejects_absolute_source_path(self):
        with self.assertRaises(ValueError):
            EvidenceRecord("secret.md#1", "/private/secret.md", "historical", EvidenceStatus.HISTORICAL)

    def test_record_preserves_source_provenance_and_serializes_status(self):
        record = EvidenceRecord("note.md#1", "note.md", "historical", EvidenceStatus.HISTORICAL)
        self.assertEqual({"id": "note.md#1", "relative_path": "note.md", "observed_at": "historical", "status": "historical"}, record.to_dict())


if __name__ == "__main__":
    unittest.main()
