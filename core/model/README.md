# Model — the method as data

Everything in `core/*.md` says a rule in prose. Everything here says the **same** rule as YAML, so
that a script can check it. Prose is for people and explains *why*; YAML is for machines and defines
the *symbols*. When they disagree, the prose is wrong or the YAML is wrong — never "both are fine".

## Files

| File | Defines | Consumed by |
|---|---|---|
| `item-types.yml` | The six work-item types and the hierarchy between them | tracks, mapping, schemas |
| `item-states.yml` | The five lifecycle **categories** and the twelve default WI-States, each with its category and who may set it | tracks, mapping, schemas, validator (state → category), sync |
| `transitions.yml` | Allowed transitions **between categories** and the evidence each requires; the free moves inside a category; what specific states need on entry | mapping, schemas. The PR validator reimplements a subset (human-only `Closed`; `Closed` only from Resolved; no New → Resolved) |
| `board-columns.yml` | Default board columns and the WI-State → column translation | tracks |
| `iterations.yml` | The iteration entity, its name pattern and the cadence parameters | tracks, instance check, `iteration_name.py` |
| `fields.yml` | Every field the method needs on a work item, with type and the rule that needs it | tracks, instance check |
| `review-gates.yml` | Gate types and the evidence types they accept | mapping, schemas, policies |
| `capabilities.yml` | The vocabulary a track uses to say what its tool can and cannot do | tracks, matrix |
| `rules.yml` | Every `RULE-…` id, its canon file, the capabilities it requires, whether it is optional | matrix, instance check |

The PR validator loads `item-states.yml` only to map a state id to its category. It hard-codes the
subset it enforces (human roles for `Closed`, `Closed` only from a Resolved-category state, no
New → Resolved, scope/claim/review/risk/receipt). Mapping and schema checks are what consume the
contract as data. When they disagree, that is a bug — say so; do not claim the gate "runs the
model".

## Symbols

A **symbol** is anything a track must translate. `automation/scripts/check_mapping.py` collects them
from the first six files above and requires every `tracks/<name>/mapping.yml` to cover **all** of
them. Symbols are `UPPER_SNAKE` and stable: renaming one is a breaking change to the contract and
bumps `VERSION`.

Symbol groups:

- **entities** — `ITEM`, `ITEM_PARENT`, `ITERATION`, `CLAIM`, `REVIEW_GATE`, `CHANGE_REQUEST`,
  `EVIDENCE_LINK`, `CONCLUSION_COMMENT`, `CEREMONY_MINUTES`, `DIGEST`
- **item_types** — from `item-types.yml`
- **item_states** — from `item-states.yml`
- **board_columns** — from `board-columns.yml`
- **fields** — from `fields.yml`

## What this directory never contains

A tool name, a vendor name, a runtime name, a profile name. The same grep that guards `core/*.md`
guards this directory. If a symbol only makes sense for one tool, it is not a symbol — it is that
track's business, in `tracks/<name>/`.
