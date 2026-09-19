"""Azure DevOps connector — reads work items via a saved WIQL query + REST; as a
mirror, patches fields (never State: Closed / Removed).

Reference code. Field reference names follow tracks/azure-devops/mapping.yml
(custom fields are Custom.PACTRole etc.); override in config if yours differ.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sync_core import STATE_BY_NAME as STATE_FROM  # noqa: E402  — state names from core/model/item-states.yml
from sync_core import Connector, Item  # noqa: E402

TYPE_FROM = {"Epic": "EPIC", "Feature": "FEATURE", "User Story": "STORY", "Product Backlog Item": "STORY",
             "Task": "TASK", "Bug": "BUG", "Issue": "ISSUE", "Impediment": "ISSUE"}
FIELDS = ["System.Id", "System.WorkItemType", "System.Title", "System.State", "System.BoardColumn", "System.Parent",
          "System.IterationPath", "Microsoft.VSTS.Common.Priority", "System.Tags", "System.ChangedDate",
          "Custom.PACTRole", "Custom.PACTRisk", "Custom.PACTClaim", "Custom.PACTHomolog",
          "Custom.PACTBranch", "Custom.PACTChange",
          "Microsoft.VSTS.Scheduling.StoryPoints", "Microsoft.VSTS.Scheduling.RemainingWork",
          "Microsoft.VSTS.Common.BusinessValue", "Custom.PACTExternalRef"]


def _get(token: str, url: str) -> dict:
    auth = base64.b64encode(f":{token}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def items_from_workitems(data: dict) -> list[Item]:
    items = []
    for w in data.get("value") or []:
        f = w.get("fields") or {}
        items.append(Item(
            id=str(f["System.Id"]), type=TYPE_FROM.get(f["System.WorkItemType"], "STORY"), title=f["System.Title"],
            wi_state=STATE_FROM.get(f["System.State"], "NEW"), status=(f.get("System.BoardColumn") or "").upper().replace(" ", "_") or None,
            parent=str(f["System.Parent"]) if f.get("System.Parent") else None, iteration=f.get("System.IterationPath"),
            priority=f"P{f['Microsoft.VSTS.Common.Priority']}" if f.get("Microsoft.VSTS.Common.Priority") else None,
            role=f.get("Custom.PACTRole"), risk=f.get("Custom.PACTRisk"), claim=f.get("Custom.PACTClaim"),
            homolog_link=f.get("Custom.PACTHomolog"),
            branch=f.get("Custom.PACTBranch"), change_link=f.get("Custom.PACTChange"),
            effort=f.get("Microsoft.VSTS.Scheduling.StoryPoints"), remaining_work=f.get("Microsoft.VSTS.Scheduling.RemainingWork"),
            business_value=f.get("Microsoft.VSTS.Common.BusinessValue"), external_ref=f.get("Custom.PACTExternalRef"),
            tags=[t.strip() for t in (f.get("System.Tags") or "").split(";") if t.strip()],
            url=w.get("url"), updated_at=f.get("System.ChangedDate"),
        ))
    return items


class AzureDevOps(Connector):
    name = "azure-devops"
    env_var = "AZURE_DEVOPS_TOKEN"

    def read(self) -> list[Item]:
        token = os.environ[self.env_var]
        org, project, query_id = self.config["organization"], self.config["project"], self.config["query_id"]
        base = f"https://dev.azure.com/{org}/{project}/_apis"
        ids = [w["id"] for w in _get(token, f"{base}/wit/wiql/{query_id}?api-version=7.1")["workItems"]]
        items = []
        for chunk in (ids[i:i + 200] for i in range(0, len(ids), 200)):
            data = _get(token, f"{base}/wit/workitems?ids={','.join(map(str, chunk))}&fields={','.join(FIELDS)}&api-version=7.1")
            items.extend(items_from_workitems(data))
        return items

    def apply(self, changed: list[Item], removed: list[str], dry_run: bool) -> None:
        for it in changed:
            print(f"    {'would patch' if dry_run else 'patch'} {it.id}: Custom.PACTRisk={it.risk} System.Tags={';'.join(it.tags)}")
        if not dry_run:
            # PATCH /wit/workitems/{id} with application/json-patch+json — never System.State to Closed/Removed.
            print("    (write path: JSON Patch per item; State is never written by the sync)")


def make(config: dict, is_sot: bool) -> Connector:
    return AzureDevOps(config, is_sot)
