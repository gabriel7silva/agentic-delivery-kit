#!/usr/bin/env python3
"""Neutral sync engine: read the source of truth, diff, print intended mirror
writes. Connectors do not send HTTP PATCHes; `--apply` only writes the local
`.state/` snapshot.

Usage:
    sync_core.py --config config.yml [--apply] [--digest]
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

STATE_DIR = Path(__file__).resolve().parent / ".state"   # last-seen snapshots per mirror; git-ignored
MODEL_DIR = Path(__file__).resolve().parents[2] / "core" / "model"


def _model(name: str) -> dict:
    return yaml.safe_load((MODEL_DIR / f"{name}.yml").read_text(encoding="utf-8")) or {}


# The lifecycle comes from the model, never from a connector: a track's tool value for
# a state is its display name in core/model/item-states.yml unless mapping.yml says otherwise.
_STATES = _model("item-states")
CATEGORIES = [c["id"] for c in _STATES.get("categories", [])]
STATE_CATEGORY = {s["id"]: s["category"] for s in _STATES.get("states", [])}
STATE_BY_NAME = {s["name"]: s["id"] for s in _STATES.get("states", [])}
COLUMN_BY_NAME = {c["name"]: c["id"] for c in _model("board-columns").get("columns", [])}
HUMAN_ONLY_CATEGORIES = {c["id"] for c in _STATES.get("categories", []) if c.get("human_only")}
HUMAN_ONLY_STATES = {s for s, c in STATE_CATEGORY.items() if c in HUMAN_ONLY_CATEGORIES} | HUMAN_ONLY_CATEGORIES


def category_of(state: str | None) -> str | None:
    """Category of a state id, or the id itself when it already names a category."""
    key = (state or "").strip().upper()
    if key in CATEGORIES:
        return key
    return STATE_CATEGORY.get(key)


@dataclass
class Item:
    """The neutral shape every connector reads into and writes from."""
    id: str
    type: str                      # EPIC | FEATURE | STORY | TASK | BUG | ISSUE
    title: str
    wi_state: str                  # a state id from core/model/item-states.yml (or a category id)
    status: str | None = None      # a column id from core/model/board-columns.yml
    parent: str | None = None
    iteration: str | None = None
    priority: str | None = None
    role: str | None = None
    risk: str | None = None
    claim: str | None = None
    tags: list[str] = field(default_factory=list)
    branch: str | None = None
    change_link: str | None = None
    homolog_link: str | None = None
    effort: float | None = None
    remaining_work: float | None = None
    business_value: float | None = None
    external_ref: str | None = None
    url: str | None = None
    updated_at: str | None = None


@dataclass
class Event:
    item_id: str
    kind: str                      # state | claim | release | rejected
    detail: str


class Connector:
    """Protocol. Subclasses override what they support; the engine checks."""
    name = "abstract"
    env_var: str | None = None

    def __init__(self, config: dict, is_sot: bool):
        self.config = config
        self.is_sot = is_sot
        if self.env_var and not os.environ.get(self.env_var):
            print(f"{self.name}: {self.env_var} is not set — refusing to start (SECURITY.md)", file=sys.stderr)
            sys.exit(2)

    def read(self) -> list[Item]:
        raise NotImplementedError(f"{self.name} cannot be a source of truth")

    def apply(self, changed: list[Item], removed: list[str], dry_run: bool) -> None:
        raise NotImplementedError(f"{self.name} cannot be a mirror")

    def post_events(self, events: list[Event], dry_run: bool) -> None:
        pass

    def post_digest(self, items: list[Item], dry_run: bool) -> None:
        pass


def load_connector(track: str, config: dict, is_sot: bool) -> Connector:
    mod = importlib.import_module(f"connectors.{track.replace('-', '_')}")
    return mod.make(config, is_sot)


def sot_eligible(track: str) -> bool:
    path = Path(__file__).resolve().parents[2] / "tracks" / track / "capabilities.yml"
    if not path.is_file():
        return False
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return bool((data.get("capabilities") or {}).get("sot_eligible"))


def connector_http_dry(apply_flag: bool) -> bool:
    """--apply writes the local snapshot only. Connectors never send HTTP from this flag."""
    return True


def guard_mirror_writes(changed: list[Item], *, is_sot: bool) -> list[Item]:
    """A SoT write path may not originate CLOSED/REMOVED. Mirrors may display them."""
    if not is_sot:
        return list(changed)
    kept = [it for it in changed if category_of(it.wi_state) not in HUMAN_ONLY_CATEGORIES]
    blocked = [it.id for it in changed if category_of(it.wi_state) in HUMAN_ONLY_CATEGORIES]
    for iid in blocked:
        print(f"  refused originating {iid} CLOSED/REMOVED (RULE-STATE-RESOLVED-NOT-CLOSED)", file=sys.stderr)
    return kept


def diff(previous: dict[str, dict], current: list[Item]) -> tuple[list[Item], list[str], list[Event]]:
    changed, events = [], []
    now = {i.id: asdict(i) for i in current}
    for iid, rec in now.items():
        old = previous.get(iid)
        if old != rec:
            changed.append(Item(**rec))
            if old and old.get("wi_state") != rec["wi_state"]:
                kind = "rejected" if (category_of(old["wi_state"]), category_of(rec["wi_state"])) == ("RESOLVED", "ACTIVE") else "state"
                events.append(Event(iid, kind, f"{old['wi_state']} → {rec['wi_state']}"))
            if old and old.get("claim") != rec.get("claim"):
                events.append(Event(iid, "release" if not rec.get("claim") else "claim", rec.get("claim") or "released"))
    removed = [iid for iid in previous if iid not in now]
    return changed, removed, events


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--apply", action="store_true", help="write the local .state/ snapshot (connectors still only print; default: dry run)")
    ap.add_argument("--digest", action="store_true", help="also post the daily digest")
    a = ap.parse_args()
    dry = connector_http_dry(a.apply)

    cfg = yaml.safe_load(a.config.read_text(encoding="utf-8"))
    sot_track = cfg["source_of_truth"]["track"]
    if not sot_eligible(sot_track):
        print(f"{sot_track} cannot be the source of truth (capabilities.sot_eligible is false)", file=sys.stderr)
        return 2

    sot = load_connector(sot_track, cfg["source_of_truth"].get(sot_track.replace("-", "_"), {}), is_sot=True)
    items = sot.read()
    print(f"{'DRY RUN — ' if dry else ''}read {len(items)} item(s) from {sot_track}")

    STATE_DIR.mkdir(exist_ok=True)
    all_events: list[Event] = []
    for m in cfg.get("mirrors", []):
        track = m["track"]
        snap = STATE_DIR / f"{track}.json"
        previous = json.loads(snap.read_text(encoding="utf-8")) if snap.is_file() else {}
        changed, removed, events = diff(previous, items)
        changed = guard_mirror_writes(changed, is_sot=False)
        print(f"  {track}: {len(changed)} changed · {len(removed)} removed · {len(events)} event(s)")
        conn = load_connector(track, m.get(track.replace("-", "_"), {}), is_sot=False)
        conn.apply(changed, removed, dry_run=dry)
        conn.post_events(events, dry_run=dry)
        if a.digest:
            conn.post_digest(items, dry_run=dry)
        if a.apply:
            snap.write_text(json.dumps({i.id: asdict(i) for i in items}, indent=1), encoding="utf-8")
        all_events += events

    if a.apply:
        print("--apply wrote the local .state/ snapshot; connectors did not send HTTP.")
    else:
        print("nothing written. --apply writes only the local .state/ snapshot; connectors still print.")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
