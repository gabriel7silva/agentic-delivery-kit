# Walkthrough — one item, intake to Closed

**Fictitious.** Acme Corp, internal team, GitHub Projects. Story `WI-42`: *add an "Export CSV"
button to the customer list screen*. Deliberately banal so the artifacts, not the domain, are what
you read.

| Step | Phase | Artifact | Who writes it |
|---|---|---|---|
| [00](00-intake.md) | — | Intake note | whoever received the request |
| [01](01-refined-story.md) | Plan | Refined Story with executable acceptance criteria | Product Owner, at Refinement |
| [02](02-handoff.md) | Plan → Act | Handoff | Orchestrator |
| [03](03-pr-body.md) | Act → Check | PR body with the `pact-context` block | Implementer |
| [04](04-receipt.md) | Check | Receipt, with *Not verified* | Implementer |
| [05](05-conclusion-comment.md) | Check | Conclusion comment on the item | Implementer |
| [06](06-closed.md) | Transfer | Acceptance and the state change | Product Owner (Approver) |

## The gate runs on this

`make check` (`test_walkthrough.py`) feeds steps 03–05 to `validate_pr.py` with the changed
paths the diff would have touched. It passes. Change the receipt to drop *Not verified* and it
fails — try it.

## What to notice

- The intake note (00) has **no acceptance criteria**. They appear in 01, written by a person who
  could ask the requester. That gap is where invention would otherwise happen.
- The handoff (02) has a **forbidden** section that is not empty.
- The receipt (04) claims two things and **declines to claim** two others. The Approver signs
  having read both lists.
- Step 06 is the only one a human writes as a state change. Nothing before it moved the item
  past the `Resolved` category.
- The instance runs nine of the model's twelve states (`instance-internal-github.yml` →
  `lifecycle`): no homologation stage, no integration test. Categories are all there; the gate
  never noticed the difference.
