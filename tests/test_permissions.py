from __future__ import annotations

import unittest

from cited_vault_recall.permissions import Action, NamespaceScope, is_allowed


class PermissionTests(unittest.TestCase):
    def test_all_known_scopes_are_read_only(self):
        for scope in NamespaceScope:
            self.assertTrue(is_allowed(scope, Action.READ))
            self.assertFalse(is_allowed(scope, Action.WRITE))

    def test_unknown_or_malformed_values_default_to_deny(self):
        for scope, action in (("user", "read"), ("USER", "read"), (" user", "read"), ("user", " write"), (None, "read"), ("agent", None)):
            self.assertFalse(is_allowed(scope, action))


if __name__ == "__main__":
    unittest.main()
