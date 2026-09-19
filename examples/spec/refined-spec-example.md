# 🔹 Customer list improvements — refined specification

**Fictitious.** Acme Corp, internal team. The raw request that produced Feature WI-40 — and,
through it, Story WI-42 of the [walkthrough](../walkthrough/README.md). Written by the PO
assistant in *refine* mode from one e-mail; the requester's name has become a role.

> **The request, as received:** "The customer list is a pain. I copy rows into a spreadsheet by
> hand for the weekly call, I would like the export to respect the filters I have on screen, it
> would be great if the weekly one just arrived by e-mail on Monday, and compliance asked who has
> been exporting customer data. Also the column headers come out as `first_name`."

## 🔹 Suggested Feature

| Field | Value |
|---|---|
| Feature | WI-40 — Customer list improvements |
| Parent Epic | WI-30 — Reduce manual reporting |
| Business objective | Let Customer Success get the list they are looking at out of the product without copying rows, without waiting for someone, and without losing track of who took customer data where |
| Requesting area | Customer Success |
| Requester (role) | Customer Success lead |
| Impacted users | Customer Success leads and analysts; compliance; whoever answers a data-access question |

## 📊 Expected benefits

- No manual copying before the weekly call — minutes saved per week, per lead.
- One export that matches what is on screen, so numbers in the call match numbers in the product.
- A record of every export of customer data, for compliance.
- Fewer "can you send me the list" requests to the product team.

---

## US 1 — Export the filtered customer list as CSV

**User story** — As a Customer Success lead, I want to export the customer list as a CSV file,
so that I can use it in the weekly call without copying rows by hand.

**Context** — The list screen shows a table with filters. Today the lead copies rows. The export
must reflect what is on screen — the filtered rows and the visible columns — because that is what
they copy today. *(Refined into Story WI-42; see the walkthrough.)*

**Acceptance criteria — scenarios**

*Scenario 1 — filtered export*
- Given the customer list with a filter applied, showing N rows
- When the user clicks **Export CSV**
- Then a file `customers.csv` downloads with one header row and exactly N data rows, in the
  on-screen order

*Scenario 2 — names with commas or quotes*
- Given a customer whose name contains a comma or a quote
- When the list is exported
- Then the file opens with that name intact in one cell

*Scenario 3 — nothing to export*
- Given a filter that matches no customer
- When the user clicks **Export CSV**
- Then the file has the header row only, and the screen says so

**Business rules to validate**

- Does "visible columns" mean the columns the user hid, or the fixed set the screen ships with?
  → Customer Success lead
- Is CSV enough, or do they need a spreadsheet format? → Customer Success lead *(answered at
  Refinement: CSV is enough)*

---

## US 2 — Scheduled weekly export by e-mail

**User story** — As a Customer Success lead, I want the filtered list sent to me by e-mail every
Monday morning, so that the weekly call starts with the file already in my inbox.

**Context** — The same export as US 1, produced on a schedule and delivered outside the product.
It leaves the product with customer data in it — that is a human gate (`RULE-HITL`, trigger 2)
and a high-risk path (`agents/policies/risk-floors.yml`: anything that sends data out).

**Acceptance criteria — scenarios**

*Scenario 1 — schedule a saved filter*
- Given a filter the user has saved
- When the user schedules it for Monday 07:00 in their timezone
- Then the export runs every Monday and an e-mail with the file reaches the user's address

*Scenario 2 — the filter changes*
- Given a scheduled export on a saved filter
- When the user edits the filter
- Then the next export uses the edited filter and the schedule stays

*Scenario 3 — the user loses access*
- Given a scheduled export owned by a user
- When that user's access to the customer list is removed
- Then the schedule stops and nobody receives the file

**Business rules to validate**

- May customer data leave the product by e-mail at all, and to which addresses (own address
  only? a distribution list?) → Compliance
- Retention: is the sent file kept anywhere? → Compliance

⚠️ **Risks and controls**

