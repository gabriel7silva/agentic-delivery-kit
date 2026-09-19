### WI-42 Export the customer list as CSV

- **Work item type:** Story
- **Parent (Feature):** WI-40 Customer list improvements
- **Epic:** WI-30 Reduce manual reporting
- **WI-State:** Awaiting development · column `Ready`
- **Target role / skill:** Implementer
- **Iteration:** Sprint 02 26 Q1 Acme Portal
- **Tags:** —

#### Description

As a Customer Success lead, I want to export the customer list as a CSV file, so that I can use
it in the weekly call without copying rows by hand.

**Context for the agent:** The customer list screen shows a table with filters. The export must
reflect **what is on screen** — the filtered rows and the visible columns — because that is what
the lead copies today. Answered at Refinement 2026-01-14 by the requester: filtered view; visible
columns; CSV is enough.

**Out of scope / forbidden:** No new columns. No scheduling or e-mailing of exports. Do not touch
the list's filtering logic. Do not add a dependency for CSV generation — the standard library is
enough.

#### Acceptance criteria

- [ ] AC1 — Given the customer list with a filter applied showing N rows, when the user clicks
      **Export CSV**, then a file `customers.csv` downloads with one header row and exactly N data
      rows, in the on-screen order. Evidence: the downloaded file for a fixture with 3 rows,
      attached.
- [ ] AC2 — Given a customer name containing a comma or a quote, when exported, then the CSV
      opens with that name intact in one cell. Evidence: a fixture row `"Doe, Jane"` and the
      exported file, attached.

#### Handoff to the orchestrator

- **Required inputs:** the list screen component; the existing table fixture with 3 rows.
- **Expected outputs:** the change, the receipt, the conclusion comment.
- **Escalate to the PO when:** the on-screen column set is not available to the export code
  without changing the filtering logic.

Refinement decision: **ready**.
