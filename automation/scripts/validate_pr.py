#!/usr/bin/env python3
"""The binding gate. Refuses a change that breaks scope, concurrency, review,
risk or evidence rules — regardless of which runtime produced it.

Inputs are deliberately tool-neutral so the same script runs in any CI:

  --changed-paths FILE   one repository-relative path per line (git diff --name-only)
  --context FILE         JSON describing the item, claims, verdicts (schema below), or
  --pr-body FILE         a PR body containing a ```pact-context fenced JSON block
  --instance FILE        instance.yml (default: ./instance.yml, else the adopter root — the kit
                         root when copied out, its parent when vendored at .pact/). The profile
                         it names supplies optional-rule defaults; the instance may raise them,
                         never lower them.
  --receipt FILE         the receipt (default: parsed from the PR body)
  --conclusion FILE      the conclusion comment (default: parsed from the PR body)
  --ownership FILE       override agents/ownership.yml (tests)
  --floors FILE          override agents/policies/risk-floors.yml (tests)

Context JSON (every key optional except item and claims):
{
  "item":         {"id": "WI-42", "type": "STORY", "wi_state": "IN_DEVELOPMENT", "risk": "low"},
  "actor_role":   "implementer",
  "target_state": "AWAITING_TEST",
  "handoff_scopes": ["app", "docs"],
  "claims":       {"this_item": ["app"], "open_elsewhere": {"docs": "WI-17"}},
  "verification": {"passed": true},
  "verdicts":     [{"reviewer": "reviewer-correctness", "verdict": "pass", "risk": "low",
                    "findings": [{"severity": "non-blocking", "where": "...", "what": "..."}]}],
  "human_review": {"present": false, "by": null},
  "optional_rules": {"require_client_signoff": false, "require_homologation_qa": false},
  "client_signoff": {"present": false},
  "homologation": {"branch": "", "environment_url": "", "qa_ready": false, "key_user_update": false},
  "transfer_review": {"accepted": false}
}

`wi_state` and `target_state` take a state id from core/model/item-states.yml or one of the
five category ids (NEW, ACTIVE, RESOLVED, CLOSED, REMOVED). The gate checks by category, so a
context written for the five-state model keeps working.

Exit 1 on any finding. Each finding names the rule it enforces.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import model as M  # noqa: E402
from lib.diffscope import RISK_ORDER, Ownership, max_risk, required_reviewers, touched_scopes  # noqa: E402
from lib.report import Report  # noqa: E402

CONCLUSION_FIELDS = ("Responsible", "Date", "What was done", "Link", "Evidence", "Next step")
HUMAN_ROLES = {"approver", "product_owner"}
PLACEHOLDER = re.compile(r"^<[^>]*>$")
CONTEXT_BLOCK = re.compile(r"```pact-context\s*\n(.*?)\n```", re.S)
DEFAULT_BRANCHES = {"main", "master", "trunk", "develop"}


def flag(value) -> bool:
    """Only a JSON/YAML boolean true counts. The string 'false' is not on."""
    return value is True


def optional_on(ctx: dict, key: str) -> bool:
    ctx_opt = ctx.get("optional_rules") or {}
    inst_opt = ctx.get("_instance_optional") or {}
    return flag(ctx_opt.get(key)) or flag(inst_opt.get(key))


def adopter_root() -> Path:
    """Where instance.yml lives: the kit root when copied out, its parent when vendored at .pact/
    (docs/adopt-and-upgrade.md — never inside .pact/)."""
    return M.REPO_ROOT.parent if M.REPO_ROOT.name == ".pact" else M.REPO_ROOT


def discover_instance(explicit: Path | None) -> Path | None:
    if explicit:
        return explicit
    for candidate in (Path("instance.yml"), adopter_root() / "instance.yml"):
        if candidate.is_file():
            return candidate
    return None


def load_instance_optional(path: Path | None) -> dict:
    """Effective optional-rule toggles: the defaults of the profile the instance names, raised —
    never lowered — by the instance's own optional_rules. The same overlay check_instance.py
    applies, so an instance that only names its profile still carries that profile's gates."""
    if path is None or not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    instance_rules = dict(data.get("optional_rules") or {})
    organization = data.get("organization")
    profile = organization.get("profile") if isinstance(organization, dict) else None
    profile_rules: dict = {}
    if profile:
        pfile = M.REPO_ROOT / "profiles" / str(profile) / "profile.yml"
        if pfile.is_file():
            pdata = yaml.safe_load(pfile.read_text(encoding="utf-8")) or {}
            profile_rules = dict(pdata.get("optional_rules") or {})
    return {key: flag(profile_rules.get(key)) or flag(instance_rules.get(key)) for key in {*profile_rules, *instance_rules}}


