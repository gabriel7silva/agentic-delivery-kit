#!/usr/bin/env python3
"""Skeleton generator. Replace `render()` with your runtime's artifact shape.

    python generate.py          # writes out/
    python generate.py --check  # exit 1 on drift
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_contract"))
import base  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"


def render(agent: dict) -> str:
    """One artifact for one agent. The brief goes in VERBATIM — wrap it, never rewrite it."""
    header = f"# {agent['id']}\n\nkind: {agent['kind']}\n\n"       # <— your runtime's front-matter here
    body = base.brief_text(agent)
    tail = ""
    if agent["kind"] == "reviewer":
        tail = "\n\n## Verdict shape\n\n```\n" + base.verdict_shape() + "\n```\n"
    return header + body + tail


def generate() -> dict[str, str]:
    agents = base.load_roster()
    # Map agent id → the file name your runtime expects. Keep it deterministic.
    return {f"{a['id']}.md": render(a) for a in agents}


if __name__ == "__main__":
    raise SystemExit(base.run(generate, OUT))
