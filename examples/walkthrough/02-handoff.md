# Handoff — WI-42 Export the customer list as CSV

## Meta

| Field | Value |
|---|---|
| Item | WI-42 · Story |
| Parent | WI-40 → WI-30 |
| Iteration | Sprint 02 26 Q1 Acme Portal |
| Target role / skill | Implementer |
| Suggested branch | `story/WI-42-export-csv` |
| Depends on | none |
| Status of this handoff | **active** |

## Read before starting

1. `AGENT-CONTEXT.md` and `CURRENT-FOCUS.md`
2. WI-42 acceptance criteria, on the board
3. `src/customers/list.py` — the screen that owns the visible columns and filtered rows

## Objective

A user can download the customer list they are looking at as a CSV file.

## Story

As a Customer Success lead, I want to export the customer list as a CSV file, so that I can use
it in the weekly call without copying rows by hand.

**Context for the agent:** export what is on screen — filtered rows, visible columns, on-screen
order. CSV via the standard library.

## Acceptance criteria

- [ ] AC1 — filtered list of N rows → `customers.csv` with 1 header + N data rows, on-screen
      order. Evidence: exported file for the 3-row fixture.
- [ ] AC2 — a name with a comma or quote survives as one cell. Evidence: fixture `"Doe, Jane"`
      and the exported file.

## Scope you may claim

- `app` — `src/**` (the list screen and the new export function)
- `tests` — `tests/**`

## Out of scope / forbidden

- Do not publish, deploy, pay, delete, or contact anyone outside the team.
- Do not touch paths outside the claimed scopes.
- Do not change the filtering logic in `src/customers/filters.py`.
- Do not add a CSV or spreadsheet dependency.
- Do not add columns, scheduling, or e-mail.

## Constraints

- Verification that must pass: `make lint`, `make test`
- One branch per item; commits reference `WI-42`.
- Stop and post a comment when any human-in-the-loop trigger applies.

## Definition of Done for this item

- AC1 and AC2 evidenced, or explicitly out of scope in the receipt.
- Receipt filled, including *Not verified / not claimed*.
- Conclusion comment posted on WI-42.
- Claim released. Item at `Awaiting test` — not `Closed`.

## Expected receipt

Attach the two exported files. Say whether you opened them in a spreadsheet application or only
inspected the bytes — the requester will want to know.
