"""SoT snapshot → context.json. Declared PR context is the fallback, never the winner."""

from __future__ import annotations

import json
from pathlib import Path


def test_build_context_prefers_sot_over_declared(run, tmp_path):
    snapshot = [
        {
            "id": "WI-42",
            "type": "STORY",
            "title": "Export the list",
            "wi_state": "IN_DEVELOPMENT",
            "risk": "medium",
            "claim": "app",
            "branch": "feat/export-list",
            "change_link": "https://example.test/change/42",
            "homolog_link": "https://example.test/hms/42",
        }
    ]
    declared = {
        "item": {"id": "WI-42", "type": "STORY", "wi_state": "ACTIVE", "risk": "low"},
        "actor_role": "implementer",
        "target_state": "RESOLVED",
        "handoff_scopes": ["docs"],
        "claims": {"this_item": ["docs"], "open_elsewhere": {}},
        "verification": {"passed": True},
        "verdicts": [],
        "human_review": {"present": False},
    }
    snap = tmp_path / "board.json"
    dec = tmp_path / "declared.json"
    out = tmp_path / "context.json"
    snap.write_text(json.dumps(snapshot), encoding="utf-8")
    dec.write_text(json.dumps(declared), encoding="utf-8")
    code, text = run(
        "build_context.py",
        "--snapshot", str(snap),
        "--declared", str(dec),
        "--item", "WI-42",
        "--out", str(out),
    )
    assert code == 0, text
    ctx = json.loads(out.read_text(encoding="utf-8"))
    assert ctx["item"]["wi_state"] == "IN_DEVELOPMENT"
    assert ctx["item"]["risk"] == "medium"
    assert ctx["claims"]["this_item"] == ["app"]
    assert ctx["homologation"]["branch"] == "feat/export-list"
    assert ctx["source"] == "sot"
    assert ctx["actor_role"] == "implementer"
    assert ctx["verification"]["passed"] is True


def test_build_context_falls_back_to_declared(run, tmp_path):
    declared = {
        "item": {"id": "WI-9", "type": "TASK", "wi_state": "ACTIVE", "risk": "low"},
        "actor_role": "implementer",
        "target_state": "RESOLVED",
        "handoff_scopes": ["docs"],
        "claims": {"this_item": ["docs"], "open_elsewhere": {}},
        "verification": {"passed": True},
    }
    dec = tmp_path / "declared.json"
    out = tmp_path / "context.json"
    dec.write_text(json.dumps(declared), encoding="utf-8")
    code, text = run(
        "build_context.py",
        "--declared", str(dec),
        "--item", "WI-9",
        "--out", str(out),
    )
    assert code == 0, text
    ctx = json.loads(out.read_text(encoding="utf-8"))
    assert ctx["source"] == "declared"
    assert ctx["item"]["id"] == "WI-9"
    assert ctx["claims"]["this_item"] == ["docs"]


def test_build_context_missing_item_on_board_is_declared(run, tmp_path):
    snap = tmp_path / "board.json"
    dec = tmp_path / "declared.json"
    out = tmp_path / "context.json"
    snap.write_text(json.dumps([{"id": "WI-1", "type": "STORY", "title": "x", "wi_state": "NEW"}]), encoding="utf-8")
    dec.write_text(json.dumps({
        "item": {"id": "WI-42", "type": "STORY", "wi_state": "ACTIVE", "risk": "low"},
        "claims": {"this_item": ["docs"], "open_elsewhere": {}},
    }), encoding="utf-8")
    code, text = run(
        "build_context.py",
        "--snapshot", str(snap),
        "--declared", str(dec),
        "--item", "WI-42",
        "--out", str(out),
    )
    assert code == 0, text
    assert json.loads(out.read_text(encoding="utf-8"))["source"] == "declared"
