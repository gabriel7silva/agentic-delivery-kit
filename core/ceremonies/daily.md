---
id: RULE-CEREMONY-DAILY
canon: true
---

# Daily sync

**PO's role: observer.** A secondary participant, available for business questions; never
chasing anyone individually, never changing priorities unilaterally. Intervenes only for business
risk.

The "daily" of an agent team is **telemetry plus an impediment queue**, not a meeting. Nobody asks
an agent what it did yesterday; the work item already says (`RULE-CONCLUSION-COMMENT`).

| Do | Don't |
|---|---|
| Read the orchestrator's digest: blockers, tool failures, ambiguous acceptance criteria | Collect oral status from each agent |
| Unblock **business**: a decision, an access, a priority | Change iteration priorities on every transient failure (`AP-THRASH`) |
| Clarify a domain question **in a comment on the item**, where the agent will read it | Turn the sync into micromanagement of prompts |

## The digest — `RULE-DAILY-DIGEST`

Generated, not written. Built from the evidence and conclusion comments on the items, in this order:

1. **Active items** — progress against acceptance criteria, from the latest evidence comment.
2. **Blockers** — open `Issue` items: auth, tool, dependency, ambiguity.
3. **Decisions needed from a human** — every open human gate (`RULE-HITL`), with the trigger and
   who it waits on.
4. **Ready for review** — items in a `Resolved`-category state (`Awaiting test` onwards) whose Check review has passed, oldest first.
   When `require_homologation_qa` is on, this line is only items that also have `HOMOLOG_LINK`
   and a key-user test on the item. Resolved waiting on QA or on the key user is **not**
   the Approver's queue yet (`core/14-homologation.md`).

The digest is posted where the PO reads (a channel, an e-mail, a board view). It is **not** the
source of truth; it is a projection of it. If the digest and the board disagree, the board is right
and the digest generator has a bug. On the day of the sprint close it is also the session's first
input (`RULE-CEREMONY-SPRINT-CLOSE`).

## Output

Nothing new on the items — that would be `AP-INVENTED-STATUS`. The output is the PO's decisions,
each written as a comment on the item it concerns.

Canon: RULE-CEREMONY-DAILY · RULE-DAILY-DIGEST
