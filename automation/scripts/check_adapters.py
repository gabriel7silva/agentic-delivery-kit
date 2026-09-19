#!/usr/bin/env python3
"""L5 — every adapter's out/ matches a fresh generation.

Replaces the Makefile bash `for`/`case` loop so `make adapters` works on Windows
without a POSIX shell.

Usage: check_adapters.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    generators = sorted(
        p for p in (REPO_ROOT / "adapters").glob("*/generate.py")
        if "_template" not in p.parts
    )
    if not generators:
        print("FAIL  no adapter generate.py found", file=sys.stderr)
        return 1
    for gen in generators:
        proc = subprocess.run([sys.executable, str(gen), "--check"], cwd=REPO_ROOT)
        if proc.returncode != 0:
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
