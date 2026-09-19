# Sprint close — <iteration name>

Canon: RULE-CEREMONY-SPRINT-CLOSE · RULE-CARRY-OVER · RULE-RETRO-CARDS · RULE-CEREMONY-REVIEW · RULE-CEREMONY-RETRO · RULE-REFINEMENT-DECISIONS · RULE-ITERATION-NAMING

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

## Ceremony item

| Field | Value |
|---|---|
| Item | <ID> — `<iteration name> — Sprint close` · tag `process: ceremony` |
| Parent | <the standing *Ceremonies <year>* Story> |
| Cards and evidence | comments on the item, posted before or during the window |
| Window | <from> → <to> (timezone) |

## Part 1 — Review

### Iteration goal

<the sentence from Planning> — **achieved: yes · partial · no**

### Items reviewed

| Item | Title | Outcome | Evidence that decided it | Homologation / key-user | Note (if rejected: which AC, what would satisfy it) |
|---|---|---|---|---|---|
| | | closed · rejected → active · still open → carry-over | <link> | <`HOMOLOG_LINK` + key-user verdict, or `n/a`> | |

### Not verified / not claimed — carried from receipts

- <item>: <gap> — accepted · needs verification before close

### Learnt → new backlog items

- <title> — <type> — <why>

## Part 2 — Retrospective

### Signals

| Signal | Value this iteration | Reading |
|---|---|---|
| Items rejected at Review, by criterion | | |
| Items that hit a human gate unnecessarily | | |
| Items that should have hit a gate and did not | | |
| Claims that expired | | |
| Reviewer findings all non-blocking | | |
| Resolved → Closed lead time | | |

### Cards

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

### What to change — the system, not the model

One to three, from the `improvement` cards. Each is a concrete edit to a brief, a floor, a
template or an instance value, and each becomes a work item.

| Change | File or value | Work item |
|---|---|---|
| | | |

## Part 3 — Refinement

### Candidates for the next iteration

| Item | Title | Decision | Acceptance criteria notes |
|---|---|---|---|
| | | ready · defer · split · cut | |

### Carry-over of this iteration's open items

One decision per item not in the `Closed` or `Removed` category, mirrored onto the item.

| Item | Title | State (category) | Decision | Reason | Decided by (role) | Applied on the item |
|---|---|---|---|---|---|---|
| | | | carry · return · remove | | | yes · no |

## Next iteration

| Field | Value |
|---|---|
| Name | <from `{{cadence.iteration_name_pattern}}` — `automation/scripts/iteration_name.py --start <date>`> |
| Start → end | <date> → <date> · sprint close on <date> |
| Candidates | <the `ready` rows above, plus the carried items> |
| Goal (draft for Planning) | <one sentence, or an honest placeholder> |
<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

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
