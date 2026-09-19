"""Slack connector — posts item events, the daily digest, and updates the mirror
List. Reads nothing. Can never be a source of truth.

Message shapes follow tracks/slack/event-formats/.
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sync_core import Connector, Event, Item, category_of  # noqa: E402


def _post(token: str, channel: str, text: str, dry_run: bool) -> None:
    # Live HTTP does not ship. --apply writes .state/ only; a --post flag is not implemented.
    del token, dry_run
    print(f"    would post to #{channel}:\n      " + text.replace("\n", "\n      "))


class Slack(Connector):
    name = "slack"
    env_var = "SLACK_BOT_TOKEN"

    def __init__(self, config: dict, is_sot: bool):
        if is_sot:
            print("slack can never be the source of truth", file=sys.stderr)
            sys.exit(2)
        super().__init__(config, is_sot)
        self.ch = config.get("channels", {})

    def apply(self, changed: list[Item], removed: list[str], dry_run: bool) -> None:
        # Mirror List rows — slackLists.items.* methods; shape varies by workspace plan, so this
        # prints the intent and leaves the call to the adopter.
        for it in changed:
            print(f"    would upsert List row {it.id}: {it.wi_state}/{it.status}")

    def post_events(self, events: list[Event], dry_run: bool) -> None:
        token = os.environ[self.env_var]
        by_item: dict[str, list[Event]] = defaultdict(list)
        for e in events:
            by_item[e.item_id].append(e)
        for iid, evs in by_item.items():
            for e in evs:
                text = f"[{iid}]\n{e.detail}" if e.kind in ("state", "claim", "release") else f"[{iid}]\n{e.detail} · REJECTED"
                _post(token, self.ch.get("updates", "delivery-updates"), text, dry_run)

    def post_digest(self, items: list[Item], dry_run: bool) -> None:
        token = os.environ[self.env_var]
        # Sections are by CATEGORY (core/model/item-states.yml), whatever states the instance runs.
        active = [i for i in items if category_of(i.wi_state) == "ACTIVE"]
        blockers = [i for i in items if i.type == "ISSUE" and category_of(i.wi_state) != "CLOSED"]
        decisions = [i for i in items if "needs-human" in i.tags and category_of(i.wi_state) not in ("CLOSED", "REMOVED")]
        review = sorted((i for i in items if category_of(i.wi_state) == "RESOLVED"), key=lambda i: i.updated_at or "")
        inconsistent = [i for i in items if i.status == "DONE" and category_of(i.wi_state) != "CLOSED"]

        def block(title: str, rows: list[Item], fmt) -> str:
            body = "\n".join(f"  {fmt(i)}" for i in rows) if rows else "  none"
            return f"{title} ({len(rows)})\n{body}"

        text = "\n\n".join([
            f"Daily digest · {date.today().isoformat()}",
            block("1 · Active", active, lambda i: f"{i.id} {i.title} — {i.role or ''}"),
            block("2 · Blockers", blockers, lambda i: f"{i.id} {i.title}"),
            block("3 · Decisions needed from a human", decisions, lambda i: f"{i.id} {i.title} — {i.wi_state}"),
            block("4 · Ready for review (oldest first)", review, lambda i: f"{i.id} {i.title} — risk {i.risk or '?'} — since {i.updated_at or '?'}"),
            block("Inconsistencies", inconsistent, lambda i: f"{i.id} — Status DONE but WI-State {i.wi_state}"),
        ])
        _post(token, self.ch.get("digest", "delivery-digest"), text, dry_run)


def make(config: dict, is_sot: bool) -> Connector:
    return Slack(config, is_sot)
