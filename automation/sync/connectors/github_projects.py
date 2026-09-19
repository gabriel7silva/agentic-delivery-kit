"""GitHub Projects connector — reads issues + Project fields via GraphQL; as a
mirror, writes Project fields (never WI-State: Closed).

Reference code: enough to run, written to be adapted. Field names follow
tracks/github-projects/mapping.yml; override them in config if yours differ.
Owner may be an organization or a user login — the digest query asks both.
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
FIELD = {
    "wi_state": "WI-State", "status": "Status", "type": "Type", "priority": "Priority",
    "role": "Role", "risk": "Risk", "iteration": "Iteration", "homolog": "Homologation",
    "branch": "Branch", "change": "Change", "change_link": "Change link",
}


def _gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _field_map(node: dict) -> dict:
    out = {}
    for v in (node.get("fieldValues") or {}).get("nodes") or []:
        field = (v.get("field") or {}).get("name")
        if not field:
            continue
        value = v.get("number")
        if value is None:
            value = v.get("name") or v.get("title") or v.get("text")
        out[field] = value
    return out


def _linked_branch(content: dict) -> str | None:
    nodes = (content.get("linkedBranches") or {}).get("nodes") or []
    for n in nodes:
        name = ((n.get("ref") or {}).get("name") or "").strip()
        if name:
            return name
    return None


def _item_from_node(node: dict) -> Item | None:
    c = node.get("content") or {}
    if "number" not in c:
        return None
    fv = _field_map(node)
    labels = [l["name"] for l in (c.get("labels") or {}).get("nodes") or []]
    claim = next((l.split(":", 1)[1] for l in labels if l.startswith("claim:")), None)
    branch = fv.get(FIELD["branch"]) or _linked_branch(c)
    change = fv.get(FIELD["change"]) or fv.get(FIELD["change_link"])
    return Item(
        id=f"#{c['number']}", type=(fv.get(FIELD["type"]) or "STORY").upper(), title=c["title"],
        wi_state=STATE_FROM.get(fv.get(FIELD["wi_state"]), "NEW"),
        status=STATUS_FROM.get(fv.get(FIELD["status"])),
        iteration=fv.get(FIELD["iteration"]), priority=fv.get(FIELD["priority"]),
        role=fv.get(FIELD["role"]), risk=fv.get(FIELD["risk"]),
        claim=claim, tags=[l for l in labels if not l.startswith(("claim:", "type:"))],
        branch=branch or None, change_link=change or None,
        homolog_link=fv.get(FIELD["homolog"]),
        effort=fv.get("Effort"), remaining_work=fv.get("Remaining work"),
        business_value=fv.get("Business value"), external_ref=fv.get("External ref"),
        url=c.get("url"), updated_at=node.get("updatedAt"),
    )


def project_from_payload(data: dict) -> dict | None:
    root = data.get("data") or {}
    for key in ("organization", "user"):
        block = root.get(key) or {}
        proj = block.get("projectV2")
        if proj:
            return proj
    return None


def items_from_payload(data: dict) -> list[Item]:
    proj = project_from_payload(data)
    if not proj:
        return []
    items = []
    for node in (proj.get("items") or {}).get("nodes") or []:
        it = _item_from_node(node)
        if it:
            items.append(it)
    return items


class GitHubProjects(Connector):
    name = "github-projects"
    env_var = "GITHUB_TOKEN"

    def read(self) -> list[Item]:
        token = os.environ[self.env_var]
        owner, number = self.config["owner"], int(self.config["project_number"])
        items, after = [], None
        while True:
            data = _gql(token, QUERY, {"login": owner, "number": number, "after": after})
            proj = project_from_payload(data)
            if not proj:
                raise RuntimeError(f"no ProjectV2 for owner {owner!r} (organization or user)")
            for node in proj["items"]["nodes"]:
                it = _item_from_node(node)
                if it:
                    items.append(it)
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
