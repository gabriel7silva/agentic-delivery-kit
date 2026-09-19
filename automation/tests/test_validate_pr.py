"""Tests for the binding gate. Each case is one documented refusal, plus a clean pass."""

from __future__ import annotations

import copy
from pathlib import Path


def test_clean_change_passes(run, pr_case, base_context, good_body):
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, good_body))
    assert code == 0, out
    assert "PASS" in out


def test_path_outside_claimed_scope(run, pr_case, base_context, good_body):
    code, out = run("validate_pr.py", *pr_case(["src/app.py"], base_context, good_body))
    assert code == 1
    assert "RULE-SCOPE" in out and "'app'" in out


def test_claim_not_in_handoff(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["claims"]["this_item"] = ["docs", "tests"]
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-GOLDEN-SCOPE" in out and "'tests'" in out


def test_open_claim_elsewhere_on_touched_scope(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["claims"]["open_elsewhere"] = {"docs": "WI-17"}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-CLAIM" in out and "WI-17" in out


def test_missing_required_reviewer(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["verdicts"] = ctx["verdicts"][:1]  # drop delivery-compliance
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-REVIEW-GATE" in out and "reviewer-delivery-compliance" in out


def test_blocking_finding_blocks(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["verdicts"][0]["findings"] = [{"severity": "blocking", "where": "docs/guide.md:3", "what": "claims a flag that does not exist"}]
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "blocking finding" in out


def test_verdict_block_blocks(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["verdicts"][0]["verdict"] = "block"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "verdict: block" in out


def test_risk_is_max_of_verdicts_and_floors(run, pr_case, base_context, good_body):
    """A docs path (floor low) with a reviewer saying high → risk high → the human gate applies."""
    ctx = copy.deepcopy(base_context)
    ctx["verdicts"][0]["risk"] = "high"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-RISK" in out and "'high'" in out          # item field says low, computed high
    assert "RULE-RISK-GATES" in out                         # and no human review


def test_high_floor_path_needs_human(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["handoff_scopes"] = ["data-boundary"]
    ctx["claims"]["this_item"] = ["data-boundary"]
    ctx["item"]["risk"] = "high"
    ctx["verdicts"] = [
        {"reviewer": r, "verdict": "pass", "risk": "low", "findings": []}
        for r in ("reviewer-correctness", "reviewer-security", "reviewer-delivery-compliance")
    ]
    code, out = run("validate_pr.py", *pr_case(["src/storage/writer.py"], ctx, good_body))
    assert code == 1
    assert "RULE-RISK-GATES" in out
    ctx["human_review"] = {"present": True, "by": "approver"}
    code, out = run("validate_pr.py", *pr_case(["src/storage/writer.py"], ctx, good_body))
    assert code == 0, out


def test_most_specific_glob_wins(run, pr_case, base_context, good_body):
    """src/storage/** (high) must beat src/** (medium) for the same path."""
    ctx = copy.deepcopy(base_context)
    ctx["handoff_scopes"] = ["app"]
    ctx["claims"]["this_item"] = ["app"]
    ctx["verdicts"] = [
        {"reviewer": r, "verdict": "pass", "risk": "low", "findings": []}
        for r in ("reviewer-correctness", "reviewer-delivery-compliance")
    ]
    code, out = run("validate_pr.py", *pr_case(["src/storage/writer.py"], ctx, good_body))
    assert code == 1
    assert "'data-boundary'" in out  # resolved to the more specific scope, not 'app'


def test_verification_not_passed(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["verification"] = {"passed": False}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "verification has not passed" in out


def test_agent_cannot_close(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-STATE-RESOLVED-NOT-CLOSED" in out


def test_approver_may_close(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 0, out


def test_approver_cannot_close_from_active(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "ACTIVE"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-STATES" in out
    assert "Resolved" in out


def test_new_to_resolved_forbidden(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["item"]["wi_state"] = "NEW"
    ctx["target_state"] = "RESOLVED"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-STATES" in out


def test_conclusion_missing_field(run, pr_case, base_context, good_body):
    body = good_body.replace("| Link | https://example.com/change/42 |", "| Link | |")
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, body))
    assert code == 1
    assert "RULE-CONCLUSION-COMMENT" in out and "'Link'" in out


def test_conclusion_next_step_closed(run, pr_case, base_context, good_body):
    body = good_body.replace("| Next step | review |", "| Next step | closed |")
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, body))
    assert code == 1
    assert "Next step says 'closed'" in out


def test_conclusion_evidence_is_prose(run, pr_case, base_context, good_body):
    body = good_body.replace(
        "| Evidence | AC1: https://example.com/run/1 · AC2: docs/receipts/WI-42.md |",
        "| Evidence | I tested it and it works fine |",
    )
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, body))
    assert code == 1
    assert "RULE-EVIDENCE" in out


def test_no_conclusion_at_all(run, pr_case, base_context):
    from conftest import GOOD_RECEIPT
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, GOOD_RECEIPT))
    assert code == 1
    assert "RULE-TRANSITION-BARRIER" in out


def test_receipt_missing_not_verified(run, pr_case, base_context, good_body):
    body = good_body.replace("### Not verified / not claimed", "### Something else")
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, body))
    assert code == 1
    assert "Not verified" in out


def test_receipt_not_verified_only_placeholder(run, pr_case, base_context, good_body):
    body = good_body.replace(
        "- Not opened in a spreadsheet application; only the raw file was inspected.",
        "- [ ] unknown — <what is not known> → <who decides>",
    )
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, body))
    assert code == 1
    assert "no real entry" in out


