---
id: RULE-CEREMONY-SPRINT-CLOSE
canon: true
---

# Sprint close

**PO's role: central, then member, then owner.** One session, three parts, in this order:
**Review** — the PO is central, value is accepted with evidence; **Retrospective** — the PO is a
member of the system being improved; **Refinement** — the PO owns what enters next. The order is
the point: what was delivered is judged before how it was delivered, and both before what comes
next. Each part keeps its own page (`review.md`, `retrospective.md`, `refinement.md`); this page
adds what only the combined session has — the ceremony item, the carry-over, and the hand-over to
Planning. It is held on the iteration's last working day (`cadence.sprint_close`); Planning opens
the next iteration on its first day.

| Do | Don't |
|---|---|
| Hold the three parts in order, in one session, on the iteration's last working day | Review one day and refine another, and lose the link between what failed and what enters next |
| Open the ceremony item before the session and let cards and evidence accumulate on it | Collect cards in a chat and paste a summary |
| Give every open item of the closing iteration one carry-over decision, written on the item | Let unfinished items slide into the next iteration by default, with no reason recorded |
| Name the next iteration and list its candidates, so Planning starts from a list | Plan during the close, or close during Planning |
| Judge the iteration goal — achieved, partial, not achieved — in one line | Re-accept item by item what the Approver already drained during the week |

## The three parts

| Part | Page | What this session adds |
|---|---|---|
| 1 · Review | `review.md` | The iteration goal judged in one line; the items still open listed for the carry-over |
| 2 · Retrospective | `retrospective.md` | Cards from people **and** agents (`RULE-RETRO-CARDS`); the `improvement` cards go to Part 3, not to a parking lot |
| 3 · Refinement | `refinement.md` | The four decisions on the next iteration's candidates (`RULE-REFINEMENT-DECISIONS`); the carry-over on this iteration's open items (below) |

## Inputs

The digest of the day (`RULE-DAILY-DIGEST`), the receipts and conclusion comments of the items
that reached a Resolved-category state, the rejections written at Review during the week, the six
signals of `RULE-RETRO-INPUTS`, and the cards already on the ceremony item. Nothing is collected
orally; what is not on an item is not an input.

## The ceremony item

The session has a home on the board: a `Task` titled `<iteration name> — Sprint close`, tagged
`process: ceremony`, child of the standing *Ceremonies <year>* Story (`core/04-work-item-model.md`).
Cards and evidence are **comments** on it; the minutes are attached to it or linked from it; the
carry-over decisions are mirrored from it onto each item they concern. When the round is written
(`RULE-CEREMONY-PARTICIPATION`), this item *is* the room. A person closes it once the minutes are
signed, like any other item — it counts as process, never as delivered value.

## Carry-over — `RULE-CARRY-OVER`

At the sprint close every item assigned to the closing iteration that is not in the `Closed` or
`Removed` category receives **exactly one** decision, recorded in the minutes and on the item —
the iteration field changed, one comment with the decision and its reason:

| Decision | Meaning | Effect on the item |
|---|---|---|
| **carry** | The work continues next iteration; its state does not change | Iteration → the next one; `TARGET_DATE` re-set at Planning |
| **return** | Not next iteration; back to the backlog | Iteration cleared. An Active-category item releases its claim and goes back to `Awaiting development` or `In analysis` — the return transition of `core/05-states.md` |
| **remove** | It will not happen | `Removed` — a human's act, never counted as delivered (`RULE-STATE-REMOVED`) |

Two defaults keep the table honest. An item in a Resolved-category state that waits on people —
a test, a homologation, an acceptance — **carries**, reason *awaiting human validation*: the agents
are done with it and the queue belongs to a person. An item in an Active-category state whose
claim has expired is **returned** unless someone writes why it should carry.

Who decides follows the topology (`RULE-CEREMONY-PARTICIPATION`): the PO; the PO-agent inside its
mandate and the sponsor outside it; the dispatcher; the bot system's manager inside its mandate
and the human Approver otherwise. An agent may **propose** a decision on the ceremony item; a
decision counts when the deciding role has written it. `remove` is never proposed into effect.

## Output

- The iteration goal judged, in one line, in the minutes.
- Every open item of the closing iteration with its carry-over decision, on the item.
- One to three system changes from the `improvement` cards, each a work item (`RULE-CEREMONY-RETRO`).
- The next iteration's **name** (`RULE-ITERATION-NAMING`), its dates, and its candidate list with a
  refinement decision on each — what Planning starts from on the first day.
- Minutes: `templates/ceremonies/sprint-close-minutes.md`, attached to the ceremony item.

Canon: RULE-CEREMONY-SPRINT-CLOSE · RULE-CARRY-OVER
