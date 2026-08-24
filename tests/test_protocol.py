from __future__ import annotations

import json
import unittest
from pathlib import Path


class ProtocolSchemaTests(unittest.TestCase):
    def test_v1_protocol_schemas_have_closed_versioned_contracts(self):
        root = Path(__file__).parents[1] / "protocol" / "v1"
        names = {"search-request.schema.json", "search-response.schema.json", "citation.schema.json", "error.schema.json"}
        self.assertEqual(names, {path.name for path in root.glob("*.schema.json")})
        schemas = {name: json.loads((root / name).read_text(encoding="utf-8")) for name in names}
        for schema in schemas.values():
            self.assertFalse(schema["additionalProperties"])
        self.assertEqual({"schema_version", "query", "vault"}, set(schemas["search-request.schema.json"]["required"]))
        self.assertEqual("1.0", schemas["search-request.schema.json"]["properties"]["schema_version"]["const"])
        self.assertEqual("1.0", schemas["search-response.schema.json"]["properties"]["schema_version"]["const"])
        self.assertIn("relative_path", schemas["citation.schema.json"]["required"])
        self.assertEqual("1.0", schemas["error.schema.json"]["properties"]["schema_version"]["const"])


if __name__ == "__main__":
    unittest.main()
