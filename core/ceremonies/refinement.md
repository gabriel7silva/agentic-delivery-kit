---
id: RULE-CEREMONY-REFINEMENT
canon: true
---

# Refinement

**PO's role: owner.** Prioritise by value; detail; write the acceptance criteria; leave with items
that are clear, small and estimable. Bad refinement means agents hallucinate or stall. Good
refinement means cheap, auditable execution. It is the highest-leverage hour in the method.

| Do | Don't |
|---|---|
| Prioritise by value | Prioritise by what is easy to prompt |
| Write and rewrite Stories in the form *As / I want / so that* | Leave the persona implicit — the agent will invent one |
| Make acceptance criteria **executable and verifiable** by an agent and by a human | Write criteria that only the author can judge |
| Walk the Definition of Ready (`RULE-DOR`) line by line | Mark `Ready` because the title is clear |
| Split Features that do not fit one execution window | Push a large item through and hope the agent splits it well |

## The four decisions — `RULE-REFINEMENT-DECISIONS`

Every item discussed leaves with exactly one of:

| Decision | Meaning | Next state |
|---|---|---|
| **ready** | Passes the DoR. May be pulled | `Awaiting development` — the *Ready* column |
| **defer** | Valid, not now. Reason recorded | `New` or `In analysis` — the *Backlog* |
| **split** | Too large for one handoff. Children created, parent stays | Parent `New`; children go through refinement |
| **cut** | Not worth doing | `Removed` (never `Closed` — `RULE-STATE-REMOVED`) |

At the sprint close, Refinement is Part 3 (`RULE-CEREMONY-SPRINT-CLOSE`): the four decisions apply
to the **next** iteration's candidates — the retrospective's `improvement` cards among them — and
the closing iteration's open items receive their carry-over decision (`RULE-CARRY-OVER`) in the
same breath, so that what did not finish and what enters next are decided by the same people with
the same evidence.

## Output

- Every discussed item carries one of the four decisions in the minutes and on the item.
- Acceptance criteria updated **on the item**, not only in the minutes.
- Minutes: Part 3 of `templates/ceremonies/sprint-close-minutes.md`, or
  `templates/ceremonies/refinement-minutes.md` when held apart.

## Writing criteria an agent can execute

A criterion is executable when it names the **evidence** that satisfies it:

> *Given a list with three rows, when the user clicks "Export", then a CSV with three data rows and
> one header row is downloaded.* — Evidence: the downloaded file, attached.

A criterion is not executable when it says *"export works correctly"*. The agent will decide what
"correctly" means, and it will be wrong in a way that is expensive to discover at Review.

Canon: RULE-CEREMONY-REFINEMENT · RULE-REFINEMENT-DECISIONS
