"""The neutral model holds its own promises: five fixed categories, every state in one of
them, human-only where the method says so, and a board that covers every state."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib import model as M  # noqa: E402

FIVE = {"NEW", "ACTIVE", "RESOLVED", "CLOSED", "REMOVED"}


def test_the_five_categories_are_fixed():
    assert set(M.categories()) == FIVE
    assert M.categories() == ["NEW", "ACTIVE", "RESOLVED", "CLOSED", "REMOVED"]


def test_every_state_has_a_known_category_and_each_category_has_a_state():
    for state in M.model("item-states")["states"]:
        assert state["category"] in FIVE, state["id"]
    for cat in M.categories():
        assert M.states_in(cat), f"category {cat} has no state"


def test_closed_and_removed_are_human_only_and_nothing_else_is():
    assert M.human_only_states() == {"CLOSED", "REMOVED"}
    for state in M.model("item-states")["states"]:
        if state["category"] in ("CLOSED", "REMOVED"):
            assert state.get("human_only") is True, state["id"]
        else:
            assert not state.get("human_only"), state["id"]


def test_category_of_accepts_a_state_or_a_category_in_any_case():
    assert M.category_of("IN_DEVELOPMENT") == "ACTIVE"
    assert M.category_of("key_user_homologation") == "RESOLVED"
    assert M.category_of("active") == "ACTIVE"
    assert M.category_of("DONE") is None
    assert M.category_of("") is None


def test_default_path_and_board_cover_every_visible_state():
    states = set(M.states())
    path = M.model("item-states")["default_path"]
    assert path[0] == "NEW" and path[-1] == "CLOSED"
    assert set(path) == states - {"REMOVED", "BLOCKED"}   # Blocked sits beside In development
    assert M.category_of("BLOCKED") == "ACTIVE"
    board = M.model("board-columns")
    assert set(board["translation"]) == states
    assert board["translation"]["REMOVED"] is None
    assert {v for v in board["translation"].values() if v} == set(M.columns())
    done = next(c for c in board["columns"] if c["id"] == "DONE")
    assert done["from_state"] == "CLOSED" and done["reached_only_by"] == "CLOSED"


def test_transitions_are_written_between_categories():
    for t in M.model("transitions")["transitions"]:
        assert t["from"] in FIVE and t["to"] in FIVE, t
    closed = next(t for t in M.model("transitions")["transitions"] if t["to"] == "CLOSED")
    assert closed["from"] == "RESOLVED" and closed.get("human_only") is True


def test_optional_fields_are_backed_by_optional_rules():
    optional_rules = {r["id"] for r in M.rules() if r.get("optional")}
    new_optional = {"EFFORT", "REMAINING_WORK", "BUSINESS_VALUE", "EXTERNAL_REF"}
    for f in M.model("fields")["fields"]:
        if f["id"] in new_optional:
            assert f.get("optional") is True, f["id"]
            assert f["required_by"] in optional_rules, f'{f["id"]} is optional but {f["required_by"]} is not an optional rule'
    ids = {f["id"] for f in M.model("fields")["fields"]}
    assert {"EFFORT", "REMAINING_WORK", "BUSINESS_VALUE", "EXTERNAL_REF"} <= ids
