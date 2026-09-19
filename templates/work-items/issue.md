### Issue: <what is blocked, in one line>

- **Work item type:** Issue (impediment)
- **Blocks:** <ITEM-ID>, …
- **WI-State:** New
- **Raised by (role):** <orchestrator · implementer · reviewer-…>
- **Kind:** <tool · auth · dependency · ambiguity · scope-conflict>
- **Needs a human:** yes (<trigger from RULE-HITL>) · no

An Issue is a **blocker**, not a defect. It exists so the blocked item can stay honest in its state
while someone with the authority to unblock it is found.

#### What is blocked and why

<one paragraph; a log or a screenshot if it is a tool failure>

#### What would unblock it

- <a decision → role> · <an access → role> · <a retry after X>
<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

#### Resolution

Filled when a **human** sets `Closed`. The orchestrator records what unblocked it and may take
the item to `Resolved`; it does not set `Closed` (`RULE-STATE-RESOLVED-NOT-CLOSED`).

Canon: RULE-ITEM-MODEL · RULE-HITL

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
