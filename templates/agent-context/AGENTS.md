# Agents: read this first — {{organization.name}}

This repository runs **PACT** (Plan → Act → Check → Transfer). The kit lives at `.pact/` — or was
copied out into this repository; either way the method is the same and this file is your entry
point. Runtime-specific pointer files at the root point here.

## Read, in this order

1. `{{conventions.agent_context_file}}` — stable context: product, layout, verification, rules.
2. `{{conventions.current_focus_file}}` — this iteration: goal, active item, branch, out of scope.
3. Your brief — `adapters/prompt-pack/out/<role>.md` in the kit. Roles and who fills them are in
   `instance.yml` (`topology: {{topology}}`).
4. The handoff for your item, linked from the item on the board. No handoff, no work.

## Rules that bind every agent here

- Only a human sets `Closed`. You stop at `Awaiting test` (`RULE-STATE-RESOLVED-NOT-CLOSED`).
- Claim the scope on the item before you write; write only inside it (`RULE-CLAIM`).
- Nothing invented: `- [ ] unknown — <what> → <who decides>` (`RULE-GOLDEN-NO-INVENTION`).
- Every action leaves a trace **on the work item** — the board fields for branch, change and
  dates included (`RULE-GOLDEN-TRACE`).
- Stop and post a gate request when a human-in-the-loop trigger applies (`RULE-HITL`).
- Answer and write artifacts in `{{language}}`; keys, ids and code stay in English.

## Where the truth is

Source of truth: **{{source_of_truth.track}}**, board **{{source_of_truth.board}}**. A channel, a
chat or this repository's files are never the record of an item's state.

## Changing the setup

The instance exists; do not run the onboarding interview again unless asked. When a person wants
to change a name, the board, the cadence or a role, run the interview block that owns that key
(`docs/onboarding/interview.md` in the kit), show the answer back, then edit `instance.yml` and
run the instance check. The pointer files for every runtime are regenerated, never edited:
`python3 <kit>/automation/scripts/entry_points.py --root . --kit <.pact or .>`.

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
