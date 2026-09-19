# Acceptance sign-off — <ITEM-ID> <title>

The Transfer evidence for an item delivered to an external customer. Attached to the item; the
item moves to `Closed` when this is signed, not before, not on a verbal yes.

Canon: RULE-OPT-CLIENT-SIGNOFF · RULE-STATE-RESOLVED-NOT-CLOSED · RULE-CEREMONY-REVIEW

## What is being accepted

| Field | Value |
|---|---|
| Item | <ITEM-ID> — <title> |
| Iteration | |
| Delivered as | <link to the change, build or environment the customer reviewed> |
| Receipt | <link> |

## Acceptance criteria, as the customer saw them

| AC | Result | Evidence the customer reviewed |
|---|---|---|
| AC1 | accepted · rejected | |
| AC2 | accepted · rejected | |

## Not verified / not claimed — carried from the receipt

The customer signs having read this list. It is the honest boundary of what is being accepted.

- <carried verbatim from the receipt>

## Decision

- [ ] **Accepted.** The item may move to `Closed`.
- [ ] **Rejected** — criterion <AC-n>: <what would satisfy it>. The item returns to `Active`.

## Signature

| | |
|---|---|
| Signed by (role) | {{roles.approver.title}} |
| Date | |
| Signature or written approval reference | <e-mail reference, e-signature id, or a dated comment on the item> |

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
