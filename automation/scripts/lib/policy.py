"""Gates and transitions as data. The PR validator reads these files; it does not
re-state their meaning in Python.

Canon: RULE-RISK-GATES · RULE-STATES · RULE-STATE-RESOLVED-NOT-CLOSED
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from .model import REPO_ROOT, load_yaml, model

GATES_PATH = REPO_ROOT / "agents" / "policies" / "gates.yml"


@lru_cache(maxsize=8)
def gates(path: str | None = None) -> dict:
    return load_yaml(Path(path) if path else GATES_PATH)


def gate_level(risk: str, path: str | None = None) -> dict:
    key = (risk or "low").lower()
    levels = gates(path).get("levels") or {}
    return dict(levels.get(key) or levels.get("high") or {})


def reviewers_mode(risk: str, path: str | None = None) -> str:
    to_resolved = (gate_level(risk, path).get("to_resolved") or {})
    return str(to_resolved.get("reviewers") or "all_scope_reviewers")


def named_human_required(risk: str, path: str | None = None) -> bool:
    to_resolved = (gate_level(risk, path).get("to_resolved") or {})
    return to_resolved.get("named_human") is True


def transitions() -> dict:
    return model("transitions")


def find_transition(current: str, target: str) -> dict | None:
    if not current or not target:
        return None
    for row in transitions().get("transitions") or []:
        if row.get("from") == current and row.get("to") == target:
            return row
    return None


def forbidden_hits(current: str, target: str, actor: str) -> list[dict]:
    actor = (actor or "").lower()
    hits = []
    for row in transitions().get("forbidden") or []:
        frm, to = row.get("from"), row.get("to")
        if to not in (target, "*"):
            continue
        if frm not in (current, "*"):
            continue
        allowed_by = [b.lower() for b in (row.get("by") or [])]
        if allowed_by and actor not in allowed_by:
            continue
        hits.append(row)
    return hits


def split_reason(reason: str) -> tuple[str, str]:
    text = (reason or "").strip() or "transition is forbidden"
    if " — " in text:
        rule, msg = text.split(" — ", 1)
        return rule.strip(), msg.strip()
    if text.startswith("RULE-"):
        return text.split()[0], text
    return "RULE-STATES", text


def human_roles_for(target: str) -> set[str]:
    """Who the model allows to enter this category, from transition rows."""
    out: set[str] = set()
    for row in transitions().get("transitions") or []:
        if row.get("to") == target and row.get("human_only"):
            out.update(b.lower() for b in (row.get("by") or []))
    return out
