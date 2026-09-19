# Cross-squad dependencies

A dependency on another team is a fact about an item, recorded on the item, watched by the
orchestrator, unblocked by a human. It is not a meeting.

## Record it

On the dependent item, an `Issue` of kind *dependency* linked with **Blocks**:

| Field | Value |
|---|---|
| Blocks | <this item> |
| Depends on | <the other team's item, by their id and board> |
| Needed by | <date the iteration goal needs it> |
| Contact (role) | <the other team's owner, by role> |
| What exactly | <the interface, the data, the decision — precisely enough that "done" is checkable> |

The dependent item stays `New`; it is not `Ready` while the Issue is open. Pulling it anyway
means an implementer will stop on the first missing piece and post an honest placeholder — the
predictable outcome of skipping this step.

## Watch it

The Issue appears in section 2 of the daily digest (`RULE-DAILY-DIGEST`) until closed. The
orchestrator re-checks the other team's item state on every digest; when it reaches their
`Closed`, the orchestrator closes the Issue and the dependent item may become `Ready`.

## Unblock it

If *Needed by* passes with the Issue open, it becomes a **decision needed from a human** (digest
section 3): the PO talks to the other team's owner. Options, in order of preference:

1. **Re-scope** — can the item deliver value without the dependency, with a follow-up item for
   the rest? Refinement decision: **split**.
2. **Stub** — can the interface be stubbed behind a flag so the item reaches `Resolved` and waits
   on the real thing only for `Closed`? Record the stub in the receipt's *Not verified*.
3. **Defer** — the item moves to a later iteration. Refinement decision: **defer**.

What is not an option: an implementer from this team writing into the other team's scope. Their
paths are theirs (`RULE-SCOPE`); if `ownership.yml` names their reviewer on a shared scope, the
claim still belongs to one implementer, and it is theirs to give.

## When this team is the one being depended on

Treat the other team's need as an intake note (`discovery-and-intake.md`). It gets a Story, goes
through Refinement, and is prioritised on value like everything else — with the requesting team's
*Needed by* visible on the card so the PO can weigh it honestly.
