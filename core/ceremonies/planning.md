---
id: RULE-CEREMONY-PLANNING
canon: true
---

# Planning

**PO's role: protagonist.** The PO presents the priorities, the business objective, the rules and
the acceptance criteria, and builds the iteration goal **with** the team; the team defines the
implementation. The orchestrator and the agents plan the breakdown into Tasks. Planning opens the
iteration on its first day, from the candidate list and the carry-over the sprint close left
(`RULE-CEREMONY-SPRINT-CLOSE`).

| Do | Don't |
|---|---|
| Present the prioritised items with a description and acceptance criteria clear enough for an agent to execute **without guessing** | Ask an agent to "find out what the business wants" with no evidence |
| Set one **iteration goal** in one sentence | Let the orchestrator choose the value scope alone |
| Negotiate **capacity**: token budget, queues, execution windows, which agents are available | Dictate the technical *how* when the agent already has the skill |
| Assign Stories to roles or skill queues | Mix five objectives in one prompt with no parent Feature |

## Output

- The iteration's **name**, rendered from the pattern (`RULE-ITERATION-NAMING`) and prepared at
  the previous sprint close — on the iteration entity and as the H1 of the minutes.
- The iteration goal, one sentence, on the board.
- The list of items in the iteration. Their WI-State may stay `New` until an agent pulls them.
  Every item that enters the iteration — carried items included (`RULE-CARRY-OVER`) — has
  `TARGET_DATE` written on the board field, not only in these minutes.
- A map item → role or skill queue.
- Confirmation that every item passes the Definition of Ready (`RULE-DOR`) — Planning is not the
  place to discover it does not; that is Refinement's job.
- Minutes: `templates/ceremonies/planning-minutes.md`, including the risks table and the
  **honest placeholders** for anything not yet known.

## Capacity with agents is not people-hours

It is a budget of runs, tokens, review passes and human gate slots. A high-risk item costs two human
gates (`RULE-RISK-GATES`); five of them in one iteration is a queue on the Approver, not on the
agents. Plan for the human bottleneck first.

## Sprint metrics — `RULE-OPT-SPRINT-METRICS`

Optional. An instance that plans with numbers keeps them **on the board fields**, never only in
the minutes:

| Field | Level | Set by | Read at |
|---|---|---|---|
| `EFFORT` | Story, Feature | Refinement or Planning | Planning — what fits the iteration |
| `REMAINING_WORK` | Task | whoever executes | The burndown, every day |
| `BUSINESS_VALUE` | Epic, Feature | The PO | Ordering the backlog, with `PRIORITY` |
| `ITERATION_CAPACITY` | Iteration, per role | Planning | Planning — the human bottleneck first |

The method's own sizing rule stays: a Story fits one handoff or it is split (`RULE-DOD`). The
numbers exist for capacity and for reporting — never for judging an agent by hours.

Canon: RULE-CEREMONY-PLANNING · RULE-OPT-SPRINT-METRICS
