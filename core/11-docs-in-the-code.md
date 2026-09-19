---
id: RULE-DOCS-IN-CODE
canon: true
---

# Docs in the code

Agents read what is near the code they touch. Documentation that lives elsewhere is documentation
they have to be told about, every session, at a cost. So this method keeps **two** kinds of
documentation with **different homes**, and is strict about which is which.

## Two kinds — `RULE-CONTEXT-VS-TRAIL`

| Kind | Read when | Lives | Examples |
|---|---|---|---|
| **Agent context** | Every session, automatically | Next to the code, at the repository root | `AGENT-CONTEXT.md`, `CURRENT-FOCUS.md`, skill or instruction packs |
| **Audit trail** | On demand, to reconstruct a decision | A `docs/` tree, or the work-item tool | Receipts, ceremony minutes, decision records, handoffs after they are executed |

The test: *does this need to be remembered every session?* If yes, it is context and it goes next to
the code. If it serves to reconstruct a decision later, it is trail and it goes in `docs/`.

## Agent context — the two files

**`AGENT-CONTEXT.md`** — stable. What the product is, how the repository is laid out, the
commands that verify it, the rules that apply to every change, where the source of truth is. Changes
rarely. Owned by whoever owns the repository's conventions.

**`CURRENT-FOCUS.md`** — volatile. Which Feature is active, which Story, which branch, what is out
of scope *this week*, which handoff to read before coding. Changes every iteration. Owned by the PO
or the orchestrator, and its last line always says who updates it and when.

Templates for both are in `templates/agent-context/`, next to `AGENTS.md` — the one entry file
an agent reads first, which names the other two. Different runtimes look for different file
names; the root carries a three-line pointer under each such name, all pointing at `AGENTS.md`.
The content is in one place.

## Why the split matters

A single "everything" file grows until the agent spends its context window re-reading last quarter's
decisions. A `docs/` tree with no stable context file means every session starts by asking the same
questions. Two files, two lifetimes, one rule for which is which.

## The audit trail is not optional

Golden rule 5 requires traces. The trail is where traces that do not fit on a work item go: a
retrospective's decisions, a decision record for an architecture choice, a receipt too long for a
comment. It is read rarely and must still be written every time — its value is exactly that it
exists when someone asks "why did we do this?".

Canon: RULE-DOCS-IN-CODE · RULE-CONTEXT-VS-TRAIL
