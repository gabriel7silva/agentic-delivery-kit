# Receipt — <ITEM-ID> <short title>

The Definition of Done made concrete. Written by the implementer when it believes the item is
finished; read by the reviewer and the Approver. Everything here traces to a tool output or a
source. Anything that does not goes in **Not verified / not claimed** — that section is what makes
the rest of the receipt trustworthy.

Canon: RULE-DOD · RULE-EVIDENCE · RULE-GOLDEN-NO-INVENTION

## Summary

Two to five lines, in the language of the acceptance criteria. What changed, for whom.

## Where

| Field | Value |
|---|---|
| Branch | |
| Change / pull request | <link> |
| Merge reference | <commit or `not merged`> |
| Scopes claimed | `<scope-id>`, … |

## Files touched

<list, grouped by scope — or "see change" if the tool shows it better>

## Commands run

The exact commands and their exit status. Output attached or linked, not summarised.

```
<command>   → exit 0
<command>   → exit 0
```

## Acceptance, criterion by criterion

| AC | Result | Evidence |
|---|---|---|
| AC1 | pass · fail · out of scope | <link or attachment> |
| AC2 | pass · fail · out of scope | <link or attachment> |

## Not verified / not claimed

Mandatory. What was **not** checked, so that its absence above is not read as a pass.

- <e.g. not run on the production-like environment; only unit tests>
- <e.g. no manual check of the exported file in a spreadsheet application>
<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

## Risks and follow-ups

Each one is an `Issue` or a Story, linked. None is left only in this section.

- <follow-up> → <ITEM-ID>

## Review gate

| Reviewer (role) | Verdict | Risk | Blocking findings |
|---|---|---|---|
| reviewer-correctness | pass · pass-with-findings · block | low · medium · high | <count> |
| reviewer-security | | | |

**Risk of this change:** `MAX(verdicts, floors)` = <low · medium · high> · Canon: RULE-RISK

## For the Approver

- [ ] Conclusion comment posted on the item (`RULE-CONCLUSION-COMMENT`)
- [ ] Item is in a Resolved-category state (`Awaiting test` on the default lifecycle) — never in `Done`
- [ ] `BRANCH` and `CHANGE_LINK` are on the **board fields**, not only in this receipt
- [ ] `START_DATE` and `TARGET_DATE` are set on the item
- [ ] When `require_homologation_qa` is on: Check review passed before QA started the env;
      `HOMOLOG_LINK` is set; the **key user** tested there; **Review (Transfer)** has that
      evidence — QA did not test the product
- [ ] Human gate required before `Closed`: yes (<trigger>) · no

<!-- canon:begin fragment=traceability-table -->
| Field | Value |
|---|---|
| Product Owner (role) | {{roles.product_owner.title}} |
| Executor (role) | |
| Branch | <feature branch — never `main`> |
| Change / pull request | <URL> |
| Homologation | <URL — QA starts; key user tests> |
| Evidence | |
| Start date | |
| Target date | |
| Closed date | |
<!-- canon:end -->

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
