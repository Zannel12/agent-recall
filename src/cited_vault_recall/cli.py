from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import cast

from .core import MAX_LIMIT, RecallError, build_local_index, error_payload, render_packet, search_response_payload, search_vault


def _doctor_payload(configured_vault: Path | None) -> dict[str, object]:
    """Report bounded local readiness without discovering or exposing paths."""
    install_code = "READY" if Path(sys.executable).is_file() else "EXECUTABLE_UNAVAILABLE"
    install = {"ok": install_code == "READY", "code": install_code}
    local_state = {"discovered": False}
    if configured_vault is None:
        return {
            "status": "NOT_READY",
            "install": install,
            "vault": {"configured": False, "accessible": False, "readable": False, "code": "VAULT_NOT_CONFIGURED"},
            "ignore": {"configured": False, "code": "NOT_RUN", "skipped_files": 0},
            "search": {"code": "NOT_RUN", "hits": 0},
            "local_state": local_state,
        }
    if not configured_vault.is_dir():
        return {
            "status": "NOT_READY",
            "install": install,
            "vault": {"configured": True, "accessible": False, "readable": False, "code": "VAULT_NOT_FOUND"},
            "ignore": {"configured": False, "code": "NOT_RUN", "skipped_files": 0},
            "search": {"code": "NOT_RUN", "hits": 0},
            "local_state": local_state,
        }
    if not os.access(configured_vault, os.R_OK | os.X_OK):
        return {
            "status": "NOT_READY",
            "install": install,
            "vault": {"configured": True, "accessible": True, "readable": False, "code": "VAULT_NOT_READABLE"},
            "ignore": {"configured": False, "code": "NOT_RUN", "skipped_files": 0},
            "search": {"code": "NOT_RUN", "hits": 0},
            "local_state": local_state,
        }
    diagnostics: dict[str, int] = {}
    try:
        hits = search_vault(configured_vault, "privacy", 1, diagnostics)
    except (RecallError, OSError, UnicodeDecodeError, ValueError):
        return {
            "status": "NOT_READY",
            "install": install,
            "vault": {"configured": True, "accessible": True, "readable": True, "code": "READY"},
            "ignore": {"configured": (configured_vault / ".recallignore").is_file(), "code": "NOT_RUN", "skipped_files": 0},
            "search": {"code": "DOCTOR_SEARCH_FAILED", "hits": 0},
            "local_state": local_state,
        }
    ready = install_code == "READY"
    return {
        "status": "READY" if ready else "NOT_READY",
        "install": install,
        "vault": {"configured": True, "accessible": True, "readable": True, "code": "READY"},
        "ignore": {"configured": (configured_vault / ".recallignore").is_file(), "code": "READY", "skipped_files": diagnostics["skipped_files"]},
        "search": {"code": "READY", "hits": len(hits)},
        "local_state": local_state,
    }


def main(argv: list[str] | None = None) -> int:
    arguments = argv if argv is not None else __import__("sys").argv[1:]
    if arguments[:1] == ["reindex"]:
        parser = argparse.ArgumentParser(description="Explicitly rebuild a derived local index.")
        parser.add_argument("reindex")
        parser.add_argument("--vault", required=True, type=Path)
        parser.add_argument("--destination", required=True, type=Path)
        parser.add_argument("--json", action="store_true")
        args = parser.parse_args(arguments)
        try:
            index = build_local_index(args.vault, args.destination)
        except (RecallError, ValueError) as error:
            parser.error(str(error))
        payload = {"reindexed": True, "index_version": index["index_version"], "records": len(cast(list[object], index["records"]))}
        print(json.dumps(payload, sort_keys=True) if args.json else "reindex: complete")
        return 0

    if arguments[:1] == ["doctor"]:
        parser = argparse.ArgumentParser(description="Check explicit local Cited Vault Recall configuration.")
        parser.add_argument("doctor")
        parser.add_argument("--vault", type=Path)
        parser.add_argument("--config", type=Path)
        parser.add_argument("--json", action="store_true")
        args = parser.parse_args(arguments)
        configured_vault = args.vault
        if args.config is not None:
            try:
                configured_vault = Path(json.loads(args.config.read_text(encoding="utf-8"))["vault"])
            except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError):
                configured_vault = None
        payload = _doctor_payload(configured_vault)
        if args.json:
            print(json.dumps(payload, sort_keys=True))
        else:
            print(f"doctor: {cast(str, payload['status']).lower()}")
        return 0 if payload["status"] == "READY" else 1

    parser = argparse.ArgumentParser(description="Create cited context packets from a local Markdown vault.")
    parser.add_argument("vault", type=Path, help="Local Markdown vault directory")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=8, help=f"Maximum hits (1-{MAX_LIMIT}, default: 8)")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--russian-lexical-expansion", action="store_true", help="Opt in to deterministic Russian lexical expansion")
    args = parser.parse_args(argv)
    diagnostics: dict[str, int] = {}
    try:
        hits = search_vault(args.vault, args.query, args.limit, diagnostics, russian_lexical_expansion=args.russian_lexical_expansion)
    except ValueError as error:
        code = error.code if isinstance(error, RecallError) else "INVALID_ARGUMENT"
        if args.format == "json":
            print(json.dumps(error_payload(code, str(error)), indent=2))
            return 2
        parser.error(f"{code}: {error}")
    if args.format == "json":
        print(json.dumps(search_response_payload(args.query, hits, diagnostics), indent=2))
    else:
        print(render_packet(args.query, hits), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
