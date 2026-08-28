#!/usr/bin/env python3
"""Build an unpublished local release candidate with SHA-256 checksums."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).parents[1]
PACKAGE_PATTERN = re.compile(r'^name\s*=\s*"([^"]+)"$', re.MULTILINE)
VERSION_PATTERN = re.compile(r'^version\s*=\s*"([^"]+)"$', re.MULTILINE)


def package_metadata() -> tuple[str, str]:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    package = PACKAGE_PATTERN.search(text)
    version = VERSION_PATTERN.search(text)
    if package is None or version is None:
        raise RuntimeError("project name/version missing from pyproject.toml")
    return package.group(1), version.group(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build(output: Path) -> dict[str, object]:
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("--output must be outside the repository")
    if output.exists():
        shutil.rmtree(output)
    artifacts_dir = output / "artifacts"
    artifacts_dir.mkdir(parents=True)

    from setuptools.build_meta import build_sdist, build_wheel

    previous_cwd = Path.cwd()
    try:
        os.chdir(ROOT)
        build_sdist(str(artifacts_dir))
        build_wheel(str(artifacts_dir))
    finally:
        os.chdir(previous_cwd)

    artifacts = sorted(path for path in artifacts_dir.iterdir() if path.suffix == ".whl" or path.name.endswith(".tar.gz"))
    if len(artifacts) != 2 or not any(path.suffix == ".whl" for path in artifacts) or not any(path.name.endswith(".tar.gz") for path in artifacts):
        raise RuntimeError("expected exactly one wheel and one source distribution")
    package, version = package_metadata()
    records = [
        {"filename": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in artifacts
    ]
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "package": package,
        "version": version,
        "unpublished": True,
        "artifacts": records,
    }
    (output / "release-candidate-manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "SHA256SUMS").write_text(
        "".join(f"{record['sha256']}  artifacts/{record['filename']}\n" for record in records), encoding="utf-8"
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="empty/replaced directory outside this repository")
    arguments = parser.parse_args()
    manifest = build(arguments.output)
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
