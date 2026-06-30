"""Command-line interface for okf-tool."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .document import read
from .index import regenerate
from .links import validate
from .log import append
from .paths import bundle_root
from .viewer import generate


def _cmd_index(args: argparse.Namespace) -> int:
    for path in regenerate(Path(args.cwd)):
        print(f"updated {path}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    result = validate(Path(args.cwd))
    broken = result.get("broken", [])
    orphans = result.get("orphans", [])

    if broken:
        print("Broken links:")
        for b in broken:
            print(f"  {b}")
    if orphans:
        print("Orphan concepts:")
        for o in orphans:
            print(f"  {o}")
    if not broken and not orphans:
        print("OK: no broken links or orphan concepts")
        return 0
    return 1


def _cmd_log(args: argparse.Namespace) -> int:
    append(args.message, Path(args.cwd))
    print("log entry appended")
    return 0


def _cmd_viz(args: argparse.Namespace) -> int:
    out = generate(Path(args.cwd), Path(args.output) if args.output else None)
    print(f"generated {out}")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    path = Path(args.path)
    doc = read(path)
    print(f"---\n{doc.frontmatter}\n---\n{doc.body}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="okf-tool", description="OKF bundle helper")
    parser.add_argument("--cwd", default=".", help="repo root")
    parser.add_argument("--version", action="version", version=f"okf-tool {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("index", help="regenerate all index.md files")
    sub.add_parser("validate", help="check frontmatter and links")

    p_log = sub.add_parser("log", help="append a log entry")
    p_log.add_argument("message", help="log message")

    p_viz = sub.add_parser("viz", help="generate viz.html")
    p_viz.add_argument("-o", "--output", help="output path")

    p_show = sub.add_parser("show", help="show a concept file")
    p_show.add_argument("path", help="path to concept markdown file")

    args = parser.parse_args(argv)
    handlers = {
        "index": _cmd_index,
        "validate": _cmd_validate,
        "log": _cmd_log,
        "viz": _cmd_viz,
        "show": _cmd_show,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
