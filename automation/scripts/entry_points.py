#!/usr/bin/env python3
"""One entry point, many pointers — generate or check the runtime pointer files.

    entry_points.py                       # rewrite the kit's own pointers (AGENTS.md is the entry point)
    entry_points.py --check               # refuse a pointer that is missing or edited by hand (make entry)
    entry_points.py --list                # every runtime and the file it reads
    entry_points.py --root . --kit .pact  # an adopter's repository with the kit vendored at .pact/
    entry_points.py --root . --kit .      # an adopter's repository with the kit copied out

Every pointer says the same two things: read AGENTS.md at the root, and a setup starts with the
interview, one block per turn, no file before the person confirms. Runtimes that read AGENTS.md
natively need none of them; the rest each get their own file, from one template
(automation/scripts/lib/entry_points.py).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import entry_points as EP  # noqa: E402
from lib import model as M  # noqa: E402
from lib.report import Report  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate or check the runtime pointer files.")
    ap.add_argument("--root", help="folder the runtimes open (default: this kit)")
    ap.add_argument("--kit", default=".", help="where the kit lives under --root: '.' (this repository, or copied out) or '.pact'")
    ap.add_argument("--check", action="store_true", help="report drift instead of writing")
    ap.add_argument("--list", action="store_true", help="list runtimes and pointer paths")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else M.REPO_ROOT
    prefix = EP.kit_prefix(args.kit)

    if args.list:
        width = max(len(p.runtime) for p in EP.POINTERS)
        for p in EP.POINTERS:
            print(f"{p.runtime:<{width}}  {p.path}")
        print(f"\nread {EP.ENTRY_POINT} natively, no pointer needed: {', '.join(EP.NATIVE_READERS)}")
        return 0

    if args.check:
        report = Report(check="check_entry_points — every runtime pointer file is current")
        report.scanned = len(EP.POINTERS)
        for path, problem in EP.drift(root, prefix):
            rel = M.rel(path) if root == M.REPO_ROOT else str(path.relative_to(root))
            report.add(rel, None, "pointer-" + problem.split()[0], f"{problem} — run {EP.GENERATOR}; never edit a pointer by hand")
        return report.emit()

    written = EP.write_all(root, prefix)
    print(f"wrote {len(written)} pointer files under {root} (kit: {args.kit}); entry point: {EP.ENTRY_POINT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
