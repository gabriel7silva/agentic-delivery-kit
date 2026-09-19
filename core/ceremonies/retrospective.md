---
id: RULE-CEREMONY-RETRO
canon: true
---

# Retrospective

**PO's role: member of the system.** An active member, open to feedback and to improvement
commitments of their own. The system is improved — skills, briefs, floors, the Definition of
Ready, the gates — not the personality of a model.

| Do | Don't |
|---|---|
| Review failures of **skill, brief, connector, DoR** — the parts you can change | Blame the model |
| Adjust briefs, guardrails, risk floors, the agents' Definition of Done | Ask an agent to "be better" without changing its card or its brief |
| Record **one to three** actionable improvements — a more testable criterion, a narrower Task, a floor that was too wide | Hold an abstract debate about AI |

## What to look at — `RULE-RETRO-INPUTS`

The retrospective has data the human-only version never had. Use it:

| Signal | Where | What it suggests |
|---|---|---|
| Items rejected at Review, by criterion | Review minutes | Criteria that agents misread → rewrite the DoR example |
| Items that hit a human gate they should not have | Escalation comments | A floor or a trigger too wide |
| Items that **should** have hit a gate and did not | Post-hoc, from incidents | A floor too narrow — the expensive one |
| Claims that expired | Orchestrator log | Items too large for one session → split earlier |
| Reviewer findings that were all `non-blocking` | Review verdicts | A reviewer brief that is not finding what matters |
| Time from `Resolved` to `Closed` | Board | The Approver is the bottleneck, not the agents |

## Cards — `RULE-RETRO-CARDS`

The retrospective runs on **cards**, written on the ceremony item (`sprint-close.md`) by people
and by agents alike, before or during the session. Four kinds, with fixed ids:

| Card | Asks | Written by |
|---|---|---|
| `went-well` | What worked — a practice, a brief, a criterion that made execution cheap | People; agents, from evidence |
| `went-wrong` | What did not — a rejection, a rework, a gate that fired late | People; agents, from evidence |
| `recurring-impediment` | What blocked this iteration **and** a previous one — the `Issue` that keeps coming back | People; the orchestrator, from the impediment queue |
| `improvement` | A suggestion: the concrete edit that would remove a `went-wrong` or a `recurring-impediment` | Anyone. Refined in Part 3 of the sprint close; the ones accepted become items for the next iteration or the backlog |

Every card carries the **iteration name**, its author as a role plus `human` or `agent`, the text,
and the items it links. An agent's card is an **observation**: it cites the rejection, the expired
claim, the blocked time, the review finding or the human gate it was drawn from
(`RULE-RETRO-INPUTS`); a card an agent cannot back with an item is not written
(`RULE-GOLDEN-NO-INVENTION`). A person's card may be an opinion — that is what people are for.
The fragment `templates/_fragments/retro-cards.md` is the table the minutes copy.

## Output

- One to three changes, each as a **concrete edit**: to a brief in `agents/briefs/`, a floor in
  `agents/policies/risk-floors.yml`, a template, or an instance value.
- Each change is itself a work item, so it goes through the same gates.
- The cards, on the ceremony item and in the minutes — Part 2 of
  `templates/ceremonies/sprint-close-minutes.md`, or `templates/ceremonies/retrospective-minutes.md`
  when the retrospective is held apart.

Canon: RULE-CEREMONY-RETRO · RULE-RETRO-INPUTS · RULE-RETRO-CARDS
