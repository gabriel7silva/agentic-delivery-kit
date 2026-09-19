# Spreadsheet — fields (columns)

One workbook. Sheet **Work items**: one row per item, the columns below, data validation on every
select-like column, the header row frozen. Sheet **Iterations**: `Name`, `Start`, `End`, `Goal`,
`Capacity`, `Minutes` (a link). Sheet **Comments**: `Item`, `Date`, `Role`, `Responsible`,
`What was done`, `Link`, `Evidence`, `Next step` — one row per conclusion or evidence comment.

| Method field | Column | Validation | Native? | Note |
|---|---|---|---|---|
| `ITEM_ID` | `ID` | — | custom | typed, unique, never reused (e.g. `WI-42`) |
| `ITEM_TYPE` | `Type` | list: Epic · Feature · Story · Task · Bug · Issue | custom | |
| `WI_STATE` | `WI-State` | list: the twelve states, or the instance's subset | custom | conditional formatting per category |
| `STATUS` | `Status` | list: the eleven columns | custom | one filter view per value is the board |
| `PARENT` | `Parent` | — | custom | the parent's `ID`; no tree |
| `ITERATION` | `Iteration` | list from the Iterations sheet | custom | dates live on that sheet |
| `PRIORITY` | `Priority` | list: P1–P4 | custom | |
| `ROLE` | `Role` | list: your role ids | custom | |
| `RISK` | `Risk` | list: low · medium · high | custom | set at the review gate |
| `CLAIM` | `Claim` | — | custom | plus a row comment for history |
| `BRANCH` | `Branch` | — | custom | never the default branch |
| `CHANGE_LINK` | `Change` | — | custom | the pull request URL |
| `HOMOLOG_LINK` | `Homologation` | — | custom | QA writes it; the key user tests there |
| `START_DATE` | `Start` | date | custom | the day the item enters In development |
| `TARGET_DATE` | `Target` | date | custom | Planning, before Ready |
| `TAGS` | `Tags` | — | custom | comma-separated; keep `needs-human` |
| `RETRO` | `Retro` | — | custom, optional | |
| `EFFORT` | `Effort` | number | custom, optional | when `track_sprint_metrics` is on |
| `REMAINING_WORK` | `Remaining` | number | custom, optional | on Task rows |
| `BUSINESS_VALUE` | `Business value` | number | custom, optional | on Epic / Feature rows |
| `EXTERNAL_REF` | `External ref` | — | custom, optional | the title starts with `[<ref>]` when `require_external_ref` is on |
| — review gate | `Reviewed · <reviewer>` | checkbox ×N | substitute | one per required reviewer — see `substitutes.md` |
| — | `Title` | — | — | the item's title; `[<ref>]` first when the rule is on |
| — | `Updated` | date-time | — | last edit, for the digest's ordering |

## Nothing is native, and that is the point

Every method field is a column you create in five minutes. The cost is on the other side: nothing
in a spreadsheet stops a person from typing `Closed`, from skipping a claim, or from sorting the
sheet and losing a row. Those are the people-enforced rules `substitutes.md` lists, and the reason
this track is for a first week, not a third year.
