from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
BUILD = ROOT / "tools" / "build_release_candidate.py"
SBOM = ROOT / "tools" / "generate_spdx_sbom.py"


class SpdxSbomTests(unittest.TestCase):
    def test_generator_writes_spdx_for_the_exact_unpublished_wheel_and_sdist(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate"
            subprocess.run([sys.executable, str(BUILD), "--output", str(output)], cwd=ROOT, check=True, capture_output=True, text=True)
            sbom = output / "cited-vault-recall.spdx.json"
            subprocess.run(
                [
                    sys.executable,
                    str(SBOM),
                    "--artifact-manifest",
                    str(output / "release-candidate-manifest.json"),
                    "--output",
                    str(sbom),
                    "--created",
                    "2026-08-28T00:00:00Z",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(sbom.read_text(encoding="utf-8"))
            self.assertEqual("SPDX-2.3", payload["spdxVersion"])
            self.assertEqual("CC0-1.0", payload["dataLicense"])
            self.assertEqual("2026-08-28T00:00:00Z", payload["creationInfo"]["created"])
            self.assertEqual("cited-vault-recall", payload["packages"][0]["name"])
            self.assertEqual("0.2.0", payload["packages"][0]["versionInfo"])
            self.assertIn("unpublished", payload["packages"][0]["comment"])
            files = {item["fileName"]: item for item in payload["files"]}
            manifest = json.loads((output / "release-candidate-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(2, len(files))
            for artifact in manifest["artifacts"]:
                file = files[f"artifacts/{artifact['filename']}"]
                self.assertEqual(artifact["sha256"], file["checksums"][0]["checksumValue"])
                self.assertEqual(artifact["bytes"], (output / file["fileName"]).stat().st_size)
                self.assertEqual(artifact["sha256"], hashlib.sha256((output / file["fileName"]).read_bytes()).hexdigest())

    def test_generator_rejects_manifest_checksum_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate"
            subprocess.run([sys.executable, str(BUILD), "--output", str(output)], cwd=ROOT, check=True, capture_output=True, text=True)
            manifest = json.loads((output / "release-candidate-manifest.json").read_text(encoding="utf-8"))
            artifact = output / "artifacts" / manifest["artifacts"][0]["filename"]
            artifact.write_bytes(artifact.read_bytes() + b"tamper")
            result = subprocess.run(
                [sys.executable, str(SBOM), "--artifact-manifest", str(output / "release-candidate-manifest.json"), "--output", str(output / "bad.spdx.json"), "--created", "2026-08-28T00:00:00Z"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("artifact bytes or checksum do not match", result.stderr)


if __name__ == "__main__":
    unittest.main()
