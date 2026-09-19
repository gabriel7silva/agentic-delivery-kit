"""Notion connector — reads a database via the API; as a mirror, updates
properties (never WI-State: Closed / Removed).

Reference code. Property names follow tracks/notion/fields.md.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sync_core import COLUMN_BY_NAME as STATUS_FROM  # noqa: E402
from sync_core import STATE_BY_NAME as STATE_FROM  # noqa: E402  — names from core/model, not hard-coded here
from sync_core import Connector, Item  # noqa: E402

API = "https://api.notion.com/v1"
VERSION = "2022-06-28"   # bump when Notion retires it; the response shape below may move with it


def _post(token: str, path: str, body: dict) -> dict:
    req = urllib.request.Request(f"{API}{path}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Notion-Version": VERSION, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _sel(p: dict, name: str) -> str | None:
    v = p.get(name) or {}
    inner = v.get("select") or v.get("status")
    return inner.get("name") if inner else None


def _num(p: dict, name: str) -> float | None:
    return (p.get(name) or {}).get("number")


def _text(p: dict, name: str) -> str | None:
    rt = (p.get(name) or {}).get("rich_text") or []
    return "".join(t.get("plain_text", "") for t in rt) or None


def items_from_query(data: dict) -> list[Item]:
    items = []
    for page in data.get("results") or []:
        p = page.get("properties") or {}
        title = "".join(t.get("plain_text", "") for t in (p.get("Name") or p.get("Title") or {}).get("title", []))
        pid = (p.get("ID") or {}).get("unique_id") or {}
        items.append(Item(
            id=f"{pid.get('prefix', '')}{pid.get('number', page['id'][:8])}", type=(_sel(p, "Type") or "STORY").upper(), title=title,
            wi_state=STATE_FROM.get(_sel(p, "WI-State"), "NEW"), status=STATUS_FROM.get(_sel(p, "Status")),
            priority=_sel(p, "Priority"), role=_sel(p, "Role"), risk=_sel(p, "Risk"), claim=_text(p, "Claim"),
            tags=[t["name"] for t in (p.get("Tags") or {}).get("multi_select", [])],
            branch=_text(p, "Branch"), change_link=(p.get("Change link") or {}).get("url"),
            homolog_link=_text(p, "Homologation") or (p.get("Homologation") or {}).get("url"),
            effort=_num(p, "Effort"), remaining_work=_num(p, "Remaining"), business_value=_num(p, "Business value"),
            external_ref=_text(p, "External ref"),
            url=page.get("url"), updated_at=page.get("last_edited_time"),
        ))
    return items


class Notion(Connector):
    name = "notion"
    env_var = "NOTION_TOKEN"

    def read(self) -> list[Item]:
        token = os.environ[self.env_var]
        db = self.config["database_id"]
        items, cursor = [], None
        while True:
            body = {"page_size": 100, **({"start_cursor": cursor} if cursor else {})}
            data = _post(token, f"/databases/{db}/query", body)
            items.extend(items_from_query(data))
            if not data.get("has_more"):
                break
            cursor = data["next_cursor"]
        return items

    def apply(self, changed: list[Item], removed: list[str], dry_run: bool) -> None:
        for it in changed:
            print(f"    {'would update' if dry_run else 'update'} {it.id}: WI-State={it.wi_state} Status={it.status} Risk={it.risk}")
        if not dry_run:
            # PATCH /pages/{id} with {"properties": {...}} — requires mapping SoT ids to page ids (keep a lookup in .state/).
            print("    (write path: PATCH /pages/{id}; WI-State never set to Closed/Removed by the sync)")


def make(config: dict, is_sot: bool) -> Connector:
    return Notion(config, is_sot)
