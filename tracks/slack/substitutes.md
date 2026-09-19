# Slack — substitutes

Slack lacks most capabilities the method needs, and that is fine **because it is a mirror**. Each
substitute below says the same thing in a different way: *the real thing lives in the source of
truth; Slack shows it to people.*

## `sot_eligible` and `durable_history`

Affects: every rule that requires `durable_history` — `RULE-GOLDEN-TRACE`, `RULE-CLAIM`.

| | |
|---|---|
| **Mechanism** | An SoT-eligible track holds state; the sync mirrors it into a List and posts events |
| **Evidence** | Always on the SoT item |
| **Loses** | Nothing, as long as nobody treats the thread as the record. The `DECISION:` copy step in `channels.md` is what makes this hold |

## `code_review` and `ci`

Affects: `RULE-REVIEW-GATE`, `RULE-REVIEW-RISK`, `RULE-RISK-GATES`, `RULE-MERGE`, `RULE-MERGE-COMMON`.

| | |
|---|---|
| **Mechanism** | The code host runs both. Slack receives the *request* for review as a thread and the *result* as an event |
| **Evidence** | On the change request in the code host |
| **Loses** | Nothing. A reaction on the thread is not a review — `channels.md` |

## `native_hierarchy` and `iteration_native`

Affects: `RULE-ITEM-MODEL`, `RULE-CEREMONIES`, `RULE-CEREMONY-PLANNING`, `RULE-ITERATION-NAMING`, `RULE-CEREMONY-SPRINT-CLOSE`, `RULE-CARRY-OVER`.

| | |
|---|---|
| **Mechanism** | Text fields mirroring the parent id and the iteration name; the tree and the dates are in the SoT |
| **Evidence** | The SoT |
| **Loses** | Tree views and timelines in Slack. Open the SoT for those |

## The one thing Slack does natively

`DIGEST`. A scheduled message is a better daily sync than any meeting, and it is the reason this
track exists. Everything else here is plumbing to make that message accurate.