- Customer data in an inbox → own address only; no forwarding by the product; the audit log of
  US 3 records every send.
- A schedule that outlives the user → stops on access removal (Scenario 3).

📌 **Recommended rule**

> A scheduled export is an *external publication*: it needs a named human's approval before the
> first send, and it never goes to an address the user does not own.

---

## US 3 — Audit log of exports

**User story** — As a compliance analyst, I want to see who exported customer data, when, and with
which filter, so that I can answer a data-access question without asking around.

**Context** — Named by the request as "compliance asked". No log exists today.

**Acceptance criteria — scenarios**

*Scenario 1 — every export is recorded*
- Given a user exports the customer list, by button or by schedule
- When the export completes
- Then a log entry exists with the user, the timestamp, the filter used, the row count and the
  delivery (download or e-mail)

*Scenario 2 — the log is readable by the right role*
- Given a user with the compliance role
- When they open the export log
- Then they can filter it by user, by period and by delivery, and export the log itself

*Scenario 3 — the log is not editable*
- Given any user, including administrators
- When they try to change or delete a log entry
- Then the product refuses and records the attempt

📊 **Suggested metrics**

- Exports per week, by delivery type.
- Distinct users exporting customer data per month.
- Time to answer a data-access question (before / after).

---

## US 4 — Column headers as on-screen labels

**User story** — As a Customer Success lead, I want the CSV header row to use the labels I see
on screen, so that the file needs no translation before the call.

**Context** — Found during the review of WI-42 as a non-blocking finding and filed as WI-45. Small,
independent, and worth its own card rather than a "quick fix" inside another story.

**Acceptance criteria — scenarios**

*Scenario 1 — labels, not keys*
- Given the customer list with the columns *First name* and *Plan*
- When the user exports
- Then the header row reads `First name,Plan`, not `first_name,plan`

*Scenario 2 — a renamed column*
- Given an administrator renamed the *Plan* column to *Tier*
- When any user exports
- Then the header row says `Tier`

---

## 🧠 Refinement questions

### Filters
- Which filters must the export honour — all of them, or only the saved ones? → Customer Success lead
- Does the on-screen sort order matter in the file? → Customer Success lead

### Scheduling
- Which timezone drives "Monday 07:00" — the user's or the organisation's? → Product Owner
- Is there a maximum row count for an e-mailed file? → Platform reviewer (role)

### Audit
- Who may read the export log, and for how long is it kept? → Compliance
- Must the log itself be exportable? → Compliance

### Data
- Is the customer list personal data under the applicable regulation? Which columns? → Compliance

## ✅ Recommended registration

```
Epic WI-30 — Reduce manual reporting
└── Feature WI-40 — Customer list improvements
    ├── US 1 — Export the filtered customer list as CSV        → WI-42
    ├── US 2 — Scheduled weekly export by e-mail               → WI-43
    ├── US 3 — Audit log of exports                            → WI-44
    └── US 4 — Column headers as on-screen labels              → WI-45
```

> ⚠️ **Main rule:** the e-mail was not one User Story. It held four independent deliverables —
> an export, a schedule that publishes data outside the product, an audit trail and a cosmetic
> fix — with different risks and different approvers. One Feature, four stories, prioritised and
> homologated one by one. US 1 first; US 2 waits for Compliance's answers.

## 🔁 What changed from the original request

| Improvement | What was done |
|---|---|
| Clarity | "The list is a pain" became four named needs; the requester became a role |
| Structure | One e-mail → one Feature, four stories, eleven scenarios |
| Scope | The scheduled e-mail was separated because it publishes data outside the product |
| Testability | Every scenario names an observable result a key user can check |
| Prioritisation | The manual copying — the pain named first — is US 1; compliance's need is US 3 |
| Governance | A human gate on US 2, an audit log on every export, questions routed to Compliance |

- [ ] unknown — whether e-mail delivery is allowed at all for customer data → Compliance
