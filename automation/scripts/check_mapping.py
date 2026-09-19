#!/usr/bin/env python3
"""L2 — every track covers 100 % of the neutral symbols and keeps its promises;
and the compatibility matrix on disk matches what the data says.

Usage:
    check_mapping.py                 # verify tracks and that the matrix is current
    check_mapping.py --write-matrix  # regenerate docs/compatibility-matrix.md
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import model as M  # noqa: E402
from lib.report import Report  # noqa: E402

MATRIX_PATH = M.REPO_ROOT / "docs" / "compatibility-matrix.md"


def check_track(report: Report, name: str) -> None:
    base = M.TRACKS_DIR / name
    label = f"tracks/{name}"
    mapping, caps = M.track(name)
    report.scanned += 1

    for req in ("README.md", "mapping.yml", "capabilities.yml", "fields.md", "setup.md"):
        if not (base / req).is_file():
            report.add(label, None, "contract", f"missing required file {req}")

    have = set(mapping["symbols"])
    want = M.symbols()
    for s in sorted(want - have):
        report.add(f"{label}/mapping.yml", None, "coverage", f"symbol {s} not mapped")
    for s in sorted(have - want):
        report.add(f"{label}/mapping.yml", None, "coverage", f"unknown symbol {s} (not in core/model)")

    for sym, expected in (("WI_STATE", set(M.states())), ("STATUS", set(M.columns()))):
        values = mapping["symbols"].get(sym, {}).get("values") or {}
        if set(values) != expected:
            report.add(f"{label}/mapping.yml", None, "values", f"{sym} values {sorted(values)} != {sorted(expected)}")
        missing = [k for k, v in values.items() if v is None]
        if missing:
            report.add(f"{label}/mapping.yml", None, "values", f"{sym}: {missing} mapped to null (not represented)")
    st = (mapping["symbols"].get("WI_STATE", {}).get("values") or {})
    resolved_values = {st.get(s) for s in M.states_in("RESOLVED") if st.get(s) is not None}
    closed_values = {st.get(s) for s in M.states_in("CLOSED") if st.get(s) is not None}
    for shared in sorted(resolved_values & closed_values):
        report.add(f"{label}/mapping.yml", None, "resolved-eq-closed", f"a Resolved-category state and Closed both map to {shared!r} — RULE-STATE-RESOLVED-NOT-CLOSED cannot be enforced")

    c = caps["capabilities"]
    if set(c) != set(M.capability_ids()):
        report.add(f"{label}/capabilities.yml", None, "vocabulary", "capability keys differ from core/model/capabilities.yml")
    if c.get("sot_eligible") and not (c.get("durable_history") and c.get("comments")):
        report.add(f"{label}/capabilities.yml", None, "sot", "sot_eligible requires durable_history and comments")
    if not all(c.values()) and not (base / "substitutes.md").is_file():
        report.add(label, None, "contract", "a capability is false but substitutes.md is missing")


def status_for(rule: dict, caps: dict, has_substitutes: bool) -> str:
    missing = [c for c in rule["requires"] if not caps["capabilities"].get(c, False)]
    if not missing:
        return "supported"
    return "substituted" if has_substitutes else "unsupported"


def render_matrix() -> str:
    tracks = [t.name for t in M.track_dirs()]
    caps = {t: M.track(t)[1] for t in tracks}
    subs = {t: (M.TRACKS_DIR / t / "substitutes.md").is_file() for t in tracks}
    lines = [
        "# Compatibility matrix",
        "",
        "**Generated** by `automation/scripts/check_mapping.py --write-matrix`. Do not edit by hand —",
        "edit `core/model/rules.yml` (what a rule requires) or `tracks/<name>/capabilities.yml` (what a",
        "tool can do) and regenerate. `make mapping` fails if this file is stale.",
        "",
        "| Status | Meaning |",
        "|---|---|",
        "| ✅ supported | every capability the rule requires is native to the tool |",
        "| ⚠️ substituted | a capability is missing and the track declares a substitute in `substitutes.md` — the rule works, with the stated loss |",
        "| ❌ unsupported | a capability is missing and nothing stands in for it |",
        "",
        "| Rule | Requires | " + " | ".join(tracks) + " |",
        "|---|---|" + "|".join("---" for _ in tracks) + "|",
    ]
    icon = {"supported": "✅", "substituted": "⚠️", "unsupported": "❌"}
    for r in M.rules():
        req = ", ".join(r["requires"]) or "—"
        cells = [icon[status_for(r, caps[t], subs[t])] for t in tracks]
        opt = " *(optional)*" if r.get("optional") else ""
        lines.append(f"| `{r['id']}`{opt} | {req} | " + " | ".join(cells) + " |")
    sot = []
    for t in tracks:
        sot.append("✅" if caps[t]["capabilities"].get("sot_eligible") else "❌")
    lines += [
        "",
        "## Source of truth",
        "",
        "A column of ⚠️ does **not** make a track a source of truth. Slack is never SoT",
        "(`sot_eligible: false`); the instance check rejects it there.",
        "",
        "| | " + " | ".join(tracks) + " |",
        "|---|" + "|".join("---" for _ in tracks) + "|",
        "| `sot_eligible` | " + " | ".join(sot) + " |",
        "",
        "## Reading it",
        "",
        "A column with many ⚠️ is a track that works with people doing what the tool will not enforce.",
        "A column with any ❌ on a non-optional rule is a track that cannot run PACT alone — pair it with",
        "one that can. Slack has no ❌ in the rule rows above because no rule `requires: [sot_eligible]`;",
        "the eligibility row is the one that says it cannot be the board.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if "--write-matrix" in sys.argv:
        MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
        MATRIX_PATH.write_text(render_matrix(), encoding="utf-8", newline="\n")
        print(f"wrote {M.rel(MATRIX_PATH)}")
        return 0

    report = Report(check="check_mapping — track coverage and the compatibility matrix")
    for t in M.track_dirs():
        check_track(report, t.name)
    expected = render_matrix()
    if not MATRIX_PATH.is_file():
        report.add(M.rel(MATRIX_PATH), None, "matrix", "missing — run: make matrix")
    elif MATRIX_PATH.read_text(encoding="utf-8").replace("\r\n", "\n") != expected:
        report.add(M.rel(MATRIX_PATH), None, "matrix", "stale — run: make matrix")
    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())
