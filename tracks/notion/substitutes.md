# Notion — substitutes

For each capability the tool lacks: what we do instead, the evidence it produces, and what is lost.
These are declarations the compatibility matrix reads; they are **not** a claim that the capability
exists.

## `code_review` — no change-request object

Affects: `RULE-REVIEW-GATE`, `RULE-REVIEW-RISK`, `RULE-RISK-GATES`, `RULE-MERGE`, `RULE-MERGE-COMMON`.

| | |
|---|---|
| **Mechanism** | The pull request exists in your **code host**; its URL goes in `Change link`. Each required reviewer posts the verdict block (`core/model/review-gates.yml` → `verdict_shape`) as a **page comment** and ticks their `Reviewed · <name>` checkbox. `Risk` is set to `MAX(verdicts, floor)` by whoever ticks the last box |
| **Evidence** | The verdict comments. The checkbox is a summary; a ticked box with no comment is not a review |
| **Loses** | Enforcement. Nothing prevents `WI-State: Resolved` with an unticked box or a missing comment. The **Unreviewed** view surfaces it; a person has to act. If your code host has branch protection, put the *real* gate there and treat Notion's checkboxes as the mirror |

## `ci` — no verification runner

Affects: `RULE-REVIEW-GATE` (the `VERIFICATION` gate).

| | |
|---|---|
| **Mechanism** | Verification runs in the code host's CI, or locally. The run's URL or its output goes in the receipt's *Commands run* section and is linked from the page |
| **Evidence** | The linked run, with exit status visible |
| **Loses** | Nothing, if the code host runs CI. Everything, if verification is "I ran it on my machine" with no attached output — that is `AP-CLAIMED-SMOKE` |

## `iteration_native` — no dated sprint entity

Affects: `RULE-CEREMONIES`, `RULE-CEREMONY-PLANNING`, `RULE-ITERATION-NAMING`, `RULE-CEREMONY-SPRINT-CLOSE`, `RULE-CARRY-OVER`.

| | |
|---|---|
| **Mechanism** | The `Iterations` database with `Start` and `End`; a relation from every item |
| **Evidence** | The relation and the Timeline view |
| **Loses** | Built-in burndown. A rollup of `WI-State = Closed` per iteration gives a count; a chart needs an export |

## What stays unsubstituted

Nothing. Every symbol in `mapping.yml` is `native`, `custom` or `unsupported`-with-substitute. If
you find one that is not, `make mapping` will find it too.
