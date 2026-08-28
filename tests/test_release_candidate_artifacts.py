from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "tools" / "build_release_candidate.py"


class ReleaseCandidateArtifactTests(unittest.TestCase):
    def test_offline_builder_writes_unpublished_artifacts_and_verifiable_checksums(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate"
            subprocess.run(
                [sys.executable, str(SCRIPT), "--output", str(output)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            manifest = json.loads((output / "release-candidate-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("1.0", manifest["schema_version"])
            self.assertEqual("cited-vault-recall", manifest["package"])
            self.assertEqual("0.2.0.dev0", manifest["version"])
            self.assertTrue(manifest["unpublished"])
            artifacts = manifest["artifacts"]
            self.assertEqual(2, len(artifacts))
            self.assertEqual(sorted(item["filename"] for item in artifacts), [item["filename"] for item in artifacts])
            self.assertTrue(any(item["filename"].endswith(".whl") for item in artifacts))
            self.assertTrue(any(item["filename"].endswith(".tar.gz") for item in artifacts))
            for artifact in artifacts:
                payload = (output / "artifacts" / artifact["filename"]).read_bytes()
                self.assertEqual(len(payload), artifact["bytes"])
                self.assertEqual(hashlib.sha256(payload).hexdigest(), artifact["sha256"])

            checksums = (output / "SHA256SUMS").read_text(encoding="utf-8")
            self.assertNotIn(str(output), checksums)
            self.assertEqual(2, len([line for line in checksums.splitlines() if line]))


if __name__ == "__main__":
    unittest.main()
