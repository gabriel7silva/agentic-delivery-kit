"""The kit's own checks run green against the kit — and red against known-bad fixtures."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib import entry_points as EP  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_leaks_pass_on_kit(run):
    code, out = run("check_leaks.py")
    assert code == 0, out


def test_leaks_fail_on_fixture(run):
    code, out = run("check_leaks.py", str(FIXTURES / "leaks"))
    assert code == 1
    for rule in ("local-path", "email", "board-url", "item-url", "repo-url", "handle"):
        assert rule in out, f"expected rule {rule} to fire\n{out}"


def test_leaks_denylist_from_env(run, monkeypatch):
    monkeypatch.setenv("PACT_DENYLIST", "acmeco,jane doe")
    code, out = run("check_leaks.py", str(FIXTURES / "leaks"))
    assert code == 1 and "denylist" in out


def test_leaks_denylist_file_does_not_self_match(tmp_path, monkeypatch):
    """Configuring via .leakcheck-denylist must not fail because the file lists its own terms."""
    import check_leaks as leaks

    denylist_path = tmp_path / ".leakcheck-denylist"
    denylist_path.write_text("secretco\n", encoding="utf-8")
    (tmp_path / "ok.md").write_text("clean text\n", encoding="utf-8")
    monkeypatch.setattr(leaks, "DENYLIST_FILE", denylist_path)
    monkeypatch.setattr(leaks, "REPO_ROOT", tmp_path)
    report = leaks.scan([tmp_path], ["secretco"])
    assert report.ok, report.findings


def test_leaks_denylist_still_flags_content(tmp_path, monkeypatch):
    import check_leaks as leaks

    denylist_path = tmp_path / ".leakcheck-denylist"
    denylist_path.write_text("secretco\n", encoding="utf-8")
    (tmp_path / "leaked.md").write_text("secretco internal\n", encoding="utf-8")
    monkeypatch.setattr(leaks, "DENYLIST_FILE", denylist_path)
    monkeypatch.setattr(leaks, "REPO_ROOT", tmp_path)
    report = leaks.scan([tmp_path], ["secretco"])
    assert not report.ok
    assert any(f.rule == "denylist" and "leaked.md" in f.path for f in report.findings)


def test_leaks_scans_extensionless_license(run, tmp_path):
    addr = "owner@" + "private.test"
    (tmp_path / "LICENSE").write_text(f"Copyright 2026 {addr}\n", encoding="utf-8")
    (tmp_path / "ok.md").write_text("fine\n", encoding="utf-8")
    code, out = run("check_leaks.py", str(tmp_path))
    assert code == 1 and "email" in out, out


def test_leaks_makefile_recipe_is_not_a_handle(run, tmp_path):
    (tmp_path / "Makefile").write_text("help:\n\t@echo hi\n", encoding="utf-8")
    code, out = run("check_leaks.py", str(tmp_path))
    assert code == 0, out


def test_leaks_allows_placeholder_repo(run, tmp_path):
    (tmp_path / "ok.md").write_text(
        "CI: https://github.com/example-org/agentic-delivery-kit/actions\n",
        encoding="utf-8",
    )
    code, out = run("check_leaks.py", str(tmp_path))
    assert code == 0, out


def test_leaks_fails_on_non_utf8_svg(run, tmp_path):
    bad = tmp_path / "latin1.svg"
    bad.write_bytes(b"<svg>SAME ROLES \xb7 TWO MODES</svg>\n")
    code, out = run("check_leaks.py", str(bad))
    assert code == 1 and "encoding" in out


def test_links_pass_on_kit(run):
    code, out = run("check_links.py")
    assert code == 0, out


def test_schemas_pass_on_kit(run):
    code, out = run("check_schemas.py")
    assert code == 0, out


def test_mapping_pass_on_kit(run):
    code, out = run("check_mapping.py")
    assert code == 0, out


def test_canon_pass_on_kit(run):
    code, out = run("check_canon.py")
    assert code == 0, out


def test_canon_detects_diverged_fence(run, tmp_path):
    """Copy the kit, corrupt one fenced block, expect fence-diverged."""
    root = Path(__file__).resolve().parents[2]
    dst = tmp_path / "kit"
    shutil.copytree(root, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
    target = dst / "templates" / "flow" / "handoff.md"
    text = target.read_text(encoding="utf-8")
    target.write_text(text.replace("Method: PACT — Plan", "Method: TAMPERED — Plan"), encoding="utf-8")
    import subprocess, sys
    proc = subprocess.run([sys.executable, str(dst / "automation/scripts/check_canon.py")], capture_output=True, text=True, cwd=dst)
    assert proc.returncode == 1 and "fence-diverged" in proc.stdout


def test_instance_example_passes(run):
    code, out = run("check_instance.py", "instance.example.yml")
    assert code == 0, out


def test_instance_rejects_slack_as_sot(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "slack-as-sot.yml"))
    assert code == 1 and "sot-not-eligible" in out


def test_instance_rejects_non_optional_toggle(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "toggles-mandatory-rule.yml"))
    assert code == 1 and "not-optional" in out


def test_instance_homolog_requires_hats(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "homolog-no-roles.yml"))
    assert code == 1
    assert "homolog-roles" in out
    assert "homolog-env" in out


def test_shipped_instances_pass(run):
    code, out = run("check_instance.py")
    assert code == 0, out


def test_instance_agency_profile_defaults_require_hats(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "agency-no-optional.yml"))
    assert code == 1
    assert "homolog-roles" in out


def test_instance_cannot_lower_profile_toggle(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "agency-lowers-signoff.yml"))
    assert code == 1
    assert "profile-contradiction" in out


def test_report_emit_handles_unicode_arrow():
    """Windows cp1252 used to crash on findings that contain →."""
    import sys

    scripts = Path(__file__).resolve().parents[1] / "scripts"
    sys.path.insert(0, str(scripts))
    from lib.report import Report  # noqa: E402

    report = Report(check="report-unicode")
    report.add("transition", None, "RULE-STATES", "New → Resolved is forbidden")
    assert report.emit() == 1


def test_instance_lifecycle_must_keep_every_category(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "lifecycle-drops-closed.yml"))
    assert code == 1
    assert "lifecycle-category-empty" in out and "CLOSED" in out


def test_instance_lifecycle_rejects_unknown_state(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "lifecycle-unknown-state.yml"))
    assert code == 1
    assert "lifecycle-unknown-state" in out


def test_instance_topology_must_agree_with_roles(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "topology-mismatch.yml"))
    assert code == 1
    assert "topology-orchestrator" in out


def test_folder_runtimes_are_in_the_generator():
    paths = {p.path for p in EP.POINTERS}
    for rel in (
        ".claude/rules/pact.md",
        ".hermes.md",
        ".hermes/rules/pact.md",
        ".grok/rules/pact.md",
        ".grokbot/rules/pact.md",
        ".openclaw/rules/pact.md",
        ".codex/rules/pact.md",
    ):
        assert rel in paths, rel


def test_github_issue_templates_are_pact_forms():
    """One frontmatter each; kit types; no GitHub-default stubs."""
    root = Path(__file__).resolve().parents[2] / ".github" / "ISSUE_TEMPLATE"
    names = {p.stem for p in root.glob("*.md")}
    assert {"bug", "feature", "issue", "task"} <= names
    assert "custom" not in names and "bug_report" not in names
    for path in root.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), path.name
        closed = text.find("\n---\n", 4)
        assert closed != -1, path.name
        body = text[closed + 5 :]
        assert not body.lstrip().startswith("---"), f"{path.name} has a second frontmatter"
        assert "PACT" in text or "Resolved" in text, path.name
    config = (root / "config.yml").read_text(encoding="utf-8")
    assert "blank_issues_enabled: false" in config


def test_every_runtime_pointer_lands_on_agents_md():
    root = Path(__file__).resolve().parents[2]
    assert (root / "AGENTS.md").is_file()
    assert len(EP.POINTERS) >= 25
    for ptr in EP.POINTERS:
        text = (root / ptr.path).read_text(encoding="utf-8")
        assert "AGENTS.md" in text, ptr.path
        if ptr.style != "aider":
            assert "interview" in text, f"{ptr.path} must say that a setup starts with the interview"
        assert len(text.splitlines()) <= 16, f"{ptr.path} is a pointer, not an instruction file"


def test_entry_points_are_current(run):
    code, out = run("entry_points.py", "--check")
    assert code == 0, out


def test_entry_points_write_for_an_adopter_root(run, tmp_path):
    code, out = run("entry_points.py", "--root", str(tmp_path), "--kit", ".pact")
    assert code == 0, out
    for ptr in EP.POINTERS:
        assert (tmp_path / ptr.path).is_file(), ptr.path
    cursor = (tmp_path / ".cursor" / "rules" / "pact.mdc").read_text(encoding="utf-8")
    assert cursor.startswith("---") and "alwaysApply: true" in cursor
    assert ".pact/docs/onboarding/interview.md" in cursor and "](../../AGENTS.md)" in cursor
    assert "read `.pact/AGENTS.md`" in cursor and "](../../.pact/AGENTS.md)" in cursor, "before the setup exists the pointer falls back to the kit's entry point"
    assert len(cursor.splitlines()) <= 16
    code, out = run("entry_points.py", "--root", str(tmp_path), "--kit", ".pact", "--check")
    assert code == 0, out
    (tmp_path / "CLAUDE.md").write_text("edited by hand\n", encoding="utf-8")
    code, out = run("entry_points.py", "--root", str(tmp_path), "--kit", ".pact", "--check")
    assert code == 1 and "pointer-differs" in out


def test_prompt_pack_ships_the_po_assistant():
    root = Path(__file__).resolve().parents[2]
    text = (root / "adapters" / "prompt-pack" / "out" / "po-assistant.md").read_text(encoding="utf-8")
    assert "{{language}}" in text, "the assistant answers in the instance language"
    assert "🔹" in text and "🗑️" in text, "the icon legend travels with the prompt"
    assert "Resolved is not Closed" in text


def test_instance_rejects_product_placeholder_without_product(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "iteration-pattern-no-product.yml"))
    assert code == 1
    assert "iteration-product" in out and "organization.product" in out


def test_instance_rejects_unknown_name_placeholder(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "iteration-pattern-unknown-placeholder.yml"))
    assert code == 1
    assert "iteration-name-pattern" in out and "{sprint}" in out


def test_instance_rejects_weekend_start_and_close(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "cadence-weekend-days.yml"))
    assert code == 1
    assert "iteration-start-day" in out and "sprint-close-day" in out


def test_instance_rejects_close_on_the_planning_day(run):
    code, out = run("check_instance.py", str(FIXTURES / "instances" / "cadence-close-on-planning-day.yml"))
    assert code == 1
    assert "sprint-close-day" in out and "planning day" in out


def test_shipped_instances_run_a_weekly_sprint():
    """Every instance the kit ships states the default week: seven days, planning on the start
    day, the sprint close on the last working day, the iteration named from the pattern."""
    root = Path(__file__).resolve().parents[2]
    files = [root / "instance.example.yml"]
    files += sorted((root / "examples").glob("instance-*.yml"))
    files += sorted((root / "profiles").glob("*/instance.example.yml"))
    assert len(files) == 7
    for f in files:
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        cadence = data["cadence"]
        assert cadence["iteration_length_days"] == 7, f
        assert cadence["iteration_start_day"] == "monday" and cadence["sprint_close"] == "friday", f
        assert cadence["iteration_name_pattern"] == "Sprint {seq:02} {yy} Q{quarter} {product}", f
        assert cadence["sequence_resets"] == "year", f
        assert data["organization"].get("product"), f
    root_tags = yaml.safe_load((root / "instance.example.yml").read_text(encoding="utf-8"))["conventions"]["tags"]
    assert "ceremony" in root_tags["process"]
