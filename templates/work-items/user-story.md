### <STORY-ID> <short, clear title>

- **Work item type:** Story (PBI)
- **Parent (Feature):** <FEATURE-ID>
- **Epic:** <EPIC-ID>
- **WI-State:** New
- **Target role / skill:** {{roles.implementer.title}}
- **Iteration:**
- **Tags:** <needs-human · spike · gap · …>
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

#### Description

As <persona>, I want <goal>, so that <benefit>.

**Context for the agent:** <what it needs to know about the domain to not invent it>

**Out of scope / forbidden:** <what the agent must not do — mandatory, never empty>

**Suggested steps (optional):**
1.
2.

#### Acceptance criteria

Each one pass/fail. Each one names the evidence that satisfies it.

- [ ] AC1 — Given <context>, when <action>, then <observable result>. Evidence: <what proves it>
- [ ] AC2 — … Evidence: …
<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

#### Scenarios (Given / When / Then)

One block per criterion that needs more than a line. Each scenario is testable by an agent and
by a person; "works correctly" is not a scenario.

**Scenario 1 — <name>** (AC1)
- Given <context>
- When <action>
- Then <observable result>

#### Business rules to validate

- <a rule this story depends on that nobody has written down> → <who confirms it>

#### Handoff to the orchestrator

- **Required inputs:** <files, credentials the agent already has, data>
- **Expected outputs:** <the artifact, the change, the receipt>
- **Escalate to the PO when:** <item-specific triggers, on top of RULE-HITL>

#### Notes / dependencies

Canon: RULE-DOR · RULE-ITEM-MODEL

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
