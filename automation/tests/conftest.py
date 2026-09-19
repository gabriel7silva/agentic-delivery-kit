"""Shared fixtures for the kit's pytest suite.

Every test runs the real scripts against fixture files, the same way CI does.
Nothing is mocked: if a script's behaviour changes, a test here changes with it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "automation" / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def run():
    """Run a kit script; return (exit_code, stdout+stderr)."""
    def _run(script: str, *args: str) -> tuple[int, str]:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / script), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT,
        )
        return proc.returncode, proc.stdout + proc.stderr
    return _run


@pytest.fixture
def pr_case(tmp_path):
    """Build the three validator inputs from a case: changed paths, context JSON, PR body."""
    def _case(paths: list[str], context: dict, body: str) -> list[str]:
        p = tmp_path / "paths.txt"
        p.write_text("\n".join(paths) + "\n", encoding="utf-8")
        c = tmp_path / "context.json"
        c.write_text(json.dumps(context), encoding="utf-8")
        b = tmp_path / "body.md"
        b.write_text(body, encoding="utf-8")
        return ["--changed-paths", str(p), "--context", str(c), "--pr-body", str(b)]
    return _case


GOOD_CONCLUSION = """
## Conclusion

| Field | Value |
|---|---|
| Responsible | implementer |
| Date | 2026-01-15 10:00 UTC |
| What was done | Added the Export CSV button to the list screen; header row plus one data row per visible item. |
| Link | https://example.com/change/42 |
| Evidence | AC1: https://example.com/run/1 · AC2: docs/receipts/WI-42.md |
| Next step | review |
"""

GOOD_RECEIPT = """
## Receipt

### Acceptance, criterion by criterion

| AC | Result | Evidence |
|---|---|---|
| AC1 | pass | https://example.com/run/1 |
| AC2 | pass | https://example.com/run/2 |

### Not verified / not claimed

- Not opened in a spreadsheet application; only the raw file was inspected.
"""


@pytest.fixture
def good_body():
    return GOOD_CONCLUSION + "\n" + GOOD_RECEIPT


@pytest.fixture
def base_context():
    """A context that passes on its own: one low-risk scope, claimed and allowed, reviewed."""
    return {
        "item": {"id": "WI-42", "type": "STORY", "wi_state": "ACTIVE", "risk": "low"},
        "actor_role": "implementer",
        "target_state": "RESOLVED",
        "handoff_scopes": ["docs"],
        "claims": {"this_item": ["docs"], "open_elsewhere": {}},
        "verification": {"passed": True},
        "verdicts": [
            {"reviewer": "reviewer-docs", "verdict": "pass", "risk": "low", "findings": []},
            {"reviewer": "reviewer-delivery-compliance", "verdict": "pass", "risk": "low", "findings": []},
        ],
        "human_review": {"present": False},
    }
