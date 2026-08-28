#!/usr/bin/env python3
"""Create a redacted, read-only candidate scope audit outside a Git repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)
BANNED_SUFFIXES = {".pem", ".p12", ".pfx", ".key"}


def _git(repository: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _path_rule(relative: Path) -> str | None:
    parts = relative.parts
    name = relative.name
    if any(part in {".hermes", ".grapify", ".obsidian"} for part in parts):
        return "private-operational-state"
    if name == ".env" or name.startswith(".env."):
        return "environment-file"
    if name in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"} or relative.suffix.lower() in BANNED_SUFFIXES:
        return "private-key-file"
    return None


def _secret_rule(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    return "secret-pattern" if any(pattern.search(text) for pattern in SECRET_PATTERNS) else None


def _artifact_summary(manifest_path: Path | None) -> dict[str, object] | None:
    if manifest_path is None:
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {"schema_version", "package", "version", "unpublished", "artifacts"}
    if set(manifest) != required or manifest["schema_version"] != "1.0" or manifest["unpublished"] is not True:
        raise ValueError("artifact manifest is not an unpublished schema-1.0 release candidate")
    artifacts: list[dict[str, object]] = []
    for record in manifest["artifacts"]:
        if set(record) != {"filename", "bytes", "sha256"}:
            raise ValueError("artifact manifest record has an unexpected shape")
        filename = record["filename"]
        if not isinstance(filename, str) or Path(filename).name != filename:
            raise ValueError("artifact filename must be a basename")
        artifact = manifest_path.parent / "artifacts" / filename
        if not artifact.is_file() or artifact.stat().st_size != record["bytes"] or _sha256(artifact) != record["sha256"]:
            raise ValueError("artifact bytes or checksum do not match the manifest")
        artifacts.append(dict(record))
    return {"package": manifest["package"], "version": manifest["version"], "unpublished": True, "artifacts": artifacts}


def audit(repository: Path, output: Path, artifact_manifest: Path | None = None) -> dict[str, object]:
    repository = Path(_git(repository, "rev-parse", "--show-toplevel").strip()).resolve()
    output = output.resolve()
    if output == repository or repository in output.parents:
        raise ValueError("--output must be outside the repository")
    if artifact_manifest is not None:
        artifact_manifest = artifact_manifest.resolve()
        if artifact_manifest == repository or repository in artifact_manifest.parents:
            raise ValueError("--artifact-manifest must be outside the repository")

    tracked = [Path(item) for item in _git(repository, "ls-files", "-z").split("\0") if item]
    findings: list[dict[str, str]] = []
    for relative in tracked:
        rule = _path_rule(relative) or _secret_rule(repository / relative)
        if rule is not None:
            findings.append({"path": relative.as_posix(), "rule": rule})

    clean = not bool(_git(repository, "status", "--porcelain"))
    if not clean:
        findings.append({"path": "<working-tree>", "rule": "working-tree-not-clean"})
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "status": "PASS" if not findings else "FAIL",
        "commit": _git(repository, "rev-parse", "HEAD").strip(),
        "working_tree_clean": clean,
        "tracked_file_count": len(tracked),
        "findings": findings,
        "artifact_summary": _artifact_summary(artifact_manifest),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifact-manifest", type=Path)
    arguments = parser.parse_args()
    payload = audit(arguments.repository, arguments.output, arguments.artifact_manifest)
    print(json.dumps({"status": payload["status"], "output": str(arguments.output.resolve())}, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
