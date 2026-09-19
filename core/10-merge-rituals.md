---
id: RULE-MERGE
canon: true
---

# Merge rituals by change type

Not every change deserves the same gate. Treating a typo fix like a schema migration burns reviewer
time; treating a schema migration like a typo fix burns the product. Three change types, three sets
of conditions.

| Change type | Examples | May merge when |
|---|---|---|
| **Code** | Anything under a scope with floor `medium` or `high`; anything a Story's criteria name | Review gate passed (`RULE-REVIEW-GATE`) · conclusion comment posted · all ACs evidenced or explicitly out of scope |
| **Docs / process** | Documentation, templates, runbooks, this method's own files | Change is opened for review · summary on the change · **no code-review gate required** — a human may merge on sight |
| **Value items** | Anything whose item carries `needs-human` or reaches risk `high` | Only the Approver moves it to `Closed`. Agents stop at `Resolved` |

## What is the same for all three — `RULE-MERGE-COMMON`

- The change is **linked from the work item** and the item is linked from the change.
- The working tree is clean: nothing is committed that is not in the diff, nothing is left out that
  the diff needs.
- No evidence is invented (`RULE-GOLDEN-NO-INVENTION`). A green check that was not actually run
  is a false claim, not a nit.

## Who merges

The role that merges is an instance decision. The method only constrains **when**. Two patterns
that work:

- **Human merges everything.** Simplest. Fine while volume is low.
- **Agent merges `low`, human merges the rest.** The validator gates the agent's merge; the human
  gates by reading the receipt.

An agent that merges its **own** change without a gate is anti-pattern `AP-SELF-MERGE`, regardless
of risk level.

## After the merge

- The item does not become `Closed` by merging. It becomes `Resolved` (`RULE-STATE-RESOLVED-NOT-CLOSED`).
- The claim on the scope is released (`RULE-CLAIM`).
- The receipt records the merge reference as **Link** in its conclusion comment.

## Optional rule an instance may switch on

- `RULE-OPT-CHANGELOG` — every `Closed` Story or Bug has a changelog line, added in the same change.

Canon: RULE-MERGE · RULE-MERGE-COMMON · RULE-OPT-CHANGELOG
