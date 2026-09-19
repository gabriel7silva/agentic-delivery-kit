# Closed — WI-42

The only step a human writes as a state change.

## What the Product Owner did

1. Read the receipt's *Not verified / not claimed* **first**. Three entries. Asked the Customer
   Success lead to open `customers_3rows.csv` in their spreadsheet application — they did, it was
   fine. Accepted the other two as known limits.
2. Checked AC1 and AC2 against their evidence. Both attached, both as described.
3. Posted the acceptance on the item:

```markdown
## Accepted

| Field | Value |
|---|---|
| Accepted by (role) | Product Owner |
| Date | 2026-01-16 16:35 UTC |
| Criteria | AC1 ✅ · AC2 ✅ |
| Not verified — accepted as known limits | spreadsheet open (now verified by requester) · >200 rows · header labels → WI-45 |
```

4. WI-State `Awaiting test → Closed` — this instance runs no homologation stage
   (`examples/instance-internal-github.yml` → `lifecycle`), so the PO's own test on the export
   was the human test; column `Awaiting test → Done`; the GitHub issue closed as completed.

## What did not happen

- No agent set `Closed`. The validator would have refused it; the PO did not need it to.
- The item did not wait in a queue. It reached `Awaiting test` at 15:40 and the PO tested it at the
  sprint close an hour later ([`examples/ceremonies/sprint-close-example.md`](../ceremonies/sprint-close-example.md));
  had it resolved on Tuesday it would have been accepted on Tuesday — `Resolved` items are reviewed
  as they come (`core/ceremonies/review.md`).
- The non-blocking finding was not "quickly fixed" before acceptance. It is WI-45, in the
  backlog, and will go through Refinement like anything else.

Total: four days from intake to Closed, of which the agent's part was one afternoon and the
human parts were a Refinement, a review of two files, and a spreadsheet opened by the person who
asked.
