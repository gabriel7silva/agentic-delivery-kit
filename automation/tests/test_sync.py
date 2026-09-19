"""Sync engine tests — offline, against in-memory items. No API is called."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).resolve().parents[1] / "sync"
sys.path.insert(0, str(SYNC))
from sync_core import Event, Item, diff  # noqa: E402
from dataclasses import asdict  # noqa: E402


def item(**kw) -> Item:
    base = dict(id="WI-1", type="STORY", title="t", wi_state="ACTIVE")
    base.update(kw)
    return Item(**base)


def test_diff_detects_state_change_as_event():
    prev = {"WI-1": asdict(item(wi_state="ACTIVE"))}
    changed, removed, events = diff(prev, [item(wi_state="RESOLVED")])
    assert [c.id for c in changed] == ["WI-1"] and removed == []
    assert events == [Event("WI-1", "state", "ACTIVE → RESOLVED")]


def test_diff_marks_resolved_to_active_as_rejection():
    prev = {"WI-1": asdict(item(wi_state="RESOLVED"))}
    _, _, events = diff(prev, [item(wi_state="ACTIVE")])
    assert events[0].kind == "rejected"


def test_diff_claim_and_release_events():
    prev = {"WI-1": asdict(item(claim=None))}
    _, _, ev = diff(prev, [item(claim="scope docs")])
    assert ev == [Event("WI-1", "claim", "scope docs")]
    prev = {"WI-1": asdict(item(claim="scope docs"))}
    _, _, ev = diff(prev, [item(claim=None)])
    assert ev == [Event("WI-1", "release", "released")]


def test_diff_removed_items():
    prev = {"WI-1": asdict(item()), "WI-2": asdict(item(id="WI-2"))}
    _, removed, _ = diff(prev, [item()])
    assert removed == ["WI-2"]


def test_connector_refuses_without_token(monkeypatch):
    monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
    proc = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, %r); from connectors.slack import make; make({}, False)" % str(SYNC)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2 and "SLACK_BOT_TOKEN" in proc.stderr


def test_slack_refuses_to_be_sot(monkeypatch):
    monkeypatch.setenv("SLACK_BOT_TOKEN", "x")
    proc = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, %r); from connectors.slack import make; make({}, True)" % str(SYNC)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2 and "source of truth" in proc.stderr


def test_sot_eligible_reads_capabilities():
    from sync_core import sot_eligible
    assert sot_eligible("slack") is False
    assert sot_eligible("github-projects") is True
    assert sot_eligible("no-such-track") is False


def test_item_carries_homolog_link():
    rec = asdict(item(homolog_link="https://example.test/hms/1", branch="feat/x"))
    assert rec["homolog_link"] == "https://example.test/hms/1"


def test_guard_refuses_sot_originating_closed():
    from sync_core import guard_mirror_writes
    closed = [item(wi_state="CLOSED")]
    assert guard_mirror_writes(closed, is_sot=True) == []
    assert guard_mirror_writes(closed, is_sot=False) == closed


def test_apply_keeps_connector_http_dry(tmp_path, monkeypatch):
    from sync_core import connector_http_dry
    assert connector_http_dry(apply_flag=True) is True
    assert connector_http_dry(apply_flag=False) is True


def test_slack_post_never_sends_http(monkeypatch):
    import connectors.slack as slack

    called = []

    def _forbidden(*_a, **_k):
        called.append(True)
        raise AssertionError("Slack must not send HTTP")

    monkeypatch.setattr(slack, "_call", _forbidden, raising=False)
    slack._post("x", "delivery-updates", "hello", dry_run=False)
    assert called == []


def test_state_names_and_categories_come_from_the_model():
    from sync_core import CATEGORIES, STATE_BY_NAME, COLUMN_BY_NAME, category_of, HUMAN_ONLY_STATES
    assert CATEGORIES == ["NEW", "ACTIVE", "RESOLVED", "CLOSED", "REMOVED"]
    assert STATE_BY_NAME["Awaiting test"] == "AWAITING_TEST"
    assert STATE_BY_NAME["Closed"] == "CLOSED"
    assert len(STATE_BY_NAME) == 12
    assert COLUMN_BY_NAME["Done"] == "DONE"
    assert category_of("PREPARE_RELEASE") == "RESOLVED" and category_of("resolved") == "RESOLVED"
    assert {"CLOSED", "REMOVED"} <= HUMAN_ONLY_STATES and "IN_DEVELOPMENT" not in HUMAN_ONLY_STATES


def test_diff_rejection_is_detected_by_category():
    prev = {"WI-1": asdict(item(wi_state="AWAITING_TEST"))}
    _, _, events = diff(prev, [item(wi_state="IN_DEVELOPMENT")])
    assert events[0].kind == "rejected"


def test_guard_uses_categories_for_human_only_states():
    from sync_core import guard_mirror_writes
    assert guard_mirror_writes([item(wi_state="REMOVED")], is_sot=True) == []
    kept = guard_mirror_writes([item(wi_state="INTEGRATION_TEST")], is_sot=True)
    assert [k.wi_state for k in kept] == ["INTEGRATION_TEST"]


API = Path(__file__).resolve().parent / "fixtures" / "api"


def test_github_projects_maps_branch_and_change_from_org_fixture():
    import json
    from connectors.github_projects import items_from_payload

    data = json.loads((API / "github" / "project-org.json").read_text(encoding="utf-8"))
    items = items_from_payload(data)
    assert len(items) == 1
    assert items[0].id == "#42"
    assert items[0].branch == "feat/export-list"
    assert items[0].change_link == "https://github.com/example-org/delivery/pull/42"
    assert items[0].homolog_link == "https://example.test/hms/42"
    assert items[0].claim == "app"


def test_github_projects_reads_user_owned_project():
    import json
    from connectors.github_projects import items_from_payload

    data = json.loads((API / "github" / "project-user.json").read_text(encoding="utf-8"))
    items = items_from_payload(data)
    assert [i.id for i in items] == ["#7"]
    assert items[0].branch == "docs/start"
    assert items[0].change_link == "https://github.com/example-org/delivery/pull/7"


def test_azure_connector_maps_trace_fields_from_fixture():
    import json
    from connectors.azure_devops import items_from_workitems

    data = json.loads((API / "azure" / "workitems.json").read_text(encoding="utf-8"))
    items = items_from_workitems(data)
    assert items[0].id == "101"
    assert items[0].branch == "feat/export-list"
    assert items[0].change_link == "https://dev.azure.com/example-org/Delivery/_git/delivery/pullrequest/9"
    assert items[0].homolog_link == "https://example.test/hms/101"


def test_notion_connector_maps_trace_fields_from_fixture():
    import json
    from connectors.notion import items_from_query

    data = json.loads((API / "notion" / "database-query.json").read_text(encoding="utf-8"))
    items = items_from_query(data)
    assert items[0].id == "WI-42"
    assert items[0].branch == "feat/export-list"
    assert items[0].change_link == "https://example.test/change/42"


def test_spreadsheet_connector_reads_a_csv_export(tmp_path):
    from connectors.spreadsheet import make
    export = tmp_path / "work-items.csv"
    export.write_text(
        "ID,Type,Title,WI-State,Status,Parent,Tags,Effort,Updated\n"
        "WI-1,Story,Export the list,Awaiting test,Awaiting test,WI-0,\"needs-human, doc\",3,2026-01-16\n"
        "WI-2,Task,Write the tests,In development,In development,WI-1,,,\n"
        ",,,,,,,,\n",
        encoding="utf-8",
    )
    items = make({"export_path": str(export)}, True).read()
    assert [i.id for i in items] == ["WI-1", "WI-2"]
    assert items[0].wi_state == "AWAITING_TEST" and items[0].status == "AWAITING_TEST"
    assert items[0].tags == ["needs-human", "doc"] and items[0].effort == 3.0
    assert items[1].type == "TASK" and items[1].parent == "WI-1" and items[1].effort is None
