# Agents: read this first

You are an AI agent opening the **PACT — Agentic Delivery Kit**. This file says what to do when a
person asks you to read, analyse, set up or use this repository. Runtimes that read `AGENTS.md`
natively load it on their own; every other runtime gets a pointer file generated from one
template — `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/pact.mdc`, `.github/copilot-instructions.md`,
`.windsurf/rules/pact.md` and the rest (`python3 automation/scripts/entry_points.py --list`) — so
every runtime lands here. **They are read from the folder a person opened, never from a
subfolder** (see the last section).

## What this repository is

A **delivery method** — PACT: Plan → Act → Check → Transfer — for teams where AI agents execute
and humans accept, plus the files that make it checkable: a neutral model, templates, one track
per tool, an agent roster, adapters and a PR validator. It is not a runtime and it does not call
a model. Ten-minute version: [`docs/start-here.md`](docs/start-here.md).

## First contact

When a person's first message here is not one of the three requests below — a greeting, "what
is this?", "help", anything vague — say in one line that this repository is the PACT kit and
offer the three: explain it, set it up for their team (an interview, one block per turn), or act
as a role. Write no file. When the message is a setup request in **any** wording — "let's adopt
this", "configure it for us", "I want to use this", "vamos adotar" — do not ask what to do:
start the interview at Block 0.

## Three requests you will get

| The person says | What you do |
|---|---|
| **"Read this repository and tell me how it works."** | Read, in this order: [`docs/start-here.md`](docs/start-here.md) · [`core/README.md`](core/README.md) and `core/01` to `core/05` · [`docs/scenarios/README.md`](docs/scenarios/README.md) · [`docs/choose-your-track.md`](docs/choose-your-track.md) · [`agents/README.md`](agents/README.md). Then answer in the person's language, in the shape of [`core/16-writing-standard.md`](core/16-writing-standard.md). Say what you did not read. Do not summarise a file you did not open. |
| **"Set this up for my company / project / team."** — or any request that needs names, a board, a topology or a tool | Follow the **setup protocol** below: the interview of [`docs/onboarding/interview.md`](docs/onboarding/interview.md), one block per turn, no file before the person confirms; then exactly the outputs of [`docs/onboarding/setup-plan.md`](docs/onboarding/setup-plan.md). Never skip the interview because the request looks obvious or the person seems in a hurry; the answers *are* the instance. |
| **"Act as the `<role>`."** — orchestrator, implementer, a reviewer, the PO assistant | Your brief is `adapters/prompt-pack/out/<role>.md` ([index](adapters/prompt-pack/out/README.md)); the roster is [`agents/roster.yml`](agents/roster.yml). Read the instance's `AGENT-CONTEXT.md` and `CURRENT-FOCUS.md` first when they exist. |

## Setup protocol — the interview comes first

A setup request — "set this up", "let's adopt it", "configure PACT for us", or any request that
needs a name, a board, a topology or a tool — is a **conversation**, not a form you fill in:

1. Your first reply is **Block 0** of [`docs/onboarding/interview.md`](docs/onboarding/interview.md):
   its questions, in the person's language, and nothing else. Then **end your turn and wait**.
   Do not answer the questions yourself.
2. **One block per turn.** Ask, stop, wait. After each answer, show what you understood as a
   table; a missing answer gets the block's default *offered*, never silently applied.
3. **Write no file** — not `instance.yml`, not a context file, not a rule for your own runtime —
   before the confirmation of Block 9. A file written before the interview ended is invented
   (`AP-SILENT-SETUP`, `RULE-GOLDEN-NO-INVENTION`): delete it and start the interview.
4. "Just use the defaults" is an answer to show, not to assume: put every default in the
   confirmation table and get one yes before writing anything.
   A person who pastes the [kick-off prompt](docs/onboarding/kickoff-prompt.md) — or `AGENTS.md`
   and the interview into a chat with no file access — gets the same protocol: Block 0 first.
5. Then produce exactly the outputs of [`docs/onboarding/setup-plan.md`](docs/onboarding/setup-plan.md),
   the pointer files for every runtime included — generated, never typed:
   `python3 <kit>/automation/scripts/entry_points.py --root <adopter root> --kit .pact`
   (`--kit .` when the kit was copied out).

## If nothing sent you here

Runtimes load `AGENTS.md` and their own rule files from the folder a person **opened** — never
from a subfolder. When this kit sits inside another workspace, the pointers are invisible and you
may reach this file only because someone named it. This file is still the instruction: follow it
as written, and tell the person that opening the kit folder itself — or running the pointer
generator at their root — is what makes the next session start here on its own.

## Rules that bind you in this repository

1. **Only a human sets `Closed`.** Never do it, never ask a tool to (`RULE-STATE-RESOLVED-NOT-CLOSED`).
2. **Do not invent.** When a fact, a name or an intent is missing, write
   `- [ ] unknown — <what> → <who decides>` and ask (`RULE-GOLDEN-NO-INVENTION`).
3. **Nothing personal in files.** No person's name, e-mail, handle, machine path, token or link to
   a private board goes into anything you write here — the leak check refuses it. Organization and
   product names the person gives you go only into the instance and its context files.
4. **Do not edit `core/` on an adopter's behalf.** The method is canon. An instance configures it
   through `instance.yml`, a profile, a track and an adapter — never by rewriting a rule.
5. **You write files; people create boards.** Ask before touching an external tool, spending
   money or publishing anything (`RULE-HITL`). The setup plan says what is yours and what is theirs.
6. **Verify what you changed:** `make check` (needs `pip install -r automation/requirements.txt`).

## Where things are

| You need | Open |
|---|---|
| The method, one rule per file | [`core/`](core/README.md) |
| The same method as YAML | [`core/model/`](core/model/README.md) |
| Cards, handoff, receipt, minutes, specs | [`templates/`](templates/README.md) |
| One tool each — Azure DevOps, GitHub Projects, Notion, Slack, spreadsheet | [`tracks/`](tracks/README.md) |
| Who the agents are and what they may touch | [`agents/`](agents/README.md) |
| Prompts for any chat; how to bind a runtime | [`adapters/`](adapters/README.md) |
| Agency vs internal | [`profiles/`](profiles/README.md) |
| The gate and the kit's own checks | [`automation/`](automation/README.md) |
| Which topology, which tool, which profile | [`docs/scenarios/`](docs/scenarios/README.md) · [`docs/choose-your-track.md`](docs/choose-your-track.md) · [`docs/choose-your-profile.md`](docs/choose-your-profile.md) |
