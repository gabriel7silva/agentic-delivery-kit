# Sprint close — Sprint 02 26 Q1 Acme Portal

**Fictitious.** Acme Corp, internal team, the week the walkthrough's WI-42 shipped
(2026-01-12 → 2026-01-18). The minutes of the Friday session in the shape of
`templates/ceremonies/sprint-close-minutes.md`, with the fences and placeholders rendered, so that
the **shape** of a real set of minutes is what you notice. Roles, never names; one product, one
board; every number traceable to an item.

| Field | Value |
|---|---|
| Date / time (timezone) | 2026-01-16 16:00 → 17:00 UTC |
| Ceremony | Sprint close — review → retrospective → refinement |
| Iteration | Sprint 02 26 Q1 Acme Portal (2026-01-12 → 2026-01-18) |
| Roles present | Product Owner (human, also the Approver) · Delivery Orchestrator (agent) · Implementer (agent) · reviewer-correctness and reviewer-delivery-compliance (agents) · Key user (human, absent — sent the WI-43 note) |
| Where the round happened | in a room (the PO) · written on the ceremony item (every agent, cards posted between Thursday 18:00 and Friday 16:00 UTC) |
| Board view on screen | the `Delivery` project, filtered on the iteration |

## Ceremony item

| Field | Value |
|---|---|
| Item | WI-50 — `Sprint 02 26 Q1 Acme Portal — Sprint close` · tag `process: ceremony` |
| Parent | WI-34 — *Ceremonies 2026* (Story) → WI-33 — *Delivery process 2026* (Feature) → WI-31 — *Unplanned work 2026* (Epic) |
| Cards and evidence | eight comments on the item: six cards, the digest of the day, the key user's note on WI-43 |
| Window | 2026-01-15 18:00 → 2026-01-16 17:00 UTC |

## Part 1 — Review

### Iteration goal

*Customer Success exports its own lists without asking the data team* — **achieved: partial**.
The export ships; the scheduled run still waits on the key user.

### Items reviewed

| Item | Title | Outcome | Evidence that decided it | Homologation / key-user | Note (if rejected: which AC, what would satisfy it) |
|---|---|---|---|---|---|
| WI-42 | Export the customer list as CSV | closed | Receipt of 2026-01-16 15:40: `customers_3rows.csv`, `customers_quoted.csv`; AC1 ✅ · AC2 ✅ | n/a — this instance runs no homologation stage | Accepted 16:35 by the Product Owner; the header-labels finding is WI-45 |
| WI-43 | Scheduled weekly export by e-mail | still open → carry-over | Conclusion comment of 2026-01-15 11:20; the key user tests the Monday run | n/a | Waits on a person, not on an agent |
| WI-44 | Audit log of exports | still open → carry-over | Claim on `app/audit/**` released on expiry, 2026-01-15 09:00; no conclusion comment | n/a | Second expiry in two iterations — see the cards |

### Not verified / not claimed — carried from receipts

- WI-42: exports above 200 rows were not tried — accepted as a known limit; revisit when a customer list is that long.
- WI-42: the file opened in a spreadsheet application — verified by the requester on Friday, before acceptance.

### Learnt → new backlog items

- Nothing new this week: the one finding of the review, column headers as on-screen labels, is already WI-45.

## Part 2 — Retrospective

### Signals

| Signal | Value this iteration | Reading |
|---|---|---|
| Items rejected at Review, by criterion | 0 | — |
| Items that hit a human gate unnecessarily | 0 | — |
| Items that should have hit a gate and did not | none known | — |
| Claims that expired | 1 — WI-44, `app/audit/**` | The item is larger than one session |
| Reviewer findings all non-blocking | 1 of 1 — WI-42, the header labels | Fine at this size; watch the reviewer brief if it repeats |
| Resolved → Closed lead time | WI-42: 55 minutes | The Approver was in the room |

### Cards

Every card names the iteration and its author as a role plus `human` or `agent`. An agent's card
cites the item it was drawn from.

