"""Iteration names from a pattern — RULE-ITERATION-NAMING.

Pure functions, shared by the CLI (automation/scripts/iteration_name.py), the instance check
and the tests. The default pattern and reset live in core/model/iterations.yml → naming; an
instance may override both under cadence:. The model names no weekday: the defaults for the
start day and the sprint-close day are here, in automation, and every shipped instance states
its own.
"""

from __future__ import annotations

import datetime as dt
import re
import string

from lib import model as M

WEEKDAYS: tuple[str, ...] = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
WEEKEND: frozenset[str] = frozenset({"saturday", "sunday"})
DEFAULT_START_DAY = "monday"        # planning day, first day of the iteration
DEFAULT_SPRINT_CLOSE = "friday"     # review → retrospective → refinement, one session
RESETS: tuple[str, ...] = ("year", "quarter", "never")

PLACEHOLDERS: dict[str, str] = {
    "seq": "sequence number since the last reset; {seq:02} zero-pads to two digits",
    "yy": "two-digit year of the start date",
    "yyyy": "four-digit year of the start date",
    "quarter": "quarter of the start date, 1 to 4",
    "half": "half of the year of the start date, 1 or 2",
    "product": "organization.product from the instance",
    "start": "start date, ISO 8601",
    "end": "end date, ISO 8601",
}
_SEQ_SPEC = re.compile(r"^0\d$")


def naming_defaults() -> dict:
    """The model's `naming:` block: pattern, sequence_resets, placeholders."""
    return dict(M.model("iterations")["naming"])


def supported() -> str:
    return "seq, seq:02, yy, yyyy, quarter, half, product, start, end"


def parse(pattern: str) -> list[tuple[str | None, str, str | None]]:
    """(field, format spec, conversion) per placeholder; raises ValueError on unbalanced braces."""
    out = []
    for _literal, field, spec, conversion in string.Formatter().parse(pattern):
        if field is not None:
            out.append((field, spec or "", conversion))
    return out


def validate_pattern(pattern: str | None) -> list[str]:
    """Every problem with a pattern, in plain sentences. Empty list means it renders."""
    if not pattern or not str(pattern).strip():
        return ["the pattern is empty"]
    try:
        parts = parse(str(pattern))
    except ValueError as exc:
        return [f"unbalanced braces ({exc})"]
    problems: list[str] = []
    if not parts:
        problems.append("the pattern has no placeholder — a fixed name cannot tell iterations apart")
    for field, spec, conversion in parts:
        if field not in PLACEHOLDERS:
            problems.append(f"unknown placeholder {{{field}}} — supported: {supported()}")
            continue
        if conversion:
            problems.append(f"{{{field}!{conversion}}}: conversions are not supported")
        if spec and field != "seq":
            problems.append(f"{{{field}:{spec}}}: only seq takes a format ({{seq:02}})")
        elif spec and not _SEQ_SPEC.match(spec):
            problems.append(f"{{seq:{spec}}}: the only format is zero padding, {{seq:02}}")
    return problems


def uses(pattern: str, field: str) -> bool:
    try:
        return any(f == field for f, _s, _c in parse(str(pattern)))
    except ValueError:
        return False


def weekday_index(name: str) -> int:
    key = str(name).strip().lower()
    if key not in WEEKDAYS:
        raise ValueError(f"'{name}' is not a weekday — one of {', '.join(WEEKDAYS)}")
    return WEEKDAYS.index(key)


def quarter_of(day: dt.date) -> int:
    return (day.month - 1) // 3 + 1


def half_of(day: dt.date) -> int:
    return 1 if day.month <= 6 else 2


def first_start_on_or_after(day: dt.date, start_day: str) -> dt.date:
    """The first date on or after `day` that falls on the start weekday."""
    return day + dt.timedelta(days=(weekday_index(start_day) - day.weekday()) % 7)


def period_start(start: dt.date, resets: str) -> dt.date:
    if resets == "year":
        return dt.date(start.year, 1, 1)
    if resets == "quarter":
        return dt.date(start.year, 3 * (quarter_of(start) - 1) + 1, 1)
    raise ValueError("--seq is required: cadence.sequence_resets is never, so nothing derives the count")


def derive_seq(start: dt.date, start_day: str, resets: str, length_days: int) -> int:
    """Sequence number of the iteration that starts on `start`: how many iteration starts
    since the first start day of the period. Only for seven-day iterations, because only
    then does 'one iteration per start day' hold; otherwise the caller passes the number."""
    if int(length_days) != 7:
        raise ValueError("--seq is required: the sequence is derived only for seven-day iterations")
    if start.weekday() != weekday_index(start_day):
        raise ValueError(f"{start.isoformat()} is a {start.strftime('%A')}; cadence.iteration_start_day is {start_day}")
    first = first_start_on_or_after(period_start(start, resets), start_day)
    return (start - first).days // 7 + 1


def end_of(start: dt.date, length_days: int) -> dt.date:
    return start + dt.timedelta(days=int(length_days) - 1)


def close_date(start: dt.date, length_days: int, sprint_close: str) -> dt.date:
    """The last day of the iteration that falls on the sprint-close weekday."""
    end = end_of(start, length_days)
    close = end - dt.timedelta(days=(end.weekday() - weekday_index(sprint_close)) % 7)
    if close < start:
        raise ValueError(f"no {sprint_close} between {start.isoformat()} and {end.isoformat()}")
    return close


def render_name(pattern: str, *, seq: int, start: dt.date, length_days: int, product: str | None = None) -> str:
    problems = validate_pattern(pattern)
    if problems:
        raise ValueError("; ".join(problems))
    if uses(pattern, "product") and not (product or "").strip():
        raise ValueError("the pattern uses {product} but organization.product is not set (RULE-ITERATION-NAMING)")
    values = {
        "seq": int(seq),
        "yy": f"{start.year % 100:02d}",
        "yyyy": str(start.year),
        "quarter": quarter_of(start),
        "half": half_of(start),
        "product": (product or "").strip(),
        "start": start.isoformat(),
        "end": end_of(start, length_days).isoformat(),
    }
    return pattern.format(**values)
