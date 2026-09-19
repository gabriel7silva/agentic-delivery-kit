#!/usr/bin/env python3
"""OPTIONAL — expand {{dotted.path}} placeholders from an instance file.

Adopters never need this: templates are readable unrendered. It exists for
people who want pre-filled templates to paste, and for generating examples.

Usage:
    render.py --instance instance.yml --out .render-out [paths...]
    (default paths: templates/)

Lists become comma-separated; missing paths are left as-is and reported.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import model as M  # noqa: E402

PLACEHOLDER = re.compile(r"\{\{([a-z0-9_.]+)\}\}")


def lookup(instance: dict, dotted: str):
    cur = instance
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def render_text(text: str, instance: dict, unresolved: set[str]) -> str:
    def sub(m: re.Match) -> str:
        v = lookup(instance, m.group(1))
        if v is None:
            unresolved.add(m.group(1))
            return m.group(0)
        if isinstance(v, list):
            return ", ".join(str(x) for x in v)
        return str(v)
    return PLACEHOLDER.sub(sub, text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--instance", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=M.REPO_ROOT / ".render-out")
    ap.add_argument("paths", nargs="*", type=Path, default=[M.REPO_ROOT / "templates"])
    a = ap.parse_args()

    instance = M.load_yaml(a.instance)
    unresolved: set[str] = set()
    count = 0
    for root in a.paths:
        files = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for f in files:
            if "_fragments" in f.parts:
                continue
            rel = f.relative_to(M.REPO_ROOT) if f.is_relative_to(M.REPO_ROOT) else Path(f.name)
            dest = a.out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(render_text(f.read_text(encoding="utf-8"), instance, unresolved), encoding="utf-8")
            count += 1
    print(f"rendered {count} file(s) into {a.out}")
    if unresolved:
        print("unresolved placeholders (left as-is):", ", ".join(sorted(unresolved)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
