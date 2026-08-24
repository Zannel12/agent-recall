from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import render_packet, search_vault


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create cited context packets from a local Markdown vault.")
    parser.add_argument("vault", type=Path, help="Local Markdown vault directory")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=8, help="Maximum hits (default: 8)")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    try:
        hits = search_vault(args.vault, args.query, args.limit)
    except ValueError as error:
        parser.error(str(error))
    if args.format == "json":
        print(json.dumps({"query": args.query, "hits": [hit.__dict__ for hit in hits]}, indent=2))
    else:
        print(render_packet(args.query, hits), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
