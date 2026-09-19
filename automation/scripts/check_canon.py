#!/usr/bin/env python3
"""L5 — anti-duplication: every fenced fragment copy matches its source byte for
byte, every {{placeholder}} resolves in instance.example.yml, and canon lives
only in core/.

Usage:
    check_canon.py          # verify
    check_canon.py --fix    # rewrite fenced copies from their fragments
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import model as M  # noqa: E402
from lib.report import Report  # noqa: E402

ROOT = M.REPO_ROOT
FRAGMENTS = ROOT / "templates" / "_fragments"
FENCE = re.compile(r"(<!-- canon:begin fragment=([\w-]+) -->\n)(.*?)(\n<!-- canon:end -->)", re.S)
PLACEHOLDER = re.compile(r"\{\{([a-z0-9_.]+)\}\}")
FRONT_CANON = re.compile(r"\A---\n.*?^canon:\s*true\s*$.*?\n---", re.S | re.M)
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}


def resolve(instance: dict, dotted: str) -> bool:
    cur = instance
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return False
        cur = cur[key]
    return True


def main() -> int:
    fix = "--fix" in sys.argv
    report = Report(check="check_canon — fenced copies, placeholders, canon location")
    fragments = {p.stem: p.read_text(encoding="utf-8").rstrip("\n") for p in FRAGMENTS.glob("*.md")}
    instance = M.load_yaml(ROOT / "instance.example.yml")

    for f in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in f.parts) or FRAGMENTS in f.parents:
            continue
        text = f.read_text(encoding="utf-8")
        report.scanned += 1
        changed = False

        def replace(m: re.Match) -> str:
            nonlocal changed
            name, body = m.group(2), m.group(3)
            if name not in fragments:
                report.add(M.rel(f), None, "unknown-fragment", f"fragment '{name}' has no source in templates/_fragments/")
                return m.group(0)
            if body != fragments[name]:
                if fix:
                    changed = True
                    return f"{m.group(1)}{fragments[name]}{m.group(4)}"
                report.add(M.rel(f), None, "fence-diverged", f"fenced copy of '{name}' differs from templates/_fragments/{name}.md (run: make fix-canon)")
            return m.group(0)

        new_text = FENCE.sub(replace, text)
        if fix and changed:
            f.write_text(new_text, encoding="utf-8")

        for lineno, line in enumerate(text.splitlines(), start=1):
            for var in PLACEHOLDER.findall(line):
                if not resolve(instance, var):
                    report.add(M.rel(f), lineno, "unknown-placeholder", f"{{{{{var}}}}} has no path in instance.example.yml")

        if FRONT_CANON.search(text) and (ROOT / "core") not in f.parents:
            report.add(M.rel(f), 1, "canon-outside-core", "front-matter says canon: true but the file is not under core/")

    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())
