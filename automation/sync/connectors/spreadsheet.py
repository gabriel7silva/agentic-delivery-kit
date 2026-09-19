"""Spreadsheet connector — reads a CSV or TSV export of the "Work items" sheet. It never
writes: people edit the sheet, and the sync only mirrors it elsewhere.

Config: { "export_path": "<path to the export>" }. Columns as tracks/spreadsheet/fields.md;
state and column names come from the model, so a renamed state must be renamed in the export
too — or mapped by the instance's lifecycle labels before export.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sync_core import COLUMN_BY_NAME, STATE_BY_NAME, Connector, Item  # noqa: E402

TYPE_FROM = {"Epic": "EPIC", "Feature": "FEATURE", "Story": "STORY", "Task": "TASK", "Bug": "BUG", "Issue": "ISSUE"}


def _num(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None


class Spreadsheet(Connector):
    name = "spreadsheet"
    env_var = None          # a file export needs no token

    def read(self) -> list[Item]:
        path = Path(self.config["export_path"])
        with path.open(encoding="utf-8", newline="") as fh:
            sample = fh.read(4096)
            fh.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel
            rows = list(csv.DictReader(fh, dialect=dialect))
        items: list[Item] = []
        for r in rows:
            def g(key: str) -> str | None:
                return (r.get(key) or "").strip() or None
            if not g("ID"):
                continue
            items.append(Item(
                id=g("ID") or "", type=TYPE_FROM.get(g("Type") or "", "STORY"), title=g("Title") or "",
                wi_state=STATE_BY_NAME.get(g("WI-State") or "", "NEW"), status=COLUMN_BY_NAME.get(g("Status") or ""),
                parent=g("Parent"), iteration=g("Iteration"), priority=g("Priority"), role=g("Role"), risk=g("Risk"),
                claim=g("Claim"), tags=[t.strip() for t in (g("Tags") or "").split(",") if t.strip()],
                branch=g("Branch"), change_link=g("Change"), homolog_link=g("Homologation"),
                effort=_num(g("Effort")), remaining_work=_num(g("Remaining")), business_value=_num(g("Business value")),
                external_ref=g("External ref"), updated_at=g("Updated"),
            ))
        return items

    def apply(self, changed: list[Item], removed: list[str], dry_run: bool) -> None:
        for it in changed:
            print(f"    {'would write' if dry_run else 'write'} row {it.id}: WI-State={it.wi_state} Status={it.status}")
        if not dry_run:
            print("    (write path: none — people edit the sheet; the sync reads its export)")


def make(config: dict, is_sot: bool) -> Connector:
    return Spreadsheet(config, is_sot)
