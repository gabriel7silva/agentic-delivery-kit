# Start here — the model in ten minutes

You have a Product Owner — a person, or an agent working under one — some AI agents that can
write code, and a backlog. This kit tells you how to run that so the agents are fast **and**
nothing reaches a user that a human did not accept. Ten minutes covers the ideas; the rest of the kit is the mechanics.

## One item's life

```
Plan ──► Act ──► Check ──► Transfer
NEW     ACTIVE   RESOLVED   CLOSED        ← categories; REMOVED is the exit
```

Those are **categories**. Each holds one or more states — twelve by default, from `New` through
`In development` and `Awaiting test` to `Closed` ([`core/05`](../core/05-states.md)). Rules and
gates read the category; the board shows the state; your instance may run fewer states, never
fewer categories.

| Phase | What happens | Who |
|---|---|---|
| **Plan** | The PO writes a card with acceptance criteria that name their evidence, and what the agent must **not** do. The orchestrator turns it into a handoff | Humans, then the orchestrator |
| **Act** | One agent claims a scope — a set of paths — and works inside it. Nobody else writes there meanwhile | One implementer |
| **Check** | Verification runs. Reviewers read the change in parallel and each returns findings **and** a risk level. A receipt says what was done and — separately — what was **not** checked | Machines, then reviewer agents |
| **Transfer** | A human reads the receipt, especially the *not verified* list, and accepts or rejects | The Approver |

The line that holds it together: **`Resolved ≠ Closed`.** Agents can finish. Only a human can
accept. Every tool track in this kit is set up so that those are two different fields.

## Five rules everything else derives from

1. Agents report by event and log, not by standup.
2. A human is in the loop wherever there is money, access, publication, an irreversible
   decision, or ambiguity.
3. Scope is closed per card — a card without a *forbidden* section is not ready.
4. Nothing is invented — `unknown — <what> → <who decides>` is a valid answer.
5. Every action leaves a trace on the work item — including the board fields for
   branch, change, start date and target date. A comment that names them while
   those fields stay empty is not a trace.

Full text: [`core/02-golden-rules.md`](../core/02-golden-rules.md).

## Three mechanisms that make it enforceable

**Two state axes.** The work item's lifecycle (`WI-State`) and the board column (`Status`) are
separate fields. `Done` is a column only `Closed` reaches. → [`core/04`](../core/04-work-item-model.md)

**N readers, one writer.** Reviewers are many and read-only. Writers are one per scope, with a
claim recorded on the item. A PR validator refuses a change outside its claim.
→ [`core/09`](../core/09-concurrency.md), [`agents/`](../agents/README.md)

**Risk = MAX(reviewer verdict, path floor).** Reviewers can raise risk; a per-path floor means
nobody can lower it. High risk means a named human before the agent may even say it is done.
→ [`core/08`](../core/08-review-and-risk.md)

## What you do next

Same order as the README:

1. This page (you are here).
2. Pick your topology — agents → human, agents → agents, independent agents, an existing bot
   team: [`scenarios/`](scenarios/README.md).
3. Walk one item through by hand: [`quickstart-30min.md`](quickstart-30min.md).
4. Pick where your work items live: [`choose-your-track.md`](choose-your-track.md) — Azure DevOps,
   GitHub Projects, Notion, or a hosted spreadsheet for a first week. Slack is a mirror, never
   the board.
5. Pick who your approver is: [`choose-your-profile.md`](choose-your-profile.md).
6. Copy `instance.example.yml` → `instance.yml`. The Approver is who sets `Closed`.

Or skip the list: open the kit folder as your workspace, say *Read `AGENTS.md` and set this up
for my team*, and answer the [onboarding interview](onboarding/README.md) one block at a time —
no file is written before you confirm. If the agent hands you a finished `instance.yml` instead of
questions, it did not read [`AGENTS.md`](../AGENTS.md); paste the
[kick-off prompt](onboarding/kickoff-prompt.md) instead.

## What this kit is not

It is not a runtime, an agent framework, or a tool integration. It is a method with the files
that make it checkable. It does not know which model you use, and a CI check keeps it that way.
Read [`core/13-not-in-this-factory.md`](../core/13-not-in-this-factory.md) before adopting —
the list of what it does not cover is short and honest.
