# Adapter — prompt pack

One Markdown file per agent, usable as the system prompt or first message in **any** chat with
**any** model. No runtime feature is assumed: no sub-agents, no tools, no file access. If a role
can be run from a pasted prompt, the roster is neutral — that is what this adapter proves.

## Use

Copy `out/<agent>.md` into a fresh conversation as the opening message, then give the agent its
inputs (the handoff, the diff, the receipt). For a review, open **one conversation per reviewer**
and paste each reviewer's prompt — that is your parallel, read-only review.

`out/README.md` is the index with the order to run them in.

## What this runtime enforces

Nothing. A pasted prompt is advice. That is fine, because none of the method's guarantees depend
on the runtime (`agents/README.md`): the PR validator enforces scope, claims, reviewers, risk and
evidence on the change itself. What the prompt pack gives you is agents that **know the rules**;
what the validator gives you is a gate that **does not care whether they did**.

| Concept | Here | Stands in |
|---|---|---|
| Read-only reviewer | instruction in the prompt | the reviewer has no write access to begin with |
| Parallel review | one conversation per reviewer | — |
| Single writer per scope | instruction | PR validator (`RULE-SCOPE`, `RULE-CLAIM`) |
| Claims | instruction to record on the item | PR validator |
| Human gate | instruction to stop and post | PR validator refuses `Closed` by an agent |

## Regenerate

```bash
python adapters/prompt-pack/generate.py          # writes out/
python adapters/prompt-pack/generate.py --check  # what CI runs
```
