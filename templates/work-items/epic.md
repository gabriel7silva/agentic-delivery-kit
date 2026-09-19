### <EPIC-ID> <title>

- **Work item type:** Epic
- **WI-State:** New
- **Owner (role):** {{roles.product_owner.title}}
- **Horizon:** <months>
- **Tags:**
- **External ref:** <[<ref>] — when the item answers a request in another system; also in the title>

<!-- canon:begin fragment=trace-dates -->
| Trace field | Value | When |
|---|---|---|
| Start date | <YYYY-MM-DD> | The day WI-State becomes Active |
| Target date | <YYYY-MM-DD> | Planning — required before Ready |
<!-- canon:end -->

#### Value

Why this initiative exists, for whom, and what changes for them when it is done. Two paragraphs at
most. If it cannot be said in two paragraphs it is two Epics.

#### Outcome measures

How the organisation will know the Epic delivered. Measures, not features.

- <measure> — baseline: <value or `unknown`> → target: <value>

#### Features

Filled as refinement produces them. An Epic is never `Closed` by an agent (`RULE-ITEM-MODEL`).

- <FEATURE-ID> — <title> — <state>

#### Not in this Epic

<what a reader might assume is here and is not>

Canon: RULE-ITEM-MODEL

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
