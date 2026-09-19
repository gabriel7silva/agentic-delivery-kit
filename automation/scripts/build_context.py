#!/usr/bin/env python3
"""Build context.json from a board snapshot, falling back to a declared PR context.

    build_context.py --declared declared.json --out context.json
    build_context.py --snapshot board.json --declared declared.json --item WI-42 --out context.json
    build_context.py --pr-body pr-body.md --snapshot board.json --out context.json

The snapshot is a JSON list of Item records (sync_core.Item as dict). Board fields
win: wi_state, risk, type, claim, branch, homolog_link. Verdicts, actor, target
state and verification stay on the declaration — the board does not hold them.

When the snapshot is missing or does not contain the item, the declared context
is written as-is with source=declared. That is the adoption fallback, not a pass
on the board.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CONTEXT_BLOCK = re.compile(r"```pact-context\s*\n(.*?)\n```", re.S)


def _load(path: Path | None) -> dict | list | None:
    if path is None or not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def declared_from_body(body: str) -> dict | None:
    m = CONTEXT_BLOCK.search(body or "")
    if not m:
        return None
    return json.loads(m.group(1))


def find_item(snapshot: list, item_id: str) -> dict | None:
    want = (item_id or "").strip()
    if not want:
        return None
    for rec in snapshot:
        if str(rec.get("id") or "") == want:
            return rec
    return None


def merge(declared: dict, board: dict | None) -> dict:
    ctx = json.loads(json.dumps(declared or {}))
    if not board:
        ctx["source"] = "declared"
        return ctx
    item = dict(ctx.get("item") or {})
    item["id"] = board.get("id") or item.get("id")
    if board.get("type"):
        item["type"] = board["type"]
    if board.get("wi_state"):
        item["wi_state"] = board["wi_state"]
    if board.get("risk"):
        item["risk"] = board["risk"]
    ctx["item"] = item
    claims = dict(ctx.get("claims") or {})
    if board.get("claim"):
        claims["this_item"] = [board["claim"]]
    claims.setdefault("open_elsewhere", {})
    ctx["claims"] = claims
    homolog = dict(ctx.get("homologation") or {})
    if board.get("branch"):
        homolog["branch"] = board["branch"]
    if board.get("homolog_link"):
        homolog["environment_url"] = board["homolog_link"]
    ctx["homologation"] = homolog
    if board.get("change_link"):
        ctx["change_link"] = board["change_link"]
    ctx["source"] = "sot"
    return ctx


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", type=Path, help="JSON list of board items")
    ap.add_argument("--declared", type=Path, help="declared context.json (PR author)")
    ap.add_argument("--pr-body", type=Path, help="PR body with a pact-context fence")
    ap.add_argument("--item", help="item id; default: declared.item.id")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    declared: dict = {}
    if args.declared:
        loaded = _load(args.declared)
        if not isinstance(loaded, dict):
            print("declared context is not a JSON object", file=sys.stderr)
            return 2
        declared = loaded
    elif args.pr_body and args.pr_body.is_file():
        parsed = declared_from_body(args.pr_body.read_text(encoding="utf-8"))
        if parsed is None:
            print("no ```pact-context block in the PR body", file=sys.stderr)
            return 2
        declared = parsed

    item_id = args.item or str((declared.get("item") or {}).get("id") or "")
    snapshot = _load(args.snapshot)
    board = None
    if isinstance(snapshot, list):
        board = find_item(snapshot, item_id)

    ctx = merge(declared, board)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(ctx, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out} source={ctx.get('source')} item={item_id or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
