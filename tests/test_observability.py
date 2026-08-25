from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_recall.core import build_local_index
from agent_recall.observability import BoundedCache, index_diagnostics


class ObservabilityTests(unittest.TestCase):
    def test_index_diagnostics_are_aggregate_and_path_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            (vault / "note.md").write_text("# Note\n\nbody\n", encoding="utf-8")
            destination = root / "index.json"
            index = build_local_index(vault, destination)
            diagnostics = index_diagnostics(vault, destination, index, now_ns=destination.stat().st_mtime_ns + 2_000_000_000, latency_ms=3.5)

            self.assertEqual({"age_seconds", "source_count", "record_count", "index_version", "rebuild_needed", "latency_ms"}, set(diagnostics))
            self.assertEqual(2.0, diagnostics["age_seconds"])
            self.assertEqual(1, diagnostics["source_count"])
            self.assertEqual(1, diagnostics["record_count"])
            self.assertFalse(diagnostics["rebuild_needed"])
            self.assertNotIn(str(vault), str(diagnostics))

    def test_bounded_cache_is_lru_with_explicit_invalidation(self):
        cache = BoundedCache[str](capacity=2)
        cache.put("one", "1")
        cache.put("two", "2")
        self.assertEqual("1", cache.get("one"))
        cache.put("three", "3")
        self.assertIsNone(cache.get("two"))
        self.assertEqual("1", cache.get("one"))
        cache.invalidate("one")
        self.assertIsNone(cache.get("one"))
        cache.clear()
        self.assertEqual(0, len(cache))


if __name__ == "__main__":
    unittest.main()
