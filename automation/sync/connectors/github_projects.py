"""GitHub Projects connector — reads issues + Project fields via GraphQL; as a
mirror, writes Project fields (never WI-State: Closed).

Reference code: enough to run, written to be adapted. Field names follow
tracks/github-projects/mapping.yml; override them in config if yours differ.
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
from sync_core import Connector, Item, category_of  # noqa: E402

API = "https://api.github.com/graphql"
QUERY = (Path(__file__).resolve().parents[3] / "tracks" / "github-projects" / "queries" / "digest.graphql").read_text(encoding="utf-8")
FIELD = {"wi_state": "WI-State", "status": "Status", "type": "Type", "priority": "Priority", "role": "Role", "risk": "Risk", "iteration": "Iteration", "homolog": "Homologation"}


def _gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


class GitHubProjects(Connector):
    name = "github-projects"
    env_var = "GITHUB_TOKEN"

    def read(self) -> list[Item]:
        token = os.environ[self.env_var]
        owner, number = self.config["owner"], int(self.config["project_number"])
        items, after = [], None
        while True:
            data = _gql(token, QUERY, {"org": owner, "number": number, "after": after})
            proj = data["data"]["organization"]["projectV2"]  # user-level: swap organization→user in the query
            for node in proj["items"]["nodes"]:
                c = node.get("content") or {}
                if "number" not in c:
                    continue
                fv = {v["field"]["name"]: (v.get("number") if v.get("number") is not None else v.get("name") or v.get("title") or v.get("text"))
                      for v in node["fieldValues"]["nodes"] if v.get("field")}
                labels = [l["name"] for l in c.get("labels", {}).get("nodes", [])]
                claim = next((l.split(":", 1)[1] for l in labels if l.startswith("claim:")), None)
                items.append(Item(
                    id=f"#{c['number']}", type=(fv.get("Type") or "STORY").upper(), title=c["title"],
                    wi_state=STATE_FROM.get(fv.get("WI-State"), "NEW"), status=STATUS_FROM.get(fv.get("Status")),
                    iteration=fv.get("Iteration"), priority=fv.get("Priority"), role=fv.get("Role"), risk=fv.get("Risk"),
                    claim=claim, tags=[l for l in labels if not l.startswith(("claim:", "type:"))],
                    homolog_link=fv.get("Homologation"),
                    effort=fv.get("Effort"), remaining_work=fv.get("Remaining work"), business_value=fv.get("Business value"),
                    external_ref=fv.get("External ref"),
                    url=c["url"], updated_at=node.get("updatedAt"),
                ))
            pi = proj["items"]["pageInfo"]
            if not pi["hasNextPage"]:
                break
            after = pi["endCursor"]
        return items

    def apply(self, changed: list[Item], removed: list[str], dry_run: bool) -> None:
        # Mirror mode: update Project single-select fields. Requires the field and option ids,
        # which are project-specific — resolve them once with a ProjectV2 fields query and cache.
        for it in changed:
            if category_of(it.wi_state) in ("CLOSED", "REMOVED") and not self.is_sot:
                pass  # mirrors DISPLAY closed items; they never originate the transition
            print(f"    {'would set' if dry_run else 'set'} {it.id}: WI-State={it.wi_state} Status={it.status}")
        if not dry_run:
            # updateProjectV2ItemFieldValue mutation per item — left as the adopter's wiring,
            # since it needs your project's field/option ids.
            print("    (write path: implement updateProjectV2ItemFieldValue with your field ids)")


def make(config: dict, is_sot: bool) -> Connector:
    return GitHubProjects(config, is_sot)
