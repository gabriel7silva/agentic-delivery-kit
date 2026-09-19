"""Iteration names — RULE-ITERATION-NAMING: the library renders the pattern, derives the
sequence for weekly iterations, and the CLI reads the instance."""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "automation" / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))
from lib import iteration_name as IN  # noqa: E402

D = dt.date
DEFAULT = "Sprint {seq:02} {yy} Q{quarter} {product}"


def test_iteration_name_renders_the_default_pattern():
    assert IN.render_name(DEFAULT, seq=38, start=D(2026, 9, 21), length_days=7, product="Acme Portal") == "Sprint 38 26 Q3 Acme Portal"


def test_iteration_name_zero_pads_and_first_of_year():
    assert IN.render_name(DEFAULT, seq=1, start=D(2026, 1, 5), length_days=7, product="Acme Portal") == "Sprint 01 26 Q1 Acme Portal"


def test_iteration_name_every_placeholder():
    pattern = "{seq}-{seq:02}-{yy}-{yyyy}-Q{quarter}-H{half}-{product}-{start}-{end}"
    assert IN.render_name(pattern, seq=38, start=D(2026, 9, 21), length_days=7, product="Acme Portal") == \
        "38-38-26-2026-Q3-H2-Acme Portal-2026-09-21-2026-09-27"


def test_iteration_name_model_default_matches_the_library():
    naming = IN.naming_defaults()
    assert naming["pattern"] == DEFAULT and naming["sequence_resets"] == "year"
    assert {p["id"] for p in naming["placeholders"]} == set(IN.PLACEHOLDERS)


def test_iteration_name_derives_seq_for_weekly_year_reset():
    assert IN.derive_seq(D(2026, 1, 5), "monday", "year", 7) == 1
    assert IN.derive_seq(D(2026, 1, 12), "monday", "year", 7) == 2
    assert IN.derive_seq(D(2026, 9, 21), "monday", "year", 7) == 38
    assert IN.derive_seq(D(2026, 12, 28), "monday", "year", 7) == 52
    assert IN.derive_seq(D(2027, 1, 4), "monday", "year", 7) == 1


def test_iteration_name_derives_seq_for_quarter_reset():
    assert IN.derive_seq(D(2026, 7, 6), "monday", "quarter", 7) == 1
    assert IN.derive_seq(D(2026, 9, 21), "monday", "quarter", 7) == 12


def test_iteration_name_refuses_seq_derivation_when_not_weekly_or_never():
    with pytest.raises(ValueError, match="seven-day"):
        IN.derive_seq(D(2026, 9, 21), "monday", "year", 14)
    with pytest.raises(ValueError, match="never"):
        IN.derive_seq(D(2026, 9, 21), "monday", "never", 7)


def test_iteration_name_refuses_start_off_the_start_day():
    with pytest.raises(ValueError, match="Tuesday"):
        IN.derive_seq(D(2026, 9, 22), "monday", "year", 7)


def test_iteration_name_close_date():
    assert IN.close_date(D(2026, 9, 21), 7, "friday") == D(2026, 9, 25)
    assert IN.close_date(D(2026, 1, 12), 7, "friday") == D(2026, 1, 16)
    assert IN.end_of(D(2026, 1, 12), 7) == D(2026, 1, 18)


def test_iteration_name_validate_pattern_lists_problems():
    assert IN.validate_pattern(DEFAULT) == []
    assert any("unknown placeholder {sprint}" in p for p in IN.validate_pattern("{sprint} {yy}"))
    assert any("only seq takes a format" in p for p in IN.validate_pattern("{yy:02}"))
    assert any("zero padding" in p for p in IN.validate_pattern("{seq:3}"))
    assert any("unbalanced" in p for p in IN.validate_pattern("{seq"))
    assert any("no placeholder" in p for p in IN.validate_pattern("Sprint"))
    assert IN.validate_pattern("") == ["the pattern is empty"]


def test_iteration_name_product_required_when_used():
    with pytest.raises(ValueError, match="organization.product"):
        IN.render_name(DEFAULT, seq=1, start=D(2026, 1, 5), length_days=7, product=None)
    assert IN.render_name("Sprint {seq} {yyyy}", seq=1, start=D(2026, 1, 5), length_days=7) == "Sprint 1 2026"


def test_iteration_name_cli_renders_from_the_example_instance(run):
    code, out = run("iteration_name.py", "--instance", "instance.example.yml", "--seq", "38", "--start", "2026-09-21")
    assert code == 0 and out.strip() == "Sprint 38 26 Q3 Acme Portal", out


def test_iteration_name_cli_derives_seq_and_json(run):
    code, out = run("iteration_name.py", "--instance", "instance.example.yml", "--start", "2026-09-21", "--json")
    assert code == 0, out
    data = json.loads(out)
    assert data["name"] == "Sprint 38 26 Q3 Acme Portal"
    assert data["seq"] == 38 and data["sprint_close_date"] == "2026-09-25" and data["end"] == "2026-09-27"


def test_iteration_name_cli_requires_seq_for_a_fortnight(run):
    fixture = FIXTURES / "instances" / "cadence-fortnight.yml"
    code, out = run("iteration_name.py", "--instance", str(fixture), "--start", "2026-09-21")
    assert code == 2 and "--seq is required" in out
    code, out = run("iteration_name.py", "--instance", str(fixture), "--start", "2026-09-21", "--seq", "19")
    assert code == 0 and out.strip() == "Sprint 19 26 Q3 Acme Portal"
