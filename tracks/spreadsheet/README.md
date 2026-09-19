# Track — Spreadsheet

A **hosted** spreadsheet — one that keeps version history and dated, attributable comments — as
the source of truth. The lowest possible entry: no project to create, no fields to configure
beyond columns with data validation, and the whole method visible on one screen. Good for a small
team's first weeks, for a pilot, or for an organisation whose only shared tool is a workbook.

| Capability | Status | Note |
|---|---|---|
| Source of truth | ✅ **hosted only** | Version history and comments are what make it eligible; a file on a disk is neither and cannot be the record — see `capabilities.yml` |
| Hierarchy | ❌ | A `Parent` column holding the parent's id; no tree view |
| Iterations | ❌ | A second sheet with dates and an `Iteration` column; no burndown |
| Code review | ❌ | The pull request lives in your code host; a `Reviewed · <name>` column per reviewer mirrors the verdict |
| CI | ❌ | Runs in the code host; the run URL goes in the receipt |
| Two state axes | ✅ | Two data-validated columns, `WI-State` and `Status` |
| Claims | custom | A `Claim` column plus a row comment |
| Digest | custom | Filter views, one per section of `RULE-DAILY-DIGEST`; nothing is posted for you |

**Read [`substitutes.md`](substitutes.md) before adopting.** Five capabilities are substituted;
the compatibility matrix marks the rules that depend on them. Everything here is enforced by
people and by the PR validator in the code host, not by the sheet.

## When to leave

The day you need a tree of Epics and Features, a board that people drag cards on, or a review
gate the tool enforces, move to Azure DevOps, GitHub Projects or Notion. The columns map one to
one onto their fields (`fields.md` ↔ each track's `fields.md`); the ids and the states travel as
they are.

## Files

[`mapping.yml`](mapping.yml) · [`capabilities.yml`](capabilities.yml) · [`fields.md`](fields.md) · [`setup.md`](setup.md) · [`substitutes.md`](substitutes.md)
