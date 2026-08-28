from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import cast

from cited_vault_recall.cli import main
from cited_vault_recall.index_integrity import index_needs_rebuild
from cited_vault_recall.core import build_local_index


class IndexIntegrityTests(unittest.TestCase):
    def test_fingerprint_detects_content_or_mtime_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            note = vault / "note.md"
            note.write_text("# Note\n\nfirst\n", encoding="utf-8")
            index = build_local_index(vault, root / "index.json")

            self.assertFalse(index_needs_rebuild(vault, index))
            note.write_text("# Note\n\nchanged\n", encoding="utf-8")
            self.assertTrue(index_needs_rebuild(vault, index))

    def test_mtime_or_integrity_tampering_requires_rebuild(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            note = vault / "note.md"
            note.write_text("# Note\n\nbody\n", encoding="utf-8")
            index = build_local_index(vault, root / "index.json")
            stat = note.stat()
            os.utime(note, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
            self.assertTrue(index_needs_rebuild(vault, index))

            rebuilt = build_local_index(vault, root / "index.json")
            records = cast(list[dict[str, object]], rebuilt["records"])
            records[0]["body"] = "tampered"
            self.assertTrue(index_needs_rebuild(vault, rebuilt))

    def test_unknown_index_version_requires_rebuild(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            (vault / "note.md").write_text("# Note\n\nbody\n", encoding="utf-8")
            index = build_local_index(vault, root / "index.json")
            index["index_version"] = "unsupported"

            self.assertTrue(index_needs_rebuild(vault, index))
    def test_reindex_requires_explicit_outside_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            (vault / "note.md").write_text("# Note\n\nbody\n", encoding="utf-8")
            destination = root / "derived" / "index.json"
            output = io.StringIO()

            with contextlib.redirect_stdout(output):
                self.assertEqual(0, main(["reindex", "--vault", str(vault), "--destination", str(destination), "--json"]))

            payload = json.loads(output.getvalue())
            self.assertTrue(payload["reindexed"])
            self.assertNotIn(str(vault), output.getvalue())
            self.assertTrue(destination.is_file())


if __name__ == "__main__":
    unittest.main()
