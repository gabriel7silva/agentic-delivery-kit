#!/usr/bin/env python3
"""L6 — adoption: an instance file is complete and coherent with the kit.

Checks, per instance file:
  - validates against schemas/instance.schema.json
  - source_of_truth.track exists under tracks/ and is sot_eligible
  - every mirror track exists; a mirror with purpose notifications may be any track
  - optional_rules keys are rules marked optional: true in core/model/rules.yml
  - the profile exists under profiles/ and its profile.yml toggles only optional rules
  - the instance may not lower a profile toggle that is true
  - homologation hats/env are required when the *effective* toggle (profile overlay + instance) is on
  - lifecycle.states (when present) names only states from core/model/item-states.yml and keeps
    every category — a state may be dropped or relabelled, a category never
  - topology agrees with roles: agent-to-agent needs an agent orchestrator; independent-agents
    has no agent orchestrator (a person dispatches)
  - the risk policy file exists
  - cadence: the iteration name pattern uses only known placeholders, {product} has an
    organization.product behind it, and the start day and the sprint close are working days that
    differ (RULE-ITERATION-NAMING, RULE-CEREMONY-SPRINT-CLOSE)

Usage: check_instance.py [instance.yml ...]
       with no args: instance.example.yml, examples/instance-*.yml,
       profiles/*/instance.example.yml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import iteration_name as IN  # noqa: E402
from lib import model as M  # noqa: E402
from lib.report import Report  # noqa: E402


def check(report: Report, path: Path) -> None:
    label = M.rel(path)
    report.scanned += 1
    data = M.load_yaml(path)
    schema = json.load(open(M.SCHEMAS_DIR / "instance.schema.json", encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(data))
    for e in errors:
        report.add(label, None, "schema", f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message[:140]}")
    if errors:
        return

    track_names = {t.name for t in M.track_dirs()}
    sot = data["source_of_truth"]["track"]
    if sot not in track_names:
        report.add(label, None, "unknown-track", f"source_of_truth.track '{sot}' is not under tracks/")
    else:
        _, caps = M.track(sot)
        if not caps["capabilities"].get("sot_eligible"):
            report.add(label, None, "sot-not-eligible", f"track '{sot}' declares sot_eligible: false — it can be a mirror, never the source of truth")
    for m in data.get("mirrors", []):
        if m["track"] not in track_names:
            report.add(label, None, "unknown-track", f"mirror track '{m['track']}' is not under tracks/")
        if m["track"] == sot:
            report.add(label, None, "mirror-is-sot", f"'{sot}' is listed as both source of truth and mirror")

    optional = {r["instance_key"]: r["id"] for r in M.rules() if r.get("optional") and r.get("instance_key")}
    for key in data.get("optional_rules", {}):
        if key not in optional:
            report.add(label, None, "not-optional", f"optional_rules.{key}: no rule with optional: true has this instance_key")

    profile = data["organization"]["profile"]
    pfile = M.REPO_ROOT / "profiles" / profile / "profile.yml"
    profile_rules: dict = {}
    if not pfile.is_file():
        report.add(label, None, "unknown-profile", f"profiles/{profile}/profile.yml does not exist")
    else:
        pdata = M.load_yaml(pfile)
        profile_rules = dict(pdata.get("optional_rules") or {})
        for key in profile_rules:
            if key not in optional:
                report.add(M.rel(pfile), None, "profile-redefines", f"toggles '{key}', which is not an optional rule — profiles may only toggle optional rules")
        instance_rules = data.get("optional_rules") or {}
        for key, val in profile_rules.items():
            if val is True and instance_rules.get(key) is False:
                report.add(label, None, "profile-contradiction", f"optional_rules.{key}: profile '{profile}' sets true; the instance may not lower it")

    policy = M.REPO_ROOT / data["risk"]["policy_file"]
    if not policy.is_file():
        report.add(label, None, "missing-policy", f"risk.policy_file {data['risk']['policy_file']} does not exist")

    roster = M.REPO_ROOT / data["roles"]["reviewers"]["roster"]
    if not roster.is_file():
        report.add(label, None, "missing-roster", f"roles.reviewers.roster {data['roles']['reviewers']['roster']} does not exist")

    topology = data.get("topology")
    orchestrator_kind = (data.get("roles", {}).get("orchestrator") or {}).get("kind")
    if topology == "agent-to-agent" and orchestrator_kind != "agent":
        report.add(label, None, "topology-orchestrator", "topology agent-to-agent: agents hand work to agents, so roles.orchestrator.kind must be agent (RULE-TOPOLOGY)")
    if topology == "independent-agents" and orchestrator_kind == "agent":
        report.add(label, None, "topology-orchestrator", "topology independent-agents: a person dispatches each item, so roles.orchestrator.kind must be human — or choose agent-to-agent (RULE-TOPOLOGY)")

    lifecycle = data.get("lifecycle") or {}
    if lifecycle:
        known = set(M.states())
        chosen = list(lifecycle.get("states") or [])
        for s in chosen:
            if s not in known:
                report.add(label, None, "lifecycle-unknown-state", f"lifecycle.states: '{s}' is not a state in core/model/item-states.yml")
        chosen_known = [s for s in chosen if s in known]
        if chosen:
            for cat in M.categories():
                if not any(M.category_of(s) == cat for s in chosen_known):
                    report.add(label, None, "lifecycle-category-empty", f"lifecycle.states: category {cat} has no state — a category may be relabelled, never dropped (RULE-STATE-CATEGORIES)")
        for key in (lifecycle.get("labels") or {}):
            if key not in known:
                report.add(label, None, "lifecycle-unknown-state", f"lifecycle.labels: '{key}' is not a state in core/model/item-states.yml")
            elif chosen and key not in chosen:
                report.add(label, None, "lifecycle-label-unused", f"lifecycle.labels: '{key}' is labelled but not listed in lifecycle.states")

    cadence = data.get("cadence") or {}
    pattern = cadence.get("iteration_name_pattern") or IN.naming_defaults()["pattern"]
    for problem in IN.validate_pattern(pattern):
        report.add(label, None, "iteration-name-pattern", f"cadence.iteration_name_pattern: {problem} (RULE-ITERATION-NAMING)")
    if IN.uses(pattern, "product") and not (data.get("organization") or {}).get("product"):
        report.add(label, None, "iteration-product", "cadence.iteration_name_pattern uses {product} but organization.product is not set (RULE-ITERATION-NAMING)")
    start_day = cadence.get("iteration_start_day") or IN.DEFAULT_START_DAY
    close_day = cadence.get("sprint_close") or IN.DEFAULT_SPRINT_CLOSE
    if start_day in IN.WEEKEND:
        report.add(label, None, "iteration-start-day", f"cadence.iteration_start_day: {start_day} — planning happens on a working day")
    if close_day in IN.WEEKEND:
        report.add(label, None, "sprint-close-day", f"cadence.sprint_close: {close_day} — the sprint close is a working day, the last one of the iteration (RULE-CEREMONY-SPRINT-CLOSE)")
    elif close_day == start_day:
        report.add(label, None, "sprint-close-day", f"cadence.sprint_close: {close_day} is the planning day — the sprint close is the last working day of the iteration, never its first (RULE-CEREMONY-SPRINT-CLOSE)")

    effective = {**profile_rules, **(data.get("optional_rules") or {})}
    if effective.get("require_homologation_qa"):
        for hat in ("qa", "key_user"):
            if hat not in data.get("roles", {}):
                report.add(label, None, "homolog-roles", f"require_homologation_qa is on: roles.{hat} is required (QA starts the env; the key user tests)")
        if not data.get("conventions", {}).get("homologation_environment"):
            report.add(label, None, "homolog-env", "require_homologation_qa is on: conventions.homologation_environment must name the environment")


def shipped_instances() -> list[Path]:
    paths = [M.REPO_ROOT / "instance.example.yml"]
    paths.extend(sorted((M.REPO_ROOT / "examples").glob("instance-*.yml")))
    paths.extend(sorted((M.REPO_ROOT / "profiles").glob("*/instance.example.yml")))
    return paths


def main() -> int:
    report = Report(check="check_instance — instance files are complete and coherent")
    paths = [Path(a) for a in sys.argv[1:]] or shipped_instances()
    for p in paths:
        if p.is_file():
            check(report, p.resolve())
        else:
            report.add(str(p), None, "missing", "file not found")
    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())
