# The kick-off prompt — what to paste when you want the interview

Two ways start the onboarding. **Say anything** — a greeting, *"let's adopt this"* — when the entry
point loaded on its own (the kit folder is open, or the pointer files are at your root). **Paste
this prompt** when it did not, or when you want the interview whatever the runtime has read: the
kit sits in a subfolder, the runtime is one the kit has no pointer for, or the chat has no access
to files at all.

## The prompt

Paste it as your first message. Any language works — the agent answers in yours; this is what it
must say:

```text
Read AGENTS.md at the root of this repository — or .pact/AGENTS.md if the kit is vendored — and
follow its setup protocol: run the onboarding interview in docs/onboarding/interview.md with me,
one block per turn. Ask the block's questions, then stop and wait for my answers. Show me what
you understood as a table. Write no file — not instance.yml, not a context file, not a rule for
your runtime — before I confirm the last block. Answer in my language. Start with Block 0 now.
```

## Without file access

A plain chat that cannot open the repository still runs the interview: paste `AGENTS.md`, then
`docs/onboarding/interview.md`, then the prompt above. The answers become an `instance.yml` you
copy into your repository; `python3 automation/scripts/check_instance.py instance.yml` checks it.

## What to expect

| The agent's first reply | Meaning |
|---|---|
| The questions of Block 0 — language, purpose, organization, product, confidentiality — and nothing else | The protocol is running. Answer; one block per turn follows |
| A summary of the kit, then a question about what you want | Fine: say *set it up for my team* and Block 0 follows |
| A finished `instance.yml`, context files or rule files | It did not read `AGENTS.md`. Delete them, paste the prompt again — that setup is `AP-SILENT-SETUP` |

The interview ends with one table of every decision and its source; nothing is written before
your yes ([`interview.md`](interview.md), Block 9). Then the agent writes the outputs of
[`setup-plan.md`](setup-plan.md).
