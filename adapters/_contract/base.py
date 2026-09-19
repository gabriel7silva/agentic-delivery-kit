"""Shared helpers for adapters: load the roster, read briefs verbatim, write a
deterministic output tree, detect drift. An adapter imports this and nothing
else from the kit.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import yaml

KIT_ROOT = Path(__file__).resolve().parents[2]
AGENTS = KIT_ROOT / "agents"


def load_roster() -> list[dict]:
    with open(AGENTS / "roster.yml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)["agents"]


def brief_text(agent: dict) -> str:
    """The brief, verbatim. Adapters wrap it; they never rewrite it."""
    return (KIT_ROOT / agent["brief"]).read_text(encoding="utf-8").rstrip("\n")


def verdict_shape() -> str:
    """The block every reviewer must return, as text an agent can copy."""
    with open(KIT_ROOT / "core" / "model" / "review-gates.yml", encoding="utf-8") as fh:
        vs = yaml.safe_load(fh)["verdict_shape"]
    return (
        "verdict: " + " | ".join(vs["verdict"]) + "\n"
        "risk: " + " | ".join(vs["risk"]) + "\n"
        "findings:\n"
        "  - severity: " + " | ".join(vs["finding"]["severity"]) + "\n"
        "    where: <path or acceptance criterion>\n"
        "    what: <one sentence: what is wrong and what would fix it>"
    )


def write_tree(out_dir: Path, files: dict[str, str]) -> None:
    """Replace out_dir with exactly these files. Deterministic: sorted, LF, trailing newline."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    for rel, text in sorted(files.items()):
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def check_drift(out_dir: Path, files: dict[str, str]) -> int:
    """Compare generated text with committed out_dir. Newlines are normalised so
    Windows checkouts (CRLF) still match a LF generation."""
    if not out_dir.exists():
        print(f"DRIFT  {out_dir} does not exist — run: python generate.py")
        return 1
    want = {name.replace("\\", "/"): (text.rstrip("\n") + "\n").replace("\r\n", "\n") for name, text in files.items()}
    have = {
        p.relative_to(out_dir).as_posix(): p.read_text(encoding="utf-8").replace("\r\n", "\n")
        for p in out_dir.rglob("*") if p.is_file()
    }
    diff = [f"{n}  (changed)" for n in sorted(set(want) & set(have)) if want[n] != have[n]]
    diff += [f"{n}  (missing from out/)" for n in sorted(set(want) - set(have))]
    diff += [f"{n}  (stale in out/)" for n in sorted(set(have) - set(want))]
    if diff:
        print(f"DRIFT  {out_dir.relative_to(KIT_ROOT)} differs from a fresh generation:")
        for d in diff:
            print(f"  {d}")
        print("  run: python generate.py")
        return 1
    print(f"OK     {out_dir.relative_to(KIT_ROOT)} is current")
    return 0


def run(generate, out_dir: Path) -> int:
    """Standard main(): `generate()` returns {relpath: text}; --check compares instead of writing."""
    files = generate()
    if "--check" in sys.argv:
        return check_drift(out_dir, files)
    write_tree(out_dir, files)
    print(f"wrote {len(files)} file(s) to {out_dir.relative_to(KIT_ROOT)}")
    return 0
