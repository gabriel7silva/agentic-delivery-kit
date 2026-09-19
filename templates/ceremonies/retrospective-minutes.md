# Retrospective — <iteration name>

Canon: RULE-CEREMONY-RETRO · RULE-RETRO-INPUTS · RULE-RETRO-CARDS

<!-- canon:begin fragment=ceremony-meta -->
| Field | Value |
|---|---|
| Date / time (timezone) | |
| Ceremony | |
| Iteration | |
| Roles present | |
| Where the round happened | in a room · written on the ceremony item · the system's channel, transcript attached |
| Board view on screen | |
<!-- canon:end -->

## Signals

| Signal | Value this iteration | Reading |
|---|---|---|
| Items rejected at Review, by criterion | | |
| Items that hit a human gate unnecessarily | | |
| Items that should have hit a gate and did not | | |
| Claims that expired | | |
| Reviewer findings all non-blocking | | |
| Resolved → Closed lead time | | |

## Cards

Every card names the iteration and its author as a role plus `human` or `agent`. An agent's card
cites the item it was drawn from.

<!-- canon:begin fragment=retro-cards -->
| Card | Iteration | Author (role · human/agent) | Text | Linked items |
|---|---|---|---|---|
| `went-well` | | | | |
| `went-wrong` | | | | |
| `recurring-impediment` | | | | |
| `improvement` | | | | |
<!-- canon:end -->

## What to change — the system, not the model

One to three, from the `improvement` cards. Each is a concrete edit to a brief, a floor, a template or an instance value, and
each becomes a work item.

| Change | File or value | Work item |
|---|---|---|
| | | |

## Actions

<!-- canon:begin fragment=actions-table -->
| Action | Owner (role) | Due |
|---|---|---|
| | | |
<!-- canon:end -->

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
