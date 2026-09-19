# Notion — fields (database schema)

One database, **Work items**, with these properties. A second, **Iterations**, with `Name`,
`Start`, `End`, `Goal`. A third, **Minutes**, with `Ceremony`, `Date`, `Iteration`.

| Method field | Property | Type | Native? | Note |
|---|---|---|---|---|
| `ITEM_ID` | `ID` | ID (auto) | ✅ | prefix e.g. `WI-` |
| `ITEM_TYPE` | `Type` | Select | custom | Epic · Feature · Story · Task · Bug · Issue |
| `WI_STATE` | `WI-State` | **Select** | custom | *not* a Status property — see below |
| `STATUS` | `Status` | Status | ✅ | drives the board view |
| `PARENT` | `Parent item` | Relation (self) | custom | created by enabling Sub-items |
| `ITERATION` | `Iteration` | Relation → Iterations | custom | |
| `PRIORITY` | `Priority` | Select | custom | P1–P4 |
| `ROLE` | `Role` | Select | custom | your role ids |
| `RISK` | `Risk` | Select | custom | low · medium · high |
| `CLAIM` | `Claim` | Text | custom | plus a comment for history |
| `BRANCH` | `Branch` | Text | custom | feature branch of this item — never `main` |
| `CHANGE_LINK` | `Change link` | URL | custom | the PR in your code host |
| `START_DATE` | `Start` | Date | custom | the day WI-State becomes In development |
| `TARGET_DATE` | `Target` | Date | custom | set in Planning, required before Ready |
| `HOMOLOG_LINK` | `Homologation` | URL | custom | QA writes it after starting the env for this branch; the key user tests there |
| `TAGS` | `Tags` | Multi-select | custom | keep `needs-human` |
| `RETRO` | `Retro` | Text | custom, optional | |
| `EFFORT` | `Effort` | Number | custom, optional | when `track_sprint_metrics` is on |
| `REMAINING_WORK` | `Remaining` | Number | custom, optional | on Task pages |
| `BUSINESS_VALUE` | `Business value` | Number | custom, optional | on Epic / Feature pages |
| `EXTERNAL_REF` | `External ref` | Text | custom, optional | the title starts with `[<ref>]` when `require_external_ref` is on |
| — review gate | `Reviewed · <reviewer>` | Checkbox ×N | substitute | one per required reviewer — see `substitutes.md` |

## Why `WI-State` is a Select and not a Status

Notion's **Status** property type forces every option into one of three groups: *To-do*,
*In progress*, *Complete*. `Resolved` and `Closed` would both have to sit in *Complete*, and any
view grouped by Status would show them as the same thing — which is precisely the confusion
`RULE-STATE-RESOLVED-NOT-CLOSED` exists to prevent. A plain **Select** has no groups and keeps the
twelve states distinct. Use the Status property for the *board column* only, where the three
groups are harmless.

## Branch and dates stay empty unless you write the properties

Notion does not invent a feature branch or a target date when you create a page. The four
properties above are the method fields. Fill them on the property row, not only in the page
body:

- `Target` — Planning, before Ready. An empty Target on an item in the iteration is unfinished
  Planning.
- `Start` — the day `WI-State` becomes `Active`.
- `Branch` — the feature branch. `main` (or your default branch) is wrong: that is the
  integration branch, not this item's change.
- `Change link` — the pull-request URL, the moment it exists.

A page in an `Active`- or `Resolved`-category state with `Target` empty or `Branch` equal to the
default branch belongs in the **Untraced** view.
