"""Generate or verify a deterministic, offline supply-chain declaration inventory."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


_ACTION_RE = re.compile(r"^\s*(?:-\s+)?uses:\s+([^\s#]+)\s*$")
_USES_TOKEN = "uses:"
_PIP_INSTALL_RE = re.compile(r"^\s*python\s+-m\s+pip\s+install\s+(.+?)\s*$")
_FULL_SHA_RE = re.compile(r"^[^@\s]+@[0-9a-fA-F]{40}$")


def classify_action(reference: str) -> str:
    return "full_sha_format_unverified" if _FULL_SHA_RE.fullmatch(reference) else "mutable_or_unverified_reference"


def classify_requirement(requirement: str) -> str:
    if requirement.startswith("--") or requirement in {".", "./"}:
        return "local_or_flagged_install"
    return "version_range_unpinned"


def project_inventory(root: Path) -> dict[str, object]:
    data: dict[str, Any] = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    project = data.get("project", {})
    build_system = data.get("build-system", {})
    runtime = project.get("dependencies") or []
    optional = project.get("optional-dependencies") or {}
    if not isinstance(runtime, list) or not isinstance(optional, dict):
        raise ValueError("unsupported pyproject dependency declaration")
    optional_entries = [
        {"group": str(group), "requirements": sorted(str(item) for item in requirements)}
        for group, requirements in sorted(optional.items())
        if isinstance(requirements, list)
    ]
    if len(optional_entries) != len(optional):
        raise ValueError("unsupported optional dependency declaration")
    build_requirements = build_system.get("requires") or []
    if not isinstance(build_requirements, list):
        raise ValueError("unsupported build-system requirement declaration")
    return {
        "runtime_dependencies": sorted(str(item) for item in runtime),
        "optional_dependencies": optional_entries,
        "build_requirements": [
            {"requirement": str(item), "classification": classify_requirement(str(item))}
            for item in sorted(build_requirements)
        ],
    }


def workflow_inventory(root: Path) -> list[dict[str, object]]:
    workflows: list[dict[str, object]] = []
    directory = root / ".github" / "workflows"
    for path in sorted([*directory.glob("*.yml"), *directory.glob("*.yaml")]):
        uses: list[dict[str, str]] = []
        installs: list[dict[str, str]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if _USES_TOKEN in line:
                match = _ACTION_RE.fullmatch(line)
                if match is None or "${{" in line:
                    raise ValueError(f"unsupported workflow uses declaration: {path.relative_to(root).as_posix()}")
                reference = match.group(1)
                uses.append({"reference": reference, "classification": classify_action(reference)})
            install = _PIP_INSTALL_RE.fullmatch(line)
            if install is not None:
                command = install.group(1)
                if "${{" in command:
                    raise ValueError(f"unsupported dynamic pip command: {path.relative_to(root).as_posix()}")
                installs.append({"command": command, "classification": classify_requirement(command)})
        workflows.append({"path": path.relative_to(root).as_posix(), "uses": sorted(uses, key=lambda item: item["reference"]), "literal_package_installs": installs})
    return workflows


def build_manifest(root: Path) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "declaration_inventory",
        "project": project_inventory(root),
        "workflows": workflow_inventory(root),
        "limitations": [
            "not a lockfile",
            "not an SBOM",
            "not a provenance attestation",
            "offline declaration inventory only",
        ],
    }


def serialized_manifest(root: Path) -> bytes:
    return (json.dumps(build_manifest(root), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or verify an offline supply-chain declaration inventory.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        content = serialized_manifest(args.root.resolve(strict=True))
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"inventory error: {error}", file=sys.stderr)
        return 2
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(content)
        return 0
    try:
        existing = args.output.read_bytes()
    except OSError:
        existing = b""
    if existing != content:
        print("manifest drift: regenerate the reviewed inventory", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
