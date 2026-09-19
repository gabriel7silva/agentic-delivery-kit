# Key-user test for Review — <ITEM-ID> <short title>

The key user **tests** on the homologation environment QA linked, then writes this **on the
item**. This is what **Review (Transfer)** reads. A chat message to the PO is not this
update and does not skip Review.

Canon: RULE-KEY-USER-UPDATE · RULE-GOLDEN-TRACE

## Environment (stop and send back to QA if any line fails)

| Field | Value |
|---|---|
| `BRANCH` on the board | <the feature branch QA wrote — never the default branch> |
| `HOMOLOG_LINK` opened | <the same URL QA wrote> |
| Environment is that branch | yes · **no → stop** |

## Test

| Field | Value |
|---|---|
| Responsible | {{roles.key_user.title}} |
| Date | |
| What I tested, on that environment | |
| Verdict | pass · pass-with-findings · block |
| Evidence | <screenshot, log, or URL — not a sentence> |

## For Review (Transfer)

| Field | Value |
|---|---|
| What Review should open | the same `HOMOLOG_LINK` |
| What Review needs to know | |
| Verdict for Review | accept · reject · need-a-look |
| Next step | `review` |

## Not verified / not claimed

- <what I did not exercise on this environment>

<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
