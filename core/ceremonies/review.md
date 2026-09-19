---
id: RULE-CEREMONY-REVIEW
canon: true
---

# Review

**PO's role: central.** This is the **Transfer** phase — human acceptance with evidence. The PO
validates the acceptance criteria, discusses the results with the stakeholders and updates the
backlog with what was learnt. The agent prepares the package; the human decides value.

| Do | Don't |
|---|---|
| Validate each acceptance criterion **against its evidence** — the receipt's per-AC table, and when `require_homologation_qa` is on the key-user test on `HOMOLOG_LINK` (`core/14-homologation.md`) | Accept on the strength of the summary alone, or from a chat update |
| Accept → the item may move to `Closed`. Reject → back to `In development` with **one objective note** (`RULE-STATE-REJECT`) | Reject with "not good enough" — that is a missing criterion, not a rejection |
| Read *Not verified / not claimed* before anything else | Assume that what the receipt does not mention was checked |
| Update the backlog with what was learnt: new items, spikes, gaps | Fold new scope into the item under review |
| Show value to stakeholders — the agent prepared the package, the PO presents it | Let an agent present to a stakeholder as if it were accountable |

## Who may move to `Closed`

Only the **Approver** (`RULE-ROLES`, `RULE-STATE-RESOLVED-NOT-CLOSED`). When the Approver is inside the
organisation it is usually the PO. When the Approver is an external customer, the acceptance is a
signed artifact (`RULE-OPT-CLIENT-SIGNOFF`).

## Output

- Every reviewed item is `Closed`, or back in `In development` with a rejection note on the item.
- Minutes: Part 1 of `templates/ceremonies/sprint-close-minutes.md`, or
  `templates/ceremonies/review-minutes.md` when held apart — the items, the outcome of each, and
  the evidence link that justified it.
- New backlog items from what was learnt, each through Refinement before it becomes `Ready`.

## Review is per item, not per iteration

Items reach `Resolved` continuously; the Approver's queue is drained continuously. The Review at
the sprint close (`RULE-CEREMONY-SPRINT-CLOSE`) is where the **iteration goal** is judged and
stakeholders see the whole — it is not a batch acceptance session. An Approver who accepts twenty
items in one hour at the sprint close is not reviewing; that queue should have been drained daily
(`RULE-DAILY-DIGEST`, item 4).

## Optional rules an instance may switch on

- `RULE-OPT-CLIENT-SIGNOFF` — acceptance must be a **signed artifact** from an external approver
  (instances with an external customer turn this on).
- `RULE-OPT-ITERATION-REPORT` — a written iteration report is produced at Review.
- `RULE-OPT-HOMOLOG-QA` — Review (Transfer) does not start until Check review has passed,
  QA has linked the homologation environment, and the key user has tested there. The
  key user is not this review; they produce the evidence this review reads.

Canon: RULE-CEREMONY-REVIEW · RULE-OPT-CLIENT-SIGNOFF · RULE-OPT-ITERATION-REPORT · RULE-OPT-HOMOLOG-QA
