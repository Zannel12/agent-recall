from __future__ import annotations

import unittest
from pathlib import Path


SOURCE = Path(__file__).parents[1] / "src" / "cited_vault_recall"


class Python310CompatibilityTests(unittest.TestCase):
    def test_package_uses_its_compatible_string_enum_base(self):
        for path in SOURCE.glob("*.py"):
            self.assertNotIn("from enum import StrEnum", path.read_text(encoding="utf-8"), path)

    def test_compatible_string_enum_keeps_value_string_semantics(self):
        from cited_vault_recall._compat import StrEnum

        class Example(StrEnum):
            VALUE = "value"

        self.assertIsInstance(Example.VALUE, str)
        self.assertEqual("value", str(Example.VALUE))
        self.assertEqual("value", Example.VALUE.value)


if __name__ == "__main__":
    unittest.main()
