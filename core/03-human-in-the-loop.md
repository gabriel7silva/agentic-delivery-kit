---
id: RULE-HITL
canon: true
---

# Human in the loop

Five triggers. Each one, on its own, forces the current step to stop and hand off to a named human.
They are written as **conditions** in `agents/policies/escalation.yml`, so an orchestrator or a
human can test them rather than trusting an agent to notice. The PR validator binds one derived
case: risk level `high`. The five triggers themselves are advisory in the gate until they are
expressed as that high-risk property.

| # | Trigger | Examples | Who decides |
|---|---|---|---|
| 1 | **Money, credentials or access** | Paying, creating a token, widening a permission, touching billing | Approver |
| 2 | **External publication** | Releasing, deploying to a shared environment, sending to a client or a third party | Approver |
| 3 | **Irreversible product decision** | Deleting data, changing a public contract, removing a feature | Product Owner |
| 4 | **Ambiguity or conflict** | Two acceptance criteria contradict; a business rule is not written down | Product Owner |
| 5 | **Risk of invention** | The agent would have to guess a fact, a value or a stakeholder's intent | Product Owner |

## What "stop" means

- The item stays in its current state. No transition is made on the agent's behalf.
- A comment on the item names the trigger, what is needed, and from whom (the *honest placeholder*
  form is fine: `- [ ] unknown — which retention period applies? → PO`).
- The Orchestrator moves on to other work. Waiting is not blocking the whole queue.

## What does not count

A transient tool failure is not a trigger — it is an `Issue` work item and a retry. Changing
iteration priority every time a tool hiccups is anti-pattern `AP-THRASH`.

## Relationship with risk

Risk level `high` (see `RULE-RISK`) is a sixth, derived trigger: it is what the five above look
like when they are expressed as a property of a change rather than of a moment. A change can be
high-risk without hitting any trigger literally; the human gate applies either way.

Canon: RULE-HITL