def test_receipt_failing_ac(run, pr_case, base_context, good_body):
    body = good_body.replace("| AC2 | pass |", "| AC2 | fail |")
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], base_context, body))
    assert code == 1
    assert "AC2 is marked fail" in out


def test_close_needs_homologation_and_key_user(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    ctx["optional_rules"] = {"require_homologation_qa": True}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-OPT-HOMOLOG-QA" in out
    ctx["homologation"] = {
        "branch": "feat/WI-42-export",
        "environment_url": "https://example.test/hms/WI-42",
        "qa_ready": True,
        "key_user_update": True,
    }
    ctx["transfer_review"] = {"accepted": True}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 0, out


def test_homologation_rejects_default_branch(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    ctx["optional_rules"] = {"require_homologation_qa": True}
    ctx["homologation"] = {
        "branch": "main",
        "environment_url": "https://example.test/hms/WI-42",
        "qa_ready": True,
        "key_user_update": True,
    }
    ctx["transfer_review"] = {"accepted": True}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-OPT-HOMOLOG-QA" in out
    assert "feature branch" in out


def test_homologation_string_false_is_not_ready(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    ctx["optional_rules"] = {"require_homologation_qa": True}
    ctx["homologation"] = {
        "branch": "feat/WI-42-export",
        "environment_url": "https://example.test/hms/WI-42",
        "qa_ready": "false",
        "key_user_update": "false",
    }
    ctx["transfer_review"] = {"accepted": True}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-OPT-HOMOLOG-QA" in out


def test_close_needs_transfer_review(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    ctx["optional_rules"] = {"require_homologation_qa": True}
    ctx["homologation"] = {
        "branch": "feat/WI-42-export",
        "environment_url": "https://example.test/hms/WI-42",
        "qa_ready": True,
        "key_user_update": True,
    }
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-CEREMONY-REVIEW" in out


def test_agency_close_needs_client_signoff(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    ctx["optional_rules"] = {"require_client_signoff": True}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-OPT-CLIENT-SIGNOFF" in out
    ctx["client_signoff"] = {"present": True}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 0, out


def test_client_signoff_string_false_is_absent(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    ctx["optional_rules"] = {"require_client_signoff": True}
    ctx["client_signoff"] = {"present": "false"}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-OPT-CLIENT-SIGNOFF" in out


def test_context_from_pr_body_block(run, tmp_path, base_context, good_body):
    import json
    body = good_body + "\n```pact-context\n" + json.dumps(base_context) + "\n```\n"
    p = tmp_path / "paths.txt"; p.write_text("docs/guide.md\n", encoding="utf-8")
    b = tmp_path / "body.md"; b.write_text(body, encoding="utf-8")
    code, out = run("validate_pr.py", "--changed-paths", str(p), "--pr-body", str(b))
    assert code == 0, out


def test_malformed_pact_context_is_a_finding(run, tmp_path, good_body):
    body = good_body + "\n```pact-context\n{not-json\n```\n"
    p = tmp_path / "paths.txt"; p.write_text("docs/guide.md\n", encoding="utf-8")
    b = tmp_path / "body.md"; b.write_text(body, encoding="utf-8")
    code, out = run("validate_pr.py", "--changed-paths", str(p), "--pr-body", str(b))
    assert code == 1
    assert "input" in out
    assert "JSON" in out or "json" in out.lower()


def test_instance_yml_enables_homologation(run, pr_case, base_context, good_body, tmp_path):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    inst = tmp_path / "instance.yml"
    inst.write_text(
        "optional_rules:\n  require_homologation_qa: true\n",
        encoding="utf-8",
    )
    args = pr_case(["docs/guide.md"], ctx, good_body) + ["--instance", str(inst)]
    code, out = run("validate_pr.py", *args)
    assert code == 1
    assert "RULE-OPT-HOMOLOG-QA" in out


def test_high_risk_requires_named_human(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["verdicts"][0]["risk"] = "high"
    ctx["item"]["risk"] = "high"
    ctx["human_review"] = {"present": True, "by": None}
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-RISK-GATES" in out


def test_missing_handoff_scopes_fails_golden(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    del ctx["handoff_scopes"]
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-GOLDEN-SCOPE" in out


def test_profile_defaults_enable_optional_rules(run, pr_case, base_context, good_body, tmp_path):
    """An instance that only names the agency profile inherits its toggles: the gate must not let
    Closed through without sign-off and homologation just because the instance is silent."""
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    inst = tmp_path / "instance.yml"
    inst.write_text("organization:\n  name: Acme Corp\n  profile: agency\n", encoding="utf-8")
    args = pr_case(["docs/guide.md"], ctx, good_body) + ["--instance", str(inst)]
    code, out = run("validate_pr.py", *args)
    assert code == 1
    assert "RULE-OPT-CLIENT-SIGNOFF" in out
    assert "RULE-OPT-HOMOLOG-QA" in out


def test_instance_cannot_lower_profile_toggle_in_gate(run, pr_case, base_context, good_body, tmp_path):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "RESOLVED"
    inst = tmp_path / "instance.yml"
    inst.write_text(
        "organization:\n  name: Acme Corp\n  profile: agency\n"
        "optional_rules:\n  require_client_signoff: false\n",
        encoding="utf-8",
    )
    args = pr_case(["docs/guide.md"], ctx, good_body) + ["--instance", str(inst)]
    code, out = run("validate_pr.py", *args)
    assert code == 1
    assert "RULE-OPT-CLIENT-SIGNOFF" in out


def test_discover_instance_follows_the_adopter_root(tmp_path, monkeypatch):
    """Copied out, instance.yml sits at the kit root; vendored at .pact/, it sits next to .pact/
    (docs/adopt-and-upgrade.md) — never inside it."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import validate_pr

    root = tmp_path / "adopter"
    (root / ".pact").mkdir(parents=True)
    (root / "instance.yml").write_text("version: 1\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)  # no instance.yml in the working directory
    monkeypatch.setattr(validate_pr.M, "REPO_ROOT", root / ".pact")
    assert validate_pr.discover_instance(None) == root / "instance.yml"
    monkeypatch.setattr(validate_pr.M, "REPO_ROOT", root)
    assert validate_pr.discover_instance(None) == root / "instance.yml"


def test_state_ids_normalise_to_categories(run, pr_case, base_context, good_body):
    """The gate speaks categories: IN_DEVELOPMENT → AWAITING_TEST is the Active → Resolved move."""
    ctx = copy.deepcopy(base_context)
    ctx["item"]["wi_state"] = "IN_DEVELOPMENT"
    ctx["target_state"] = "AWAITING_TEST"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 0, out


def test_close_from_a_resolved_state_id(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "KEY_USER_HOMOLOGATION"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 0, out


def test_close_from_an_active_state_id_is_refused(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["target_state"] = "CLOSED"
    ctx["actor_role"] = "approver"
    ctx["item"]["wi_state"] = "BLOCKED"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-STATES" in out and "Resolved" in out


def test_unknown_state_is_a_finding(run, pr_case, base_context, good_body):
    ctx = copy.deepcopy(base_context)
    ctx["item"]["wi_state"] = "DONE"
    code, out = run("validate_pr.py", *pr_case(["docs/guide.md"], ctx, good_body))
    assert code == 1
    assert "RULE-STATES" in out and "not a state" in out
