"""The kit's own example must pass the kit's own gate. If it does not, the kit is wrong."""

from __future__ import annotations

from pathlib import Path

WALK = Path(__file__).resolve().parents[2] / "examples" / "walkthrough"
CHANGED = ["src/customers/list.py", "src/customers/export.py", "tests/customers/test_export.py", "tests/fixtures/customers_3rows.json"]


def _args(tmp_path, body_text: str) -> list[str]:
    p = tmp_path / "paths.txt"
    p.write_text("\n".join(CHANGED) + "\n", encoding="utf-8")
    b = tmp_path / "body.md"
    b.write_text(body_text, encoding="utf-8")
    return ["--changed-paths", str(p), "--pr-body", str(b)]


def test_walkthrough_pr_passes_the_gate(run, tmp_path):
    body = (WALK / "03-pr-body.md").read_text(encoding="utf-8")
    code, out = run("validate_pr.py", *_args(tmp_path, body))
    assert code == 0, out


def test_walkthrough_fails_without_not_verified(run, tmp_path):
    body = (WALK / "03-pr-body.md").read_text(encoding="utf-8")
    body = body.replace("### Not verified / not claimed", "### Notes")
    code, out = run("validate_pr.py", *_args(tmp_path, body))
    assert code == 1 and "Not verified" in out


def test_walkthrough_fails_if_agent_closes(run, tmp_path):
    body = (WALK / "03-pr-body.md").read_text(encoding="utf-8")
    body = body.replace('"target_state": "AWAITING_TEST"', '"target_state": "CLOSED"')
    code, out = run("validate_pr.py", *_args(tmp_path, body))
    assert code == 1 and "RULE-STATE-RESOLVED-NOT-CLOSED" in out


def test_walkthrough_fails_outside_claim(run, tmp_path):
    body = (WALK / "03-pr-body.md").read_text(encoding="utf-8")
    p = tmp_path / "paths.txt"
    p.write_text("\n".join(CHANGED + ["src/customers/filters.py", "docs/export.md"]) + "\n", encoding="utf-8")
    b = tmp_path / "body.md"
    b.write_text(body, encoding="utf-8")
    code, out = run("validate_pr.py", "--changed-paths", str(p), "--pr-body", str(b))
    # filters.py is still in scope 'app' (claimed) — docs/export.md is in 'docs' (not claimed)
    assert code == 1 and "'docs'" in out