| Card | Iteration | Author (role · human/agent) | Text | Linked items |
|---|---|---|---|---|
| `went-well` | Sprint 02 26 Q1 Acme Portal | Product Owner · human | The criterion "a CSV with three data rows and one header row" was executed without one question back | WI-42 |
| `went-well` | Sprint 02 26 Q1 Acme Portal | reviewer-delivery-compliance · agent | Receipt, conclusion comment and both CSV files were on the item before the review started; one pass | WI-42 (receipt, 2026-01-16 15:40) |
| `went-wrong` | Sprint 02 26 Q1 Acme Portal | Delivery Orchestrator · agent | WI-43 has waited 29 hours in `Awaiting test` for a key-user test nobody was assigned to | WI-43 (state change, 2026-01-15 11:20) |
| `recurring-impediment` | Sprint 02 26 Q1 Acme Portal | Delivery Orchestrator · agent | The claim on `app/audit/**` expired for the second iteration in a row: the implementer's session ends before the conclusion comment | WI-44 (claim releases 2026-01-08 and 2026-01-15) |
| `improvement` | Sprint 02 26 Q1 Acme Portal | Implementer · agent | Split a Story that touches two modules into two Tasks, so that one claim fits one session | WI-44 |
| `improvement` | Sprint 02 26 Q1 Acme Portal | Product Owner · human | Name the key user on every Story before it leaves Refinement | WI-43 |

### What to change — the system, not the model

One to three, from the `improvement` cards. Each is a concrete edit to a brief, a floor, a
template or an instance value, and each becomes a work item.

| Change | File or value | Work item |
|---|---|---|
| A Story that touches two modules is split before the claim is written | `templates/flow/handoff.md` → *Scope you may claim*; the DoR walk in Refinement | WI-51 |
| The refinement minutes carry the key user's role before an item is `ready` | `templates/ceremonies/refinement-minutes.md` → *Items refined* | WI-52 |

## Part 3 — Refinement

### Candidates for the next iteration

| Item | Title | Decision | Acceptance criteria notes |
|---|---|---|---|
| WI-51 | Split two-module Stories before the claim | ready | Given a handoff whose scope spans two modules, when the DoR is walked, then the Story is split and neither child claims two scopes |
| WI-52 | Key user named at Refinement | ready | Given a Story that turns on homologation, when Refinement ends, then the minutes name the key user or the decision is `defer` |
| WI-45 | Column headers as on-screen labels | defer | Waits on the labels decision — refinement question *Data* in the specification |

### Carry-over of this iteration's open items

One decision per item not in the `Closed` or `Removed` category, mirrored onto the item.

| Item | Title | State (category) | Decision | Reason | Decided by (role) | Applied on the item |
|---|---|---|---|---|---|---|
| WI-43 | Scheduled weekly export by e-mail | Awaiting test (Resolved) | carry | Awaiting human validation — the key user tests the Monday run on 2026-01-19 | Product Owner | yes |
| WI-44 | Audit log of exports | In development (Active) | return | The claim expired twice; back to `Awaiting development` once WI-51 has split it | Product Owner | yes |
| WI-46 | E-mail the customer list every Monday | New (New) | remove | Duplicate of WI-43 | Product Owner | yes |

## Next iteration

| Field | Value |
|---|---|
| Name | Sprint 03 26 Q1 Acme Portal |
| Start → end | 2026-01-19 → 2026-01-25 · sprint close on 2026-01-23 |
| Candidates | WI-43 (carried) · WI-51 · WI-52 |
| Goal (draft for Planning) | The weekly export runs on its own, and the process stops losing claims |
- [ ] unknown — whether Compliance signs the audit-log fields this month → Product Owner

## Actions

| Action | Owner (role) | Due |
|---|---|---|
| Mirror the three carry-over decisions onto WI-43, WI-44 and WI-46 — iteration field and comment | Delivery Orchestrator | 2026-01-16 17:30 UTC |
| Assign the key user on WI-43 and post the test date | Product Owner | 2026-01-19 |
| Attach these minutes to WI-50 and close it | Product Owner | 2026-01-16 |

---
Source of truth: github-projects · Board: Delivery · Iteration: 7 days · Timezone: UTC
Roles: PO = Product Owner · Orchestrator = Delivery Orchestrator · Implementer = Implementer · Approver = Product Owner
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
