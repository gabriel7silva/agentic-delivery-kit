# The setup plan — what the agent produces

After the interview ([`interview.md`](interview.md)), the agent writes five files at the root of
the adopter's repository, in this order, and nothing else. Each is produced from a template in
the kit; none is invented. Then it stops and hands the plan to the person.

| # | File | From | What it must contain |
|---|---|---|---|
| 1 | `instance.yml` | [`instance.example.yml`](../../instance.example.yml) | Every answer from the interview: language, topology, profile, source of truth and mirrors, roles with kinds and titles, cadence (length, start day, sprint-close day, the iteration name pattern), the product, conventions, risk policy, optional rules, lifecycle. Must pass `check_instance.py` |
| 2 | `AGENT-CONTEXT.md` | [`templates/agent-context/AGENT-CONTEXT.md`](../../templates/agent-context/AGENT-CONTEXT.md) | Product paragraph, repository layout, verification commands, the rules that apply to every change, scopes and floors, language |
| 3 | `CURRENT-FOCUS.md` | [`templates/agent-context/CURRENT-FOCUS.md`](../../templates/agent-context/CURRENT-FOCUS.md) | The first iteration's name (from the pattern) and goal, the mandate when the PO is an agent, what is out of scope, open human gates. Dated and signed by role |
| 4 | `AGENTS.md` (+ pointers) | [`templates/agent-context/AGENTS.md`](../../templates/agent-context/AGENTS.md) | The adopter's own entry file: where the kit lives (`.pact/` or copied out), what to read first, the rules that bind every agent here. Pointer files for every runtime the kit knows — generated, never typed: `python3 <kit>/automation/scripts/entry_points.py --root . --kit .pact` (`--kit .` when the kit was copied out; `--list` names the runtimes) |
| 5 | `SETUP-PLAN.md` | the skeleton below | What was decided, what the person must do in their tools, what the agent could not decide, and the first item to run |

Files 1 to 4 are written in the instance language for prose and in English for keys and ids.
File 5 follows the writing standard ([`core/16-writing-standard.md`](../../core/16-writing-standard.md)):
short sections, tables, one rule in a box, honest placeholders where something is unknown.

## `SETUP-PLAN.md` — skeleton

```markdown
# 📌 Setup plan — <organization>

## 🔹 Decisions

| Decision | Value | Source |
|---|---|---|
| Topology | agent-to-human | answer |
| Profile | internal | default |
| Source of truth | <track> · board <name> | answer |
| Mirror | <track> · <channel> | answer |
| Lifecycle | 9 of 12 states — no homologation stage | answer |
| Cadence | 7 days · Planning Monday · sprint close Friday · `Sprint {seq:02} {yy} Q{quarter} {product}` | default |
| Language | pt-BR | answer |
| … | | |

## ✅ Done by me (files at your root)

- `instance.yml` — passes `check_instance.py`
- `AGENT-CONTEXT.md`, `CURRENT-FOCUS.md`, `AGENTS.md` + pointers

## 👉 Yours to do — in <tool>

Numbered from `tracks/<track>/setup.md`, with what each step needs from the decisions above.
1. Create the first iteration on the board, named `<iteration name>` — `automation/scripts/iteration_name.py --start <date>` prints it
2. …

## 🧠 Agents

| Role | Filled by | Brief |
|---|---|---|
| Orchestrator | <agent or person> | `adapters/prompt-pack/out/orchestrator.md` |
| … | | |

## ⚠️ Not decided — needs you

- [ ] unknown — <what> → <who decides>

## 🔁 First item

Walk one small item through by hand: `docs/quickstart-30min.md`. Then wire the gate:
`automation/ci/INSTALL.md`.

> 📌 Only a human sets Closed. Everything above configures the method; nothing above changes it.
```

## What the plan never does

- Create the board, project, fields, labels, channels or pipelines. Those steps are listed under
  *Yours to do*, straight from the track's `setup.md`.
- Put a person's name, an e-mail, a token or a private link in any file. Roles, not names.
- Get written before the interview ended. A Decisions table whose every *Source* is `default`
  is not a plan; it is `AP-SILENT-SETUP` — go back to Block 0.
- Touch `core/`, `agents/roster.yml` or a track. Scopes and floors are the two files an
  instance is expected to edit (`agents/ownership.yml`, `agents/policies/risk-floors.yml`), and
  the plan says so when they need editing.
