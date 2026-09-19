# Onboarding — your agent sets it up

Open the kit with any agent — a coding CLI, an IDE agent, a chat — and say *"let's adopt this"*,
or paste the [kick-off prompt](kickoff-prompt.md). `AGENTS.md` at the root sends the agent here. It runs the **interview**
— one block of questions per turn, your answers shown back, no file written before you confirm —
and then writes the **setup plan** and the files an instance needs, the pointer files for every
runtime included. A person can run the same interview on themselves with a text editor; nothing
here needs an agent.

## Where to open it

Runtimes read `AGENTS.md` and their own rule file from the folder you **opened**, never from a
subfolder. Open the kit folder itself as your workspace, or your repository with the kit at
`.pact/` and the pointer files at its root —
`python3 .pact/automation/scripts/entry_points.py --root . --kit .pact` writes one for every
runtime the kit knows (`--list` names them). If the agent's first reply to "set this up" is a
finished `instance.yml` instead of a block of questions, it did not read `AGENTS.md`: point it
there and start again. An instance nobody answered for is `AP-SILENT-SETUP`. Before the setup
exists, the pointers at your root send the agent to `.pact/AGENTS.md`; once your own `AGENTS.md`
is written, to that one.

## Trying it without instructions

The test that matters is the one where you tell the agent nothing: open the folder (the kit, or
your repository with the pointers at its root), start a fresh chat in agent mode, and type a
greeting or *"let's adopt this"* — no file name, no command. Expected: the agent says this is the
PACT kit and offers the three requests, or goes straight to Block 0 of the interview; nothing is
written until you confirm Block 9. A first reply that reads the repository and then hands you a
finished `instance.yml` means the entry point was not loaded — check which folder is open, or
paste the [kick-off prompt](kickoff-prompt.md), which works whatever the runtime has read.

| Step | File | What it is |
|---|---|---|
| 1 | [`interview.md`](interview.md) | The questions, in blocks: purpose and names, who accepts, topology, tool, where things live, lifecycle, cadence, risk, conventions — each with *why we ask*, *writes to* and *default if unanswered*. One block per turn |
| 0 | [`kickoff-prompt.md`](kickoff-prompt.md) | The message to paste when the entry point did not load, or when the chat has no access to files: it makes any agent run the interview, one block per turn, and write nothing before you confirm |
| 2 | [`setup-plan.md`](setup-plan.md) | What the agent produces from the answers: `instance.yml`, `AGENT-CONTEXT.md`, `CURRENT-FOCUS.md`, the adopter's `AGENTS.md` with the generated pointer files, and a `SETUP-PLAN.md` that says what is done, what is theirs to do and what is still unknown |

## What onboarding does not do

- It does not create the board, the project, the fields or the labels in your tool. The setup
  plan lists those steps from the track's `setup.md`, marked *yours*; the agent stops at the
  edge of any external tool (`RULE-HITL`).
- It does not decide value. Names, priorities and the first items are yours; the interview
  records them, the agent does not guess them (`RULE-GOLDEN-NO-INVENTION`).
- It does not write before it asks. The interview ends with one confirmation table; the files
  come after it, never before.
- It does not change the method. Every answer lands in `instance.yml`, a profile, a track or an
  adapter — never in `core/`.

## After the interview

Run `make instance` (or `python .pact/automation/scripts/check_instance.py instance.yml`): it
refuses an instance whose topology contradicts its roles, whose lifecycle drops a category, or
whose source of truth cannot be one. Then walk one item through by hand
([`docs/quickstart-30min.md`](../quickstart-30min.md)) before wiring anything.
