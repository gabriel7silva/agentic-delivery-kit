#!/usr/bin/env python3
"""Print the name of an iteration from the instance's pattern — RULE-ITERATION-NAMING.

    iteration_name.py --start 2026-01-12                 # Sprint 02 26 Q1 Acme Portal
    iteration_name.py --start 2026-01-12 --seq 2 --json  # name, dates, sprint-close date
    iteration_name.py --instance examples/instance-internal-github.yml --start 2026-09-21

Reads cadence.iteration_name_pattern, cadence.sequence_resets, cadence.iteration_length_days,
cadence.iteration_start_day, cadence.sprint_close and organization.product from instance.yml
(--instance, ./instance.yml, or the adopter's root next to .pact/), falling back to the model's
defaults (core/model/iterations.yml → naming) and the kit's start/close days. --seq is derived
for seven-day iterations with a year or quarter reset; otherwise pass it. Exit 2 on any problem.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import iteration_name as IN  # noqa: E402
from lib import model as M  # noqa: E402


def adopter_root() -> Path:
    return M.REPO_ROOT.parent if M.REPO_ROOT.name == ".pact" else M.REPO_ROOT


def discover_instance(explicit: str | None) -> Path | None:
    if explicit:
        return Path(explicit)
    for candidate in (Path("instance.yml"), adopter_root() / "instance.yml"):
        if candidate.is_file():
            return candidate
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Render an iteration name from the instance's pattern.")
    ap.add_argument("--instance", help="instance.yml (default: ./instance.yml or the adopter's root)")
    ap.add_argument("--start", required=True, help="start date of the iteration, YYYY-MM-DD")
    ap.add_argument("--seq", type=int, help="sequence number; derived for seven-day iterations when omitted")
    ap.add_argument("--json", action="store_true", help="print name, seq, dates and the sprint-close date as JSON")
    args = ap.parse_args()

    path = discover_instance(args.instance)
    if path is None or not path.is_file():
        print("iteration_name: no instance.yml found — pass --instance", file=sys.stderr)
        return 2
    data = M.load_yaml(path) or {}
    cadence = data.get("cadence") or {}
    defaults = IN.naming_defaults()
    pattern = cadence.get("iteration_name_pattern") or defaults["pattern"]
    resets = cadence.get("sequence_resets") or defaults["sequence_resets"]
    length = int(cadence.get("iteration_length_days") or 7)
    start_day = cadence.get("iteration_start_day") or IN.DEFAULT_START_DAY
    sprint_close = cadence.get("sprint_close") or IN.DEFAULT_SPRINT_CLOSE
    product = (data.get("organization") or {}).get("product")

    try:
        start = dt.date.fromisoformat(args.start)
        seq = args.seq if args.seq is not None else IN.derive_seq(start, start_day, resets, length)
        name = IN.render_name(pattern, seq=seq, start=start, length_days=length, product=product)
        close = IN.close_date(start, length, sprint_close)
    except ValueError as exc:
        print(f"iteration_name: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({
            "name": name,
            "seq": seq,
            "start": start.isoformat(),
            "end": IN.end_of(start, length).isoformat(),
            "sprint_close_date": close.isoformat(),
            "quarter": IN.quarter_of(start),
            "half": IN.half_of(start),
            "pattern": pattern,
        }, ensure_ascii=False))
    else:
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
