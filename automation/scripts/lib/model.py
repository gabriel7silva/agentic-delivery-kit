"""One loader for the neutral model, shared by every check and by the validator.

Anything that needs a symbol, a state, a rule or a capability goes through here,
so the definition of "the symbol set" exists in exactly one place.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = REPO_ROOT / "core" / "model"
TRACKS_DIR = REPO_ROOT / "tracks"
SCHEMAS_DIR = REPO_ROOT / "schemas"

# Entities are listed in core/model/README.md; they have no YAML of their own.
ENTITIES: tuple[str, ...] = (
    "ITEM", "ITEM_PARENT", "ITERATION", "CLAIM", "REVIEW_GATE", "CHANGE_REQUEST",
    "EVIDENCE_LINK", "CONCLUSION_COMMENT", "CEREMONY_MINUTES", "DIGEST",
)

# The state and column groups are mapped as one symbol each, carrying `values`.
GROUP_SYMBOLS: tuple[str, ...] = ("WI_STATE", "STATUS")


def load_yaml(path: Path | str) -> Any:
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@lru_cache(maxsize=None)
def model(name: str) -> dict:
    """core/model/<name>.yml as a dict."""
    return load_yaml(MODEL_DIR / f"{name}.yml")


def item_types() -> list[str]:
    return [t["id"] for t in model("item-types")["types"]]


def states() -> list[str]:
    return [s["id"] for s in model("item-states")["states"]]


def columns() -> list[str]:
    return [c["id"] for c in model("board-columns")["columns"]]


def categories() -> list[str]:
    """The five lifecycle categories, in order. They never change; states do."""
    return [c["id"] for c in model("item-states")["categories"]]


def state_category() -> dict[str, str]:
    return {s["id"]: s["category"] for s in model("item-states")["states"]}


def category_of(state: str | None) -> str | None:
    """Category of a state id — or the id itself when it already names a category.
    None when the value is neither. Case-insensitive, so contexts may say 'active'."""
    key = (state or "").strip().upper()
    if key in categories():
        return key
    return state_category().get(key)


def states_in(category: str) -> list[str]:
    return [s for s, c in state_category().items() if c == category]


def state_names() -> dict[str, str]:
    """Display name per state id — the default tool value in every track."""
    return {s["id"]: s["name"] for s in model("item-states")["states"]}


def human_only_states() -> set[str]:
    """States nobody but a human may set: those in a human-only category, plus the
    category ids themselves (a context may name the category)."""
    human = {c["id"] for c in model("item-states")["categories"] if c.get("human_only")}
    return {s for s, c in state_category().items() if c in human} | human


def fields() -> list[str]:
    return [f["id"] for f in model("fields")["fields"]]


def rules() -> list[dict]:
    return model("rules")["rules"]


def rule_ids() -> set[str]:
    return {r["id"] for r in rules()}


def capability_ids() -> list[str]:
    return [c["id"] for c in model("capabilities")["capabilities"]]


def symbols() -> set[str]:
    """Every symbol a track must map. Union, de-duplicated: a field with the
    same id as an entity (ITERATION, CLAIM) is the same symbol."""
    out: set[str] = set(ENTITIES)
    out.update(item_types())
    out.update(GROUP_SYMBOLS)
    out.update(fields())
    return out


def track_dirs() -> list[Path]:
    return sorted(
        p for p in TRACKS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith("_")
    )


def track(name: str) -> tuple[dict, dict]:
    """(mapping, capabilities) for one track."""
    base = TRACKS_DIR / name
    return load_yaml(base / "mapping.yml"), load_yaml(base / "capabilities.yml")


def rel(path: Path) -> str:
    """Repository-relative path for reports."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)
