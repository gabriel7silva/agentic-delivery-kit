# Slack — channels

One channel per **purpose**, not per person or per agent. Agents post events; people answer in
threads; decisions are copied to the SoT. Bots talking to bots in a channel is `AP-BOT-CHATTER`.

| Channel | Purpose | Who posts | Who reads |
|---|---|---|---|
| `#delivery-updates` | Item events: claimed, resolved, closed, rejected (`event-formats/item-event.md`) | the sync / orchestrator | everyone |
| `#delivery-digest` | The daily digest, one scheduled message (`event-formats/digest.md`) | the sync | PO, Approver |
| `#delivery-gates` | Human gates: one thread per open gate (`event-formats/human-gate.md`) | orchestrator opens; humans answer | PO, Approver |
| `#delivery-blockers` | Open `Issue` items and their resolution | orchestrator | PO, whoever can unblock |
| `#<iteration-name-slug>` (optional) | Ceremony canvases and the iteration goal, pinned; the sprint-close minutes link back to the ceremony item on the board | PO | team |

## Thread etiquette

- **Every event is a top-level message; every discussion is its thread.** A channel with
  discussion at the top level is unreadable in a week.
- A thread's **decision** is posted as the last reply, prefixed `DECISION:`, and copied to the SoT
  item as a comment with a link back. Until it is on the SoT item, it has not been decided.
- Reactions are **signals**, not records: ✅ on a gate thread means *I answered in the thread*,
  not *approved*. The word "approved" is written, on the SoT item.

## Retention

Set the workspace's retention for these channels to at least one iteration length. Anything that
must outlive it is on the SoT by design — if it is not, that is the defect, not the retention.
