#!/usr/bin/env python3
"""Generate an SPDX 2.3 SBOM for an exact unpublished release-candidate manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]
CREATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_artifacts(manifest_path: Path) -> tuple[str, str, list[dict[str, Any]]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {"schema_version", "package", "version", "unpublished", "artifacts"}
    if set(manifest) != required or manifest["schema_version"] != "1.0" or manifest["unpublished"] is not True:
        raise ValueError("artifact manifest is not an unpublished schema-1.0 release candidate")
    package, version = manifest["package"], manifest["version"]
    if not isinstance(package, str) or not isinstance(version, str) or not isinstance(manifest["artifacts"], list):
        raise ValueError("artifact manifest has invalid package metadata")
    artifacts: list[dict[str, Any]] = []
    for record in manifest["artifacts"]:
        if set(record) != {"filename", "bytes", "sha256"}:
            raise ValueError("artifact manifest record has an unexpected shape")
        filename, size, digest = record["filename"], record["bytes"], record["sha256"]
        if not isinstance(filename, str) or Path(filename).name != filename or not isinstance(size, int) or not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            raise ValueError("artifact manifest record is invalid")
        path = manifest_path.parent / "artifacts" / filename
        if not path.is_file() or path.stat().st_size != size or sha256(path) != digest:
            raise ValueError("artifact bytes or checksum do not match the manifest")
        artifacts.append({"filename": filename, "bytes": size, "sha256": digest})
    if len(artifacts) != 2:
        raise ValueError("expected exactly two release artifacts")
    return package, version, sorted(artifacts, key=lambda item: item["filename"])


def build_spdx(package: str, version: str, artifacts: list[dict[str, Any]], created: str) -> dict[str, Any]:
    primary_digest = artifacts[0]["sha256"]
    package_id = "SPDXRef-Package-CitedVaultRecall"
    files = []
    relationships = [{"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": package_id}]
    for number, artifact in enumerate(artifacts, start=1):
        file_id = f"SPDXRef-File-Artifact{number}"
        files.append(
            {
                "SPDXID": file_id,
                "fileName": f"artifacts/{artifact['filename']}",
                "checksums": [{"algorithm": "SHA256", "checksumValue": artifact["sha256"]}],
                "licenseConcluded": "NOASSERTION",
                "licenseInfoInFiles": ["NOASSERTION"],
                "copyrightText": "NOASSERTION",
                "fileTypes": ["BINARY" if artifact["filename"].endswith(".whl") else "SOURCE"],
            }
        )
        relationships.append({"spdxElementId": package_id, "relationshipType": "CONTAINS", "relatedSpdxElement": file_id})
    document_namespace = f"https://spdx.org/spdxdocs/{package}-{primary_digest}"
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"{package}-{version}-unpublished-sbom",
        "documentNamespace": document_namespace,
        "creationInfo": {"created": created, "creators": ["Tool: cited-vault-recall-sbom-1.0"]},
        "packages": [
            {
                "SPDXID": package_id,
                "name": package,
                "versionInfo": version,
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "MIT",
                "licenseDeclared": "MIT",
                "copyrightText": "NOASSERTION",
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": f"pkg:pypi/{package}@{version}",
                    }
                ],
                "comment": "unpublished local release candidate; exact wheel and sdist checksums are represented as SPDX files",
            }
        ],
        "files": files,
        "relationships": relationships,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--created", required=True, help="UTC timestamp, e.g. 2026-08-28T00:00:00Z")
    arguments = parser.parse_args()
    try:
        if not CREATED_RE.fullmatch(arguments.created):
            raise ValueError("--created must be a UTC timestamp in YYYY-MM-DDTHH:MM:SSZ format")
        output = arguments.output.resolve()
        if output == ROOT or ROOT in output.parents:
            raise ValueError("--output must be outside the repository")
        package, version, artifacts = load_artifacts(arguments.artifact_manifest.resolve(strict=True))
        payload = build_spdx(package, version, artifacts, arguments.created)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"sbom error: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"output": str(output), "spdxVersion": payload["spdxVersion"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
