### Bug: <what is wrong, in one line>

- **Work item type:** Bug
- **Related to:** <STORY-ID or FEATURE-ID, if any>
- **WI-State:** New
- **Role / skill:** {{roles.implementer.title}}
- **Severity:** <blocking · major · minor>
- **Tags:**
- **External ref:** <[<ref>] — when the item answers a request in another system; also in the title>

<!-- canon:begin fragment=trace-fields -->
| Trace field | Value | When |
|---|---|---|
| Branch | <feature branch — never `main`> | Act — write the **board field**, not only this cell |
| Change / pull request | <URL> | When the PR exists |
| Homologation | <URL of the running env for this branch> | QA starts it; the key user tests there |
| Start date | <YYYY-MM-DD> | The day WI-State becomes Active |
| Target date | <YYYY-MM-DD> | Planning — required before Ready |
<!-- canon:end -->

A Bug is a **proven defect**. A gap in the product is a Story tagged `gap`, not a Bug
(`AP-BUG-FOR-GAPS`).

#### Reproduction

1. Given <state>
2. When <action>
3. Then <what happens> — expected: <what should happen>

**Evidence of the defect:** <log, screenshot, failing test — attached>

#### Acceptance criteria

- [ ] AC1 — The reproduction above no longer produces the defect. Evidence: <the same steps, passing>
- [ ] AC2 — A regression test exists and fails on the previous version. Evidence: <test name and run>
<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

#### Forbidden

- Do not fix adjacent problems in the same change — file them.
- <item-specific limits>

Canon: RULE-ITEM-MODEL · RULE-DOR

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
