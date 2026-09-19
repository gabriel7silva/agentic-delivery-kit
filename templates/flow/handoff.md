# Handoff — <ITEM-ID> <short title>

The Definition of Ready made concrete: everything an implementer needs to execute **without
guessing**, and everything it must not do. If a section cannot be filled, the item is not ready —
write an honest placeholder and send it back to Refinement.

Canon: RULE-DOR · RULE-GOLDEN-SCOPE · RULE-CLAIM

## Meta

| Field | Value |
|---|---|
| Item | <ITEM-ID> · <type: Story / Task / Bug> |
| Parent | <FEATURE-ID> → <EPIC-ID> |
| Iteration | |
| Target role / skill | {{roles.implementer.title}} |
| Suggested branch | `{{conventions.branch_pattern}}` — write it on the board `BRANCH` field in Act, never `main` |
| Target date | <YYYY-MM-DD — already on the board field; if empty this handoff is not Ready> |
| Depends on | <items that must be `Closed` first, or `none`> |
| Status of this handoff | draft · **active** · superseded |

## Read before starting

Ordered. The implementer reads these and nothing else is assumed.

1. `{{conventions.agent_context_file}}` and `{{conventions.current_focus_file}}`
2. <the item's acceptance criteria, on the board>
3. <a decision record, a previous receipt, a design note — only what this item needs>

## Objective

One or two sentences. What exists after this item that does not exist before.

## Story

As <persona>, I want <goal>, so that <benefit>.

**Context for the agent:** <what the agent needs to know about the domain to not invent it>

## Acceptance criteria

Each one pass/fail, each one naming its evidence.

- [ ] AC1 — <criterion> · Evidence: <what proves it>
- [ ] AC2 — <criterion> · Evidence: <what proves it>
<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

## Scope you may claim

The scopes from `agents/ownership.yml` this item is allowed to write to. Claiming outside this list
is out of scope by definition.

- `<scope-id>` — <paths, for the reader's benefit>

## Out of scope / forbidden

What the agent must **not** do. This section is mandatory; an empty one is a defect of the card.

- Do not publish, deploy, pay, delete, or contact anyone outside the team.
- Do not touch paths outside the claimed scopes.
- <item-specific limits>

## Constraints

- Verification that must pass: {{conventions.verification_commands}}
- One branch per item; commits reference `<ITEM-ID>`. Link that branch and its pull request on
  the item's board fields (`BRANCH`, `CHANGE_LINK`) — not only in this handoff.
- Stop and post a comment when any human-in-the-loop trigger applies (`RULE-HITL`).

## Definition of Done for this item

- Every AC above evidenced or explicitly marked out of scope.
- Receipt filled from `templates/flow/receipt.md`, including *Not verified / not claimed*.
- Conclusion comment posted on the item (`RULE-CONCLUSION-COMMENT`).
- Claim released. Item at `Awaiting test` (Resolved) — **not** `Closed`.

## Expected receipt

<anything specific the PO wants to see in the receipt: a screenshot of X, the output of command Y>

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
