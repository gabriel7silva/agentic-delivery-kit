#!/usr/bin/env python3
"""L2 — every YAML the kit ships validates against its schema, plus the semantic
checks a schema cannot express (ids that must exist elsewhere, globs that must
not repeat, floors that must agree).

Usage: check_schemas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import model as M  # noqa: E402
from lib.diffscope import Ownership  # noqa: E402
from lib.report import Report  # noqa: E402


def validate(report: Report, schema_path: Path, data, label: str, sub: str | None = None) -> bool:
    schema = json.load(open(schema_path, encoding="utf-8"))
    if sub is not None:
        schema = {"$schema": schema.get("$schema"), "$defs": schema["$defs"], **schema["$defs"][sub]}
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    for e in errors:
        where = "/".join(str(p) for p in e.path) or "<root>"
        report.add(label, None, "schema", f"{where}: {e.message[:140]}")
    report.scanned += 1
    return not errors


def main() -> int:
    report = Report(check="check_schemas — YAML validates, ids resolve")
    S = M.SCHEMAS_DIR

    # core/model
    for f in sorted(M.MODEL_DIR.glob("*.yml")):
        validate(report, S / "model.schema.json", M.load_yaml(f), M.rel(f), sub=f.stem)

    # instance example(s)
    for f in [M.REPO_ROOT / "instance.example.yml", *sorted((M.REPO_ROOT / "examples").glob("instance-*.yml"))]:
        if f.is_file():
            validate(report, S / "instance.schema.json", M.load_yaml(f), M.rel(f))
    for f in sorted((M.REPO_ROOT / "profiles").glob("*/instance.example.yml")):
        validate(report, S / "instance.schema.json", M.load_yaml(f), M.rel(f))

    # tracks
    for t in M.track_dirs():
        mapping, caps = M.track(t.name)
        validate(report, S / "mapping.schema.json", mapping, M.rel(t / "mapping.yml"))
        validate(report, S / "capabilities.schema.json", caps, M.rel(t / "capabilities.yml"))

    # agents
    roster = M.load_yaml(M.REPO_ROOT / "agents" / "roster.yml")
    validate(report, S / "roster.schema.json", roster, "agents/roster.yml")
    agent_ids = {a["id"] for a in roster["agents"]}
    for a in roster["agents"]:
        if not (M.REPO_ROOT / a["brief"]).is_file():
            report.add("agents/roster.yml", None, "missing-brief", f"{a['id']}: {a['brief']} does not exist")

    own_data = M.load_yaml(M.REPO_ROOT / "agents" / "ownership.yml")
    if validate(report, S / "ownership.schema.json", own_data, "agents/ownership.yml"):
        own = Ownership(own_data)
        for scope in [*own.scopes, own.default]:
            if scope.writer not in agent_ids:
                report.add("agents/ownership.yml", None, "unknown-agent", f"scope {scope.id}: writer '{scope.writer}' not in roster")
            for r in scope.reviewers:
                if r not in agent_ids:
                    report.add("agents/ownership.yml", None, "unknown-agent", f"scope {scope.id}: reviewer '{r}' not in roster")
        for glob, a, b in own.duplicate_globs():
            report.add("agents/ownership.yml", None, "duplicate-glob", f"{glob!r} appears in scopes {a} and {b}")

    for f in [M.REPO_ROOT / "agents" / "concurrency.yml", *sorted((M.REPO_ROOT / "agents" / "policies").glob("*.yml"))]:
        validate(report, S / "policies.schema.json", M.load_yaml(f), M.rel(f))

    # escalation triggers cite existing rules; floors agree with ownership on shared globs
    rule_ids = M.rule_ids()
    esc = M.load_yaml(M.REPO_ROOT / "agents" / "policies" / "escalation.yml")
    for t in esc.get("triggers", []):
        if t["canon"] not in rule_ids:
            report.add("agents/policies/escalation.yml", None, "unknown-rule", f"trigger {t['id']}: canon {t['canon']} not in rules.yml")
    floors = M.load_yaml(M.REPO_ROOT / "agents" / "policies" / "risk-floors.yml")
    floor_by_glob = {p: f["floor"] for f in floors["floors"] for p in f["paths"]}
    for s in own_data["scopes"]:
        for g in s["paths"]:
            if g in floor_by_glob and floor_by_glob[g] != s["floor"]:
                report.add("agents/ownership.yml", None, "floor-mismatch", f"{g!r}: ownership says {s['floor']}, risk-floors says {floor_by_glob[g]}")

    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())
