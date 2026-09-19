"""Unit tests for the path → scope → floor resolution the validator relies on."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.diffscope import Ownership, glob_to_regex, max_risk, missing_reviewers, specificity  # noqa: E402

OWN = {
    "version": 1,
    "default_scope": {"writer": "implementer", "reviewers": ["reviewer-correctness"], "floor": "medium"},
    "scopes": [
        {"id": "docs", "paths": ["docs/**", "*.md"], "writer": "implementer", "reviewers": ["reviewer-docs"], "floor": "low"},
        {"id": "app", "paths": ["src/**"], "writer": "implementer", "reviewers": ["reviewer-correctness"], "floor": "medium"},
        {"id": "data", "paths": ["src/storage/**"], "writer": "implementer", "reviewers": ["reviewer-security"], "floor": "high"},
    ],
}
FLOORS = {"version": 1, "policy": "risk-floors", "floors": [
    {"paths": ["src/storage/**"], "floor": "high"},
    {"paths": ["**/*.policy.*"], "floor": "high"},
]}


def test_glob_double_star_any_depth():
    rx = glob_to_regex("src/**")
    assert rx.match("src/a.py") and rx.match("src/x/y/z.py")
    assert not rx.match("lib/a.py")


def test_glob_double_star_prefix():
    rx = glob_to_regex("**/*.policy.*")
    assert rx.match("a.policy.yml") and rx.match("x/y/a.policy.json")


def test_glob_star_single_segment():
    rx = glob_to_regex("*.md")
    assert rx.match("README.md") and not rx.match("docs/README.md")


def test_specificity_prefers_longer_literal():
    assert specificity("src/storage/**") > specificity("src/**")


def test_most_specific_scope_wins():
    own = Ownership(OWN, FLOORS)
    assert own.scope_for("src/storage/w.py").id == "data"
    assert own.scope_for("src/main.py").id == "app"
    assert own.scope_for("docs/x.md").id == "docs"


def test_unmatched_goes_to_default():
    own = Ownership(OWN, FLOORS)
    assert own.scope_for("Makefile").id == "default"
    assert own.floor_for("Makefile", own.default) == "medium"


def test_floor_from_policy_overrides_scope_floor():
    """A high-floor glob applies even inside a low-floor scope."""
    own = Ownership(OWN, FLOORS)
    r = own.resolve(["docs/access.policy.md"])[0]
    assert r.scope.id == "docs" and r.floor == "high"


def test_duplicate_globs_detected():
    dup = {**OWN, "scopes": OWN["scopes"] + [{"id": "again", "paths": ["src/**"], "writer": "implementer", "reviewers": ["reviewer-docs"], "floor": "low"}]}
    assert Ownership(dup).duplicate_globs() == [("src/**", "app", "again")]


def test_max_risk():
    assert max_risk([]) == "low"
    assert max_risk(["low", "medium"]) == "medium"
    assert max_risk(["low", "high", "medium"]) == "high"


def test_max_risk_unknown_is_high():
    assert max_risk(["low", "critical"]) == "high"
    assert max_risk(["High"]) == "high"


def test_missing_reviewers_low_is_one_from_the_pool():
    own = Ownership({
        **OWN,
        "scopes": [
            {**OWN["scopes"][0], "reviewers": ["reviewer-docs", "reviewer-delivery-compliance"]},
            *OWN["scopes"][1:],
        ],
    }, FLOORS)
    docs = own.resolve(["README.md"])
    assert missing_reviewers(docs, {"reviewer-docs"}, "low") == []
    assert missing_reviewers(docs, set(), "low") == ["reviewer-delivery-compliance", "reviewer-docs"]


def test_missing_reviewers_medium_needs_all():
    own = Ownership({
        **OWN,
        "scopes": [
            {**OWN["scopes"][1], "reviewers": ["reviewer-correctness", "reviewer-delivery-compliance"]},
            OWN["scopes"][0],
            OWN["scopes"][2],
        ],
    }, FLOORS)
    res = own.resolve(["src/main.py"])
    assert "reviewer-delivery-compliance" in missing_reviewers(res, {"reviewer-correctness"}, "medium")
    assert missing_reviewers(res, {"reviewer-correctness", "reviewer-delivery-compliance"}, "medium") == []
