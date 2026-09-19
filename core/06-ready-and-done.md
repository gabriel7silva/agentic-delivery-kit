---
id: RULE-DOR-DOD
canon: true
---

# Definition of Ready · Definition of Done

Two checklists. The first is the gate into `Active`; the second is the gate out of `Resolved`. The
handoff template is the DoR made concrete; the receipt template is the DoD made concrete
(`templates/flow/`). Neither checklist is copied anywhere else — templates point here.

## Definition of Ready — `RULE-DOR`

Before an item may become `Active`:

- [ ] **Title** is clear enough to be the subject line of the change.
- [ ] **Description** in the form *As [persona], I want [goal], so that [benefit]* — plus enough
      context for an agent to execute without guessing.
- [ ] **Acceptance criteria** are testable — each one is pass/fail, and says what evidence proves it.
      When one line is not enough, a criterion is a scenario: *Given* a context, *when* an action,
      *then* an observable result.
- [ ] **Evidence** is attached or linked (document, screenshot, API, repository) — or the criterion
      is explicitly marked `unknown` (`RULE-GOLDEN-NO-INVENTION`).
- [ ] **Limits** are explicit — what the agent must **not** do: publish, pay, delete, contact
      anyone external, touch paths outside the scope.
- [ ] **Parent** Feature and Epic are filled in.
- [ ] **Target role or skill** is named (or the queue it goes to).
- [ ] **Target date** is set on the board field (`TARGET_DATE`).
- [ ] **Suggested branch** is named (pattern from `instance.yml`). The branch itself is created
      in Act, from the item when the track can link it.
- [ ] **Stop condition** is written: what "done" looks like and what to report when finishing.

An item that fails one line is not ready. Pulling it anyway is how agents hallucinate or stall —
refinement quality is the cheapest lever this method has.

## Definition of Done — `RULE-DOD`

Before an item may be presented for `Closed`:

- [ ] **Every acceptance criterion** is either evidenced or explicitly marked out of scope in the
      conclusion comment.
- [ ] **Evidence is attached** — an artifact, a test run, a screenshot, a log.
- [ ] **Nothing invented** — every claim in the receipt traces to a tool output or a source.
- [ ] **Issues opened** for every remaining blocker or follow-up.
- [ ] **Reviewed by a human** if the item carries `needs-human` or its risk is `high`.
- [ ] **Branch** is on the board field (`BRANCH`) — the feature branch of this item, not the
      default branch.
- [ ] **Change / pull request** is on the board field (`CHANGE_LINK`).
- [ ] **Start date** is set (`START_DATE`).
- [ ] **When `require_homologation_qa` is on:** Check review has passed (`Resolved`) before
      QA started anything. QA wrote `BRANCH` + `HOMOLOG_LINK`. The **key user** tested on
      that URL. **Review (Transfer)** accepted that evidence. QA does not test the product.

The receipt has one more mandatory section that the DoD implies but people forget:
**Not verified / not claimed** — the list of things that were *not* checked. A receipt without it is
incomplete, because the absence of a claim would otherwise be read as a claim.

## Sizing

If a Story cannot be executed inside one agent session with a single scope claim, it is not one
Story. Split it in refinement (`decision: split`). The method has no estimate field on purpose:
the unit of sizing is "fits one handoff".

Canon: RULE-DOR-DOD · RULE-DOR · RULE-DOD
