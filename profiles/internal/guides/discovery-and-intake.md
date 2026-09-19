# Discovery and intake

How a request — from support, from another team, from a metric, from a hallway — becomes a card
an agent can execute, without anyone guessing what was meant.

## The path

```
request → intake note → Refinement → Story (Ready) → handoff
```

Every arrow is a human step. The agents' first contact with the work is the **handoff**; by then
the guessing has been done by people who could ask.

## 1. Intake note

Whoever receives the request writes four lines on a new item of type Story, state `New`, column
`Backlog`:

| Line | Content |
|---|---|
| **Who asked** | A role or a team, and where (a link to the ticket, the thread, the metric) |
| **What they said** | Their words, quoted. Not your interpretation |
| **What we think they need** | Your interpretation, marked as such |
| **What we do not know** | Honest placeholders: `- [ ] unknown — <what> → <who decides>` |

That is enough. Do not write acceptance criteria yet; you would be inventing them.

## 2. Refinement does the rest

The item goes to the next Refinement (`core/ceremonies/refinement.md`). There the PO:

- rewrites *What we think they need* as *As / I want / so that* — or sends the item back with a
  question to whoever asked;
- writes acceptance criteria that name their evidence;
- applies the four decisions: **ready · defer · split · cut**.

An intake note that still has an unresolved `unknown` on something the criteria depend on is
**defer**, with the question routed to the person who can answer it.

## 3. What intake is not

- **Not a Bug** unless the reproduction is written (`AP-BUG-FOR-GAPS`).
- **Not a Task** — Tasks come from Stories, in the handoff.
- **Not an agent's job.** An agent may draft the intake note from a thread if asked; a person
  reviews it before Refinement, because the person can ask the requester and the agent cannot.

## Signals that intake is working

- Items rejected at Review *because the criteria were wrong* trend down (retrospective signal).
- The share of Refinement time spent asking "what did they actually mean?" trends down.
- Requesters can find their request on the board within a day, in their own words.
