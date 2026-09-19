### Task: <verb + object>

- **Parent (Story):** <STORY-ID>
- **WI-State:** New
- **Role / skill:** {{roles.implementer.title}}
- **Scope(s) to claim:** `<scope-id>`
- **Objective (one or two sentences):**
- **Steps:**
  1.
  2.
- **Done when:** <observable condition, with its evidence>
- **Forbidden:** <what this Task must not do — mandatory>
- **Report:** file paths, ids, errors, uncertainties — as a conclusion comment on this item

<!-- canon:begin fragment=trace-fields -->
| Trace field | Value | When |
|---|---|---|
| Branch | <feature branch — never `main`> | Act — write the **board field**, not only this cell |
| Change / pull request | <URL> | When the PR exists |
| Homologation | <URL of the running env for this branch> | QA starts it; the key user tests there |
| Start date | <YYYY-MM-DD> | The day WI-State becomes Active |
| Target date | <YYYY-MM-DD> | Planning — required before Ready |
<!-- canon:end -->

Canon: RULE-ITEM-MODEL · RULE-CONCLUSION-COMMENT

<!-- canon:begin fragment=traceability-table -->
| Field | Value |
|---|---|
| Product Owner (role) | {{roles.product_owner.title}} |
| Executor (role) | |
| Branch | <feature branch — never `main`> |
| Change / pull request | <URL> |
| Homologation | <URL — QA starts; key user tests> |
| Evidence | |
| Start date | |
| Target date | |
| Closed date | |
<!-- canon:end -->

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