def parse_json(text: str, report: Report, label: str) -> dict | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        report.add(label, None, "input", f"invalid JSON: {exc}")
        return None


def read_paths(path: Path) -> list[str]:
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def context_from_body(body: str, report: Report) -> dict | None:
    m = CONTEXT_BLOCK.search(body)
    if not m:
        return None
    return parse_json(m.group(1), report, "context")


def section(text: str, heading_rx: str) -> str:
    """Body of the first markdown section whose heading matches, up to the next heading of
    the same or higher level."""
    m = re.search(rf"^(#{{1,6}})\s*{heading_rx}[^\n]*$", text, re.M | re.I)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(rf"^#{{1,{level}}}\s", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def field_value(text: str, name: str) -> str:
    """Value of `| Name | value |` or `Name: value` or `**Name:** value`, first match."""
    patterns = [
        rf"^\|\s*\**{re.escape(name)}\**\s*\|\s*(.*?)\s*\|\s*$",
        rf"^\**{re.escape(name)}\**\s*:\s*(.*?)\s*$",
    ]
    for p in patterns:
        m = re.search(p, text, re.M | re.I)
        if m:
            v = m.group(1).strip()
            return "" if PLACEHOLDER.match(v) else v
    return ""


def bullets(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*[-*]\s+(?:\[[ x]\]\s*)?(.*)$", line)
        if m:
            v = m.group(1).strip()
            if v and not PLACEHOLDER.match(v) and "<what is not known>" not in v:
                out.append(v)
    return out


def acceptance_rows(text: str) -> list[tuple[str, str]]:
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*(AC\d+)\s*\|\s*(pass|fail|out of scope)\b[^|]*\|", line, re.I)
        if m:
            rows.append((m.group(1).upper(), m.group(2).lower()))
    return rows


def check_scope_and_claims(report: Report, own: Ownership, paths: list[str], ctx: dict) -> str:
    res = own.resolve(paths)
    touched = touched_scopes(res)
    claimed = set(ctx.get("claims", {}).get("this_item", []))
    if "handoff_scopes" not in ctx:
        report.add("claim", None, "RULE-GOLDEN-SCOPE", "handoff_scopes is missing — claimed scopes must be listed on the handoff")
        handoff: set[str] = set()
    else:
        handoff = set(ctx.get("handoff_scopes") or [])
    elsewhere = ctx.get("claims", {}).get("open_elsewhere", {})

    for r in res:
        if r.scope.id not in claimed:
            report.add(r.path, None, "RULE-SCOPE", f"path is in scope '{r.scope.id}', which this item has not claimed (claimed: {sorted(claimed) or 'none'})")
    for s in sorted(claimed - handoff):
        report.add("claim", None, "RULE-GOLDEN-SCOPE", f"scope '{s}' is claimed but the handoff did not allow it (handoff: {sorted(handoff)})")
    for s in sorted(touched):
        if s in elsewhere:
            report.add("claim", None, "RULE-CLAIM", f"scope '{s}' has an open claim by {elsewhere[s]} — one open claim per scope")

    need = required_reviewers(res)
    verdicts = ctx.get("verdicts", [])
    have = {v.get("reviewer") for v in verdicts}
    for rv in sorted(need - have):
        report.add("review", None, "RULE-REVIEW-GATE", f"required reviewer '{rv}' has not returned a verdict")
    for v in verdicts:
        if v.get("verdict") == "block":
            report.add("review", None, "RULE-REVIEW-GATE", f"{v.get('reviewer')} returned verdict: block")
        for f in v.get("findings", []):
            if f.get("severity") == "blocking":
                report.add(f.get("where", "review"), None, "RULE-REVIEW-GATE", f"blocking finding from {v.get('reviewer')}: {f.get('what', '')}")
        raw = v.get("risk", "low")
        if (raw or "").lower() not in RISK_ORDER:
            report.add("review", None, "RULE-RISK", f"unknown risk {raw!r} from {v.get('reviewer')} — treated as high")

    floors = [r.floor for r in res]
    verdict_risks = [v.get("risk", "low") for v in verdicts]
    risk = max_risk(floors + verdict_risks)
    declared = (ctx.get("item", {}).get("risk") or "").lower()
    if declared and declared != risk:
        report.add("item", None, "RULE-RISK", f"item risk field says '{declared}' but MAX(verdicts, floors) is '{risk}'")
    hr = ctx.get("human_review") or {}
    named = str(hr.get("by") or "").strip()
    if risk == "high" and not (flag(hr.get("present")) and named):
        report.add("review", None, "RULE-RISK-GATES", "risk is high: a named human must review before Resolved, and none is recorded")
    return risk


def check_verification(report: Report, ctx: dict) -> None:
    if not flag((ctx.get("verification") or {}).get("passed")):
        report.add("verification", None, "RULE-REVIEW-GATE", "deterministic verification has not passed (verification.passed is not true)")


def state_category(report: Report, raw: str, what: str) -> str:
    """Normalise a state id (or a category id) to its category. Unknown → finding, treated as ''."""
    key = (raw or "").strip()
    if not key:
        return ""
    cat = M.category_of(key)
    if cat is None:
        report.add("transition", None, "RULE-STATES", f"{what} '{raw}' is not a state in core/model/item-states.yml (nor a category)")
        return ""
    return cat


def check_transition(report: Report, ctx: dict) -> None:
    raw_target = ctx.get("target_state") or ""
    raw_current = (ctx.get("item") or {}).get("wi_state") or ""
    target = state_category(report, raw_target, "target_state")
    current = state_category(report, raw_current, "item.wi_state")
    actor = (ctx.get("actor_role") or "").lower()
    if target == "CLOSED" and actor not in HUMAN_ROLES:
        report.add("transition", None, "RULE-STATE-RESOLVED-NOT-CLOSED", f"actor '{actor or 'unknown'}' may not set Closed — only {sorted(HUMAN_ROLES)}")
    if target == "CLOSED" and current != "RESOLVED":
        report.add("transition", None, "RULE-STATES", f"Closed is only allowed from a Resolved-category state (item is '{raw_current or 'unknown'}' → category {current or 'unknown'})")
    if target == "CLOSED" and optional_on(ctx, "require_client_signoff"):
        if not flag((ctx.get("client_signoff") or {}).get("present")):
            report.add("transition", None, "RULE-OPT-CLIENT-SIGNOFF", "require_client_signoff is on: Closed needs a recorded client sign-off")
    if target == "CLOSED" and optional_on(ctx, "require_homologation_qa"):
        homolog = ctx.get("homologation") or {}
        branch = (homolog.get("branch") or "").strip()
        url = (homolog.get("environment_url") or "").strip()
        if not branch or branch.lower() in DEFAULT_BRANCHES:
            report.add("transition", None, "RULE-OPT-HOMOLOG-QA", "require_homologation_qa is on: Closed needs the feature branch on the item (not the default branch)")
        if not url:
            report.add("transition", None, "RULE-OPT-HOMOLOG-QA", "require_homologation_qa is on: Closed needs the homologation environment URL for that branch")
        if not flag(homolog.get("qa_ready")):
            report.add("transition", None, "RULE-OPT-HOMOLOG-QA", "require_homologation_qa is on: QA has not recorded that the environment is up and linked")
        if not flag(homolog.get("key_user_update")):
            report.add("transition", None, "RULE-OPT-HOMOLOG-QA", "require_homologation_qa is on: the key user has not tested on that environment and posted the PO update")
        if not flag((ctx.get("transfer_review") or {}).get("accepted")):
            report.add("transition", None, "RULE-CEREMONY-REVIEW", "require_homologation_qa is on: Transfer review has not accepted the key-user evidence")
    if target == "RESOLVED" and current == "NEW":
        report.add("transition", None, "RULE-STATES", "New -> Resolved is forbidden: nothing was executed")


def check_conclusion(report: Report, text: str) -> None:
    if not text.strip():
        report.add("conclusion", None, "RULE-TRANSITION-BARRIER", "no conclusion comment found (six fields required before leaving Active)")
        return
    for name in CONCLUSION_FIELDS:
        if not field_value(text, name):
            report.add("conclusion", None, "RULE-CONCLUSION-COMMENT", f"field '{name}' is empty or missing")
    nxt = field_value(text, "Next step").lower()
    if "closed" in nxt:
        report.add("conclusion", None, "RULE-STATE-RESOLVED-NOT-CLOSED", "Next step says 'closed' — an agent never sets that")
    ev = field_value(text, "Evidence")
    if ev and not re.search(r"https?://|\.md|\.png|\.log|\.txt|#|/", ev):
        report.add("conclusion", None, "RULE-EVIDENCE", "Evidence is a sentence, not a link or an attachment reference")


def check_receipt(report: Report, text: str) -> None:
    if not text.strip():
        report.add("receipt", None, "RULE-DOD", "no receipt found")
        return
    nv = section(text, r"Not verified")
    if not nv.strip():
        report.add("receipt", None, "RULE-DOD", "missing section 'Not verified / not claimed'")
    elif not bullets(nv):
        report.add("receipt", None, "RULE-DOD", "'Not verified / not claimed' has no real entry — nothing is fully verified; say what was not checked")
    rows = acceptance_rows(text)
    if not rows:
        report.add("receipt", None, "RULE-DOD", "no per-AC acceptance rows (| AC1 | pass | ... |)")
    for ac, result in rows:
        if result == "fail":
            report.add("receipt", None, "RULE-DOD", f"{ac} is marked fail — cannot move to Resolved with a failing criterion")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--changed-paths", type=Path, required=True)
    ap.add_argument("--context", type=Path)
    ap.add_argument("--pr-body", type=Path)
    ap.add_argument("--instance", type=Path)
    ap.add_argument("--receipt", type=Path)
    ap.add_argument("--conclusion", type=Path)
    ap.add_argument("--ownership", type=Path)
    ap.add_argument("--floors", type=Path)
    a = ap.parse_args(argv)

    report = Report(check="validate_pr — scope, claims, review, risk, evidence")
    body = a.pr_body.read_text(encoding="utf-8") if a.pr_body else ""

    if a.context:
        ctx = parse_json(a.context.read_text(encoding="utf-8"), report, "context")
        if ctx is None:
            return report.emit()
    else:
        ctx = context_from_body(body, report)
        if ctx is None:
            if not any(f.rule == "input" for f in report.findings):
                report.add("context", None, "input", "no --context file and no ```pact-context block in the PR body")
            return report.emit()

    ctx["_instance_optional"] = load_instance_optional(discover_instance(a.instance))

    if a.ownership:
        own = Ownership(M.load_yaml(a.ownership), M.load_yaml(a.floors) if a.floors else None)
    else:
        own = Ownership.from_repo()

    paths = read_paths(a.changed_paths)
    report.scanned = len(paths)

    check_transition(report, ctx)
    check_verification(report, ctx)
    check_scope_and_claims(report, own, paths, ctx)
    check_conclusion(report, a.conclusion.read_text(encoding="utf-8") if a.conclusion else section(body, r"Conclusion"))
    check_receipt(report, a.receipt.read_text(encoding="utf-8") if a.receipt else section(body, r"Receipt"))
    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())
