# Spreadsheet — substitutes

For each capability the tool lacks: what we do instead, the evidence it produces, and what is lost.
These are declarations the compatibility matrix reads; they are **not** a claim that the capability
exists. This track has more of them than any other, which is the honest price of zero setup.

## `native_hierarchy` — no tree

Affects: `RULE-ITEM-MODEL`.

| | |
|---|---|
| **Mechanism** | A `Parent` column holding the parent's `ID` |
| **Evidence** | The column, filterable by parent |
| **Loses** | Tree views, roll-ups, drag-and-drop re-parenting. A filter view per Feature is the nearest thing |

## `attachments` — links only

Affects: `RULE-DOR`, `RULE-DOD`, `RULE-EVIDENCE`, `RULE-CEREMONY-REVIEW`, `RULE-OPT-CLIENT-SIGNOFF`.

| | |
|---|---|
| **Mechanism** | Evidence lives in the code host, a document store or a shared drive; the `Evidence` column holds one URL per criterion |
| **Evidence** | The linked file, with its own history |
| **Loses** | Nothing, as long as the link is durable. A file pasted into a chat is not evidence (`core/07-evidence.md`) |

## `code_review` — no change-request object

Affects: `RULE-REVIEW-GATE`, `RULE-REVIEW-RISK`, `RULE-RISK-GATES`, `RULE-MERGE`, `RULE-MERGE-COMMON`.

| | |
|---|---|
| **Mechanism** | The pull request in your **code host**; its URL in `Change`. Each required reviewer posts the verdict block there and ticks their `Reviewed · <name>` checkbox on the row. `Risk` is set to `MAX(verdicts, floor)` by whoever ticks the last box |
| **Evidence** | The verdict comments on the pull request; the checkbox is a summary |
| **Loses** | Enforcement in the sheet. The PR validator in the code host enforces; the **Unreviewed** view surfaces what people missed |

## `ci` — no verification runner

Affects: `RULE-REVIEW-GATE` (the `VERIFICATION` gate).

| | |
|---|---|
| **Mechanism** | Verification runs in the code host's CI; the run's URL goes in the receipt's *Commands run* and in `Evidence` |
| **Evidence** | The linked run, with exit status visible |
| **Loses** | Nothing, if the code host runs CI. Everything, if verification is "I ran it on my machine" with no attached output — `AP-CLAIMED-SMOKE` |

## `iteration_native` — no dated sprint entity

Affects: `RULE-CEREMONIES`, `RULE-CEREMONY-PLANNING`, `RULE-ITERATION-NAMING`, `RULE-CEREMONY-SPRINT-CLOSE`, `RULE-CARRY-OVER`, `RULE-OPT-SPRINT-METRICS`.

| | |
|---|---|
| **Mechanism** | The `Iterations` sheet with `Start`, `End`, `Goal`, `Capacity`; the `Iteration` column validated against it |
| **Evidence** | The two sheets |
| **Loses** | Burndown and velocity charts. `SUMIF` on `Remaining` per iteration is a number, not a chart |

## What stays unsubstituted

Nothing. Every symbol in `mapping.yml` is `custom` or `unsupported`-with-substitute; the sheet
has no native symbol at all. If you find one that is not covered, `make mapping` will find it too.
