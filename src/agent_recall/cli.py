from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import RecallError, render_packet, search_vault


def main(argv: list[str] | None = None) -> int:
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
