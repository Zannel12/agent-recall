from __future__ import annotations

import unittest

from agent_recall.portability import BundleManifest, DeletionRequest, RestoreRequest


class PortabilityTests(unittest.TestCase):
    def test_manifest_declares_version_coverage_and_source_links(self):
        manifest = BundleManifest("1.0", ("staging",), ("note.md#1",), complete=False)
        self.assertEqual("1.0", manifest.schema_version)
        self.assertFalse(manifest.complete)
        self.assertEqual(("note.md#1",), manifest.source_ids)
        self.assertFalse(hasattr(manifest, "export"))
        self.assertEqual(
            {"schema_version": "1.0", "coverage": ["staging"], "source_ids": ["note.md#1"], "complete": False},
            manifest.to_dict(),
        )

    def test_deletion_request_is_source_linked_and_non_executing(self):
        request = DeletionRequest("candidate-1", "note.md#1")
        self.assertEqual("candidate-1", request.target_id)
        self.assertEqual("note.md#1", request.source_id)
        self.assertFalse(hasattr(request, "delete"))

    def test_restore_request_is_quarantined_by_default(self):
        request = RestoreRequest("bundle-1")
        self.assertTrue(request.quarantined)
        self.assertFalse(hasattr(request, "restore"))


if __name__ == "__main__":
    unittest.main()
