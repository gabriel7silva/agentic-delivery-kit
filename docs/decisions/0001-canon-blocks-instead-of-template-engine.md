# ADR 0001 — Canon and fenced copies instead of a template engine

**Status:** accepted · **Applies to:** `core/`, `templates/`, `automation/scripts/check_canon.py`

## Context

The source material had the same content copied many times — the roles table in five places, the
state model in six, the instance footer in more. Generalising it without addressing that would
multiply the divergence. Two kinds of duplication were present, and they need different answers:

- **Normative** content (rules, tables) that stays inside the repository.
- **Repeated blocks** that must **leave** the repository — a footer inside a template pasted into
  a work item cannot link back.

## Options

1. A template engine (Jinja or similar) with a required build step.
2. A `variables.yml` and a mandatory render script.
3. Front-matter includes.
4. **Canon by id + fenced inline copies verified by a linter + readable placeholders.**

## Decision

Option 4.

- A rule has exactly one home in `core/` and is cited elsewhere as `Canon: RULE-…`. The linter
  fails on a cited id that does not exist and on canon front-matter outside `core/`.
- A block that must leave the repo has one source in `templates/_fragments/` and appears in
  templates as an inline copy between `<!-- canon:begin fragment=x -->` / `<!-- canon:end -->`.
  `check_canon.py` compares each copy byte-for-byte; `--fix` rewrites them.
- Instance values are `{{source_of_truth.board}}` placeholders, readable unrendered. `render.py` is optional.

## Consequences

- **Zero build to adopt.** A PO can paste a template into a card today.
- Duplication becomes a **CI failure**, not a slow drift.
- Templates carry a few HTML comments that render as nothing.
- Options 1–3 were rejected because each makes the repository unreadable on GitHub without a
  build, or handles only one of the two duplication kinds.
