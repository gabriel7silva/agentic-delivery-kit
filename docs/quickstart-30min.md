# Quickstart — one item, thirty minutes, nothing to install

You will take one small piece of work from a request to `Closed`, using the templates by hand.
No script runs. When you finish, you will know whether the method fits before you wire any tool.

**Rather let an agent do the setup?** Open the kit folder as your workspace and say *Read
`AGENTS.md` and set this up for my team*: [`AGENTS.md`](../AGENTS.md) runs the
[onboarding interview](onboarding/README.md) one block per turn and writes your instance only
after you confirm. No entry point loaded? Paste the [kick-off prompt](onboarding/kickoff-prompt.md). This page is the by-hand path — and the fastest way to feel whether the
method fits.

**You need:** a board with a text field or a label you can set (Azure DevOps, GitHub Projects,
Notion, or a hosted spreadsheet — its own track — **not** Slack), one agent you can paste a
prompt into, and yourself as PO and Approver. Slack is a notification mirror, never the board.

## 0 · Two minutes — the instance

Copy [`instance.example.yml`](../instance.example.yml) to `instance.yml`. Fill in
`organization.name`, `source_of_truth.board`, and the four role titles. Leave the rest
(`require_homologation_qa` is off in that example so this 30-minute path can finish without
QA and a key user). If you later turn that toggle on, Transfer also needs `HOMOLOG_LINK`
and `templates/flow/key-user-update.md`.

## 1 · Five minutes — Plan

Pick something real and small. Write it with
[`templates/work-items/user-story.md`](../templates/work-items/user-story.md):

- *As / I want / so that*.
- **Two** acceptance criteria, each naming the evidence that proves it.
- The **Out of scope / forbidden** section. Not empty.

Walk the Definition of Ready ([`core/06`](../core/06-ready-and-done.md)). If a line fails,
write an honest placeholder and stop — that is the method working, not failing.

Then write the handoff from [`templates/flow/handoff.md`](../templates/flow/handoff.md). Name
the scope the agent may touch in *Scope you may claim*. Write **Target date** on the board
field. Set the item to `In development`, write **Start date** (today) and `claim: <scope>` on it.

## 2 · Ten minutes — Act

Paste [`adapters/prompt-pack/out/implementer.md`](../adapters/prompt-pack/out/implementer.md)
into a fresh conversation with your agent, then the handoff. Let it work.

It should stop with: a change on a **feature branch** (not the default branch) linked from the
item, a filled [receipt](../templates/flow/receipt.md) that has a
**Not verified / not claimed** section with something in it, and a
[conclusion comment](../templates/flow/conclusion-comment.md) whose *Next step* is `review`.
If it says `closed`, the *Not verified* section is empty, or the board still has no branch /
dates, send it back — the brief told it not to.

## 3 · Eight minutes — Check

Open **two** new conversations. Paste
[`reviewer-correctness.md`](../adapters/prompt-pack/out/reviewer-correctness.md) into one and
[`reviewer-delivery-compliance.md`](../adapters/prompt-pack/out/reviewer-delivery-compliance.md)
into the other. Give each the diff, the criteria and the receipt. Each returns a verdict block.

Risk = the higher of what they said and what the path floor says
([`agents/policies/risk-floors.yml`](../agents/policies/risk-floors.yml)). If it is `high`, you
review it yourself now, before the next step.

Set the item to `Awaiting test` — the first state of the `Resolved` category. Remove the claim.

## 4 · Five minutes — Transfer

You are the Approver. Read the receipt's *Not verified* list **first**. Then each criterion
against its evidence. Accept — set `Closed`, column `Done` — or reject with one line naming the
criterion and what would satisfy it, and set `In development` again.

## What you just did

You ran every gate in the method by hand. The tracks and the CI automate these steps so they
cannot be skipped when nobody is watching — but the copy-ready guard checks the context in the
PR, not the board, until you wire that. If the thirty minutes felt right,
[`choose-your-track.md`](choose-your-track.md) is next. If they did not,
[`core/13`](../core/13-not-in-this-factory.md) may say why.
