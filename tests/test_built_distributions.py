from __future__ import annotations

import json
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
BUILD_COMMAND = (
    "from setuptools.build_meta import build_sdist, build_wheel; "
    "build_sdist('dist'); build_wheel('dist')"
)


class BuiltDistributionSmokeTests(unittest.TestCase):
    def test_sdist_and_wheel_build_and_install_non_editably(self):
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            clone = workspace / "agent-recall"
            subprocess.run(
                ["git", "clone", "--local", str(ROOT), str(clone)],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "-c", BUILD_COMMAND],
                cwd=clone,
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            artifacts = sorted((clone / "dist").iterdir())
            wheel = next(path for path in artifacts if path.suffix == ".whl")
            sdist = next(path for path in artifacts if path.name.endswith(".tar.gz"))
            with tarfile.open(sdist) as archive:
                members = {member.name.split("/", 1)[-1] for member in archive.getmembers() if "/" in member.name}
            self.assertIn("pyproject.toml", members)
            self.assertIn("src/agent_recall/mcp.py", members)
            self._assert_installable(wheel, clone / "examples" / "demo-vault", workspace / "wheel-venv", environment)

    def _assert_installable(self, artifact: Path, vault: Path, venv: Path, environment: dict[str, str]) -> None:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, text=True, env=environment
        )
        commands = venv / "bin"
        python = commands / "python"
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", "--no-build-isolation", str(artifact)],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        query = subprocess.run(
            [str(commands / "agent-recall"), str(vault), "privacy", "--format", "json"],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        payload = json.loads(query.stdout)
        self.assertEqual("privacy.md", payload["hits"][0]["relative_path"])
        mcp_help = subprocess.run(
            [str(commands / "agent-recall-mcp"), "--help"],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertIn("--vault", mcp_help.stdout)


if __name__ == "__main__":
    unittest.main()
