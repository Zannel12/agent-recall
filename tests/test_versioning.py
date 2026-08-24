from __future__ import annotations

import unittest

from agent_recall.versioning import Compatibility, MigrationPlan, RecoveryAction, VersionSet, assess_compatibility, assess_recovery


class VersioningTests(unittest.TestCase):
    def test_product_protocol_schema_and_index_versions_are_independent(self):
        versions = VersionSet(product="0.1.0", protocol="1.0", schema="1.0", index="1.0")
        self.assertEqual(Compatibility.READY, assess_compatibility(versions, versions))
        self.assertEqual(Compatibility.MIGRATION_REQUIRED, assess_compatibility(versions, VersionSet("0.1.0", "1.0", "1.0", "2.0")))
    def test_corrupt_derived_artifact_requires_rebuild_not_silent_repair(self):
        self.assertEqual(RecoveryAction.REBUILD_DERIVED, assess_recovery(derived=True, corrupt=True))
        self.assertEqual(RecoveryAction.STOP_AND_REPORT, assess_recovery(derived=False, corrupt=True))

    def test_migration_plan_requires_snapshot_and_explicit_rollback_target(self):
        plan = MigrationPlan(from_version="1.0", to_version="2.0", snapshot_id="snapshot-1", rollback_target="snapshot-1")
        self.assertEqual("snapshot-1", plan.rollback_target)
        self.assertFalse(hasattr(plan, "execute"))


if __name__ == "__main__":
    unittest.main()
