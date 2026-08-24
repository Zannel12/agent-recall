from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import RecallError, render_packet, search_vault


def main(argv: list[str] | None = None) -> int:
    arguments = argv if argv is not None else __import__("sys").argv[1:]
    if arguments[:1] == ["doctor"]:
        parser = argparse.ArgumentParser(description="Check explicit local Agent Recall configuration.")
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
        payload = {
            "install": {"ok": True},
            "vault": {"configured": configured_vault is not None, "accessible": configured_vault.is_dir() if configured_vault else False},
            "local_state": {"discovered": False},
        }
        if args.json:
            print(json.dumps(payload, sort_keys=True))
        else:
            print("doctor: ok" if payload["vault"]["accessible"] else "doctor: vault not configured")
        return 0 if payload["vault"]["accessible"] else 1

    parser = argparse.ArgumentParser(description="Create cited context packets from a local Markdown vault.")
    parser.add_argument("vault", type=Path, help="Local Markdown vault directory")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=8, help="Maximum hits (default: 8)")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    diagnostics: dict[str, int] = {}
    try:
        hits = search_vault(args.vault, args.query, args.limit, diagnostics)
    except ValueError as error:
        code = error.code if isinstance(error, RecallError) else "INVALID_ARGUMENT"
        parser.error(f"{code}: {error}")
    if args.format == "json":
        print(json.dumps({"query": args.query, "hits": [hit.__dict__ for hit in hits], "diagnostics": diagnostics}, indent=2))
    else:
        print(render_packet(args.query, hits), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
