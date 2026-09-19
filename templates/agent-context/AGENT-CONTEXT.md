# <Product name> — agent context

Read at the start of **every** session. Stable: this file changes when the repository's conventions
change, not when the iteration does. For what is active this week, read `CURRENT-FOCUS.md`.

Canon: RULE-CONTEXT-VS-TRAIL

## Product

<two or three lines: what it is, for whom, the one constraint that shapes everything (offline, regulated, multi-tenant, …)>

## Repository

- **Layout:** <top-level directories and what each owns>
- **Source of truth for work items:** {{source_of_truth.track}} — board `{{source_of_truth.board}}`
- **Audit trail:** `docs/` — receipts, minutes, decisions. Read on demand, not every session.

## Verify before you claim anything works

```
{{conventions.verification_commands}}
```

The exact commands the review gate runs. If they do not pass locally, the change is not ready.

## Rules that apply to every change

- Read the handoff for the item before writing a line. No handoff, no work.
- Claim the scope in the source of truth first; write only inside it (`RULE-CLAIM`).
- Branch: `{{conventions.branch_pattern}}`. One item per branch. Write the name on the board
  field (`BRANCH`) the moment it exists — never the default branch. Write the pull-request URL
  on `CHANGE_LINK`. `START_DATE` is the day the item became Active; `TARGET_DATE` is already
  there from Planning.
- When finished: receipt, conclusion comment on the item, claim released. The item goes to
  `Awaiting test` (the Resolved category) — never `Closed` (`RULE-STATE-RESOLVED-NOT-CLOSED`).
- Stop and comment when a human-in-the-loop trigger applies (`RULE-HITL`): money, access,
  publication, irreversible decision, ambiguity.
- Never invent. Write `unknown` and ask.

## Scopes and floors

See `agents/ownership.yml` and `agents/policies/risk-floors.yml`. The short version:

| Scope | Paths | Floor |
|---|---|---|
| | | |

## Language

<code, commits and comments language>

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
