### <FEATURE-ID> <title>

- **Work item type:** Feature
- **Parent (Epic):** <EPIC-ID>
- **WI-State:** New
- **Owner (role):** {{roles.product_owner.title}}
- **Target iteration(s):**
- **Tags:**
- **External ref:** <[<ref>] — when the item answers a request in another system; also in the title>

<!-- canon:begin fragment=trace-dates -->
| Trace field | Value | When |
|---|---|---|
| Start date | <YYYY-MM-DD> | The day WI-State becomes Active |
| Target date | <YYYY-MM-DD> | Planning — required before Ready |
<!-- canon:end -->

#### Capability

What a user can do after this Feature that they cannot do before. One paragraph.

#### Stories

Filled as refinement produces them. A Feature reaches `Closed` when the PO accepts the capability,
not when the last Story is `Resolved` (`RULE-STATE-RESOLVED-NOT-CLOSED`).

| Story | Title | WI-State | Risk floor |
|---|---|---|---|
| <STORY-ID> | | New | |

#### Dependencies

- <item or external dependency> — <blocking · informational>

#### Risks

| Risk | Mitigation |
|---|---|
| | |

#### Out of scope

<what a stakeholder might expect under this name and will not get>

Canon: RULE-ITEM-MODEL

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
