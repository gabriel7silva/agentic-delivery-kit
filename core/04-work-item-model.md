---
id: RULE-ITEM-MODEL
canon: true
---

# Work item model

The hierarchy is the same one most delivery tools already have. What changes with agents is not the
shape but **who carries each level**.

```
Epic
 └── Feature
        └── Story (PBI)
             └── Task   ← the unit an agent executes
```

Auxiliary types, outside the hierarchy: **Bug** (a proven defect) and **Issue** (an impediment —
tool, auth, dependency, ambiguity).

| Type | Represents | Carried by | Agents may close it? |
|---|---|---|---|
| **Epic** | A value initiative, months | PO / management | Never |
| **Feature** | A capability, a few iterations | PO; agents deliver its children | Never |
| **Story** | A need with acceptance criteria | PO writes; agents execute; PO accepts | Never — `Resolved` at most |
| **Task** | An objective technical step | An implementer (or a short chain) | `Resolved`; `Closed` only by a human |
| **Bug** | A proven defect | An implementer, with regression evidence | `Resolved` at most |
| **Issue** | A blocker | Orchestrator escalates to a human | `Resolved` at most; `Closed` only by a human |

## The two axes — `RULE-TWO-AXES`

Every item has **two** independent properties that tools often conflate:

| Axis | Values | Meaning | Who moves it |
|---|---|---|---|
| **WI-State** | Twelve states in five fixed **categories** — `New` · `Active` · `Resolved` · `Closed` · `Removed` (`core/05-states.md`) | Where the item is in its *lifecycle* | Agents up to the `Resolved` category; humans beyond |
| **Status** | Board columns — by default one per state, `Backlog` … `Done` | Where the item sits *on the board* | Derived from WI-State. Never set `Done` while WI-State is still in the `Resolved` category |

They are related but not identical. The `Resolved`-category states map to their own columns
(`Awaiting test` … `Integration test`), never to `Done`. `Done` is a column that only `Closed`
may reach. Each track declares its own translation; the default is in
`core/model/board-columns.yml`. When a board tool stores Status as a separate field, an agent
must not move Status past the WI-State mapping — Status is a view, not a second lifecycle.

Keeping the axes separate is what lets a Kanban board be honest: a card in `Awaiting test` tells
you *an agent finished and a person has not tested yet* — which is exactly the information the PO
needs at the start of the day.

## Typical flow

1. Business / PO defines Epics.
2. Epics → Features.
3. Features → Stories, made ready for an agent (`RULE-DOR`).
4. Stories → Tasks (closed prompts / skills).
5. Bugs and Issues appear during execution and join the queue.

## Tags — a taxonomy, not a cloud

Tags answer questions a field does not. They work when every tag belongs to a **family** with a
short list of allowed values, written in `instance.yml` → `conventions.tags`; a tag outside its
family is noise the next reader cannot filter on.

| Family | Answers | Examples |
|---|---|---|
| `process` | What does this item need from the method? | `needs-human` · `spike` · `gap` · `improvement` · `tooling` · `doc` · `qa` · `ceremony` |
| `category` | Why does it exist? | improvement · legal requirement · duplicate of another request |
| `module` | Which part of the product? | the product area, as your team names it |
| `project` | Which initiative pays for it? | the initiative's name |
| `year` | When was it requested? | the year, for queries that outlive iterations |

Keep `needs-human` whatever else you drop — it is how a human gate is made visible on a board
that has no other way to show it (`RULE-HITL`). "Blocked" is a **state**, not a tag
(`core/05-states.md`); "current iteration" is the iteration field, not a tag.

## External references — `RULE-OPT-EXTERNAL-REF`

When an item answers a request that lives in another system — a service desk ticket, a contract
line, an incident — that reference travels with the item: on the board field `EXTERNAL_REF`
**and** at the start of the title, `[<ref>] <title>`, so it survives every view, every export
and every chat mention. The item's own id stays the id of record; the reference is the way back
to the requester. Optional; instances that field requests this way turn it on
(`require_external_ref`).

## One standing Epic for unplanned work

Interrupts happen — an incident, a legal deadline, a customer escalation. They still get a card,
a Feature and Refinement; what they do not get is a place in a planned initiative. One standing
Epic per year, *Unplanned work <year>*, holds them, so that the roadmap stays honest and the
Retrospective can read how much of the iteration was planned (`RULE-RETRO-INPUTS`). Under it, one
Feature *Delivery process <year>* and one Story *Ceremonies <year>* parent the ceremony items — one
`Task` per sprint close (`RULE-CEREMONY-SPRINT-CLOSE`) — so that process work is visible,
queryable, and never mistaken for delivered value.

Canon: RULE-ITEM-MODEL · RULE-TWO-AXES · RULE-OPT-EXTERNAL-REF
