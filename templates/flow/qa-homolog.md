# QA homologation ready — <ITEM-ID> <short title>

Posted **on the item** when the homologation environment for this branch is up and linked.
This is the handoff to the key user, who **tests**. QA does not test the product. Next step
is `key-user`. Never `closed`.

Canon: RULE-HOMOLOG-QA · RULE-HOMOLOG-READY · RULE-GOLDEN-TRACE

## Ready for the key user (all four, or do not hand over)

| Field | Value |
|---|---|
| Feature branch (`BRANCH` on the board) | <name — never the default branch> |
| Environment started for **that** branch | yes · **no → do not hand over** |
| Homologation URL (`HOMOLOG_LINK` on the board) | <URL> |
| Environment matches `BRANCH` | yes · **no → stop, restart, rewrite the URL** |

## Handoff

| Field | Value |
|---|---|
| Responsible | {{roles.qa.title}} |
| Date | |
| What the key user should open | the `HOMOLOG_LINK` above — that URL, this branch |
| Next step | `key-user` |

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
