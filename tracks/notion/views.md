# Notion — views

On the **Work items** database. Views are cheap; the point is that each one answers exactly one
question the method asks.

| View | Layout | Group / filter / sort | Answers |
|---|---|---|---|
| **Board** | Board | group by `Status` | Where is everything on the board |
| **WI-State** | Board | group by `WI-State` | The honest picture — how much sits in Resolved-category states waiting on a person |
| **Hierarchy** | Table | show sub-items nested, filter `Type` in (Epic, Feature, Story) | Tree |
| **Gate queue** | Table | filter `WI-State` is any Resolved-category state (Awaiting test, Prepare homologation, Key-user homologation, Prepare release, Integration test) **or** `Tags` contains needs-human, filter `WI-State` ≠ Closed, sort Last edited ↑ | The human queue, oldest first |
| **Iteration** | Timeline | by `Iteration` relation dates | Roadmap |
| **Epic roadmap** | Timeline | by `Target`, grouped by parent item, filter `Type` in (Epic, Feature) | Where each initiative lands |
| **Unreviewed** | Table | filter `WI-State` is any Resolved-category state **and** any `Reviewed · …` unchecked | The review-gate substitute's watchdog |
| **Inconsistent** | Table | filter `Status` = Done **and** `WI-State` ≠ Closed | A card reached Done without a human — a defect, not a state |
| **Untraced** | Table | filter `WI-State` is not New, In analysis, Awaiting development, Closed or Removed, and (`Target` is empty **or** `Branch` is empty **or** `Branch` is `main`) | Work started without the change or the dates on the properties |

## The Daily digest page

One page with four **linked views** of the same database, in the order `RULE-DAILY-DIGEST` sets:
Active · Blockers (`Type` = Issue, `WI-State` ≠ Closed) · Needs human · Ready for review. The PO
opens one page every morning; nothing is written by hand.
