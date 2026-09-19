# ADR 0002 — The neutral model is a YAML contract, not prose

**Status:** accepted · **Applies to:** `core/model/`, `tracks/`, `schemas/`, `check_mapping.py`

## Context

Four tools with different vocabularies had to carry one method. Describing each translation in
prose would leave "does this track support rule X" as a matter of opinion, and would let a track
quietly omit a concept.

## Decision

- `core/model/*.yml` defines the **symbols** (entities, item types, states, columns, fields),
  the **gates** and evidence types, a **capability** vocabulary, and `rules.yml` — every rule id
  with the capabilities it requires and whether it is optional.
- A track is a `mapping.yml` that must cover **100 %** of the symbols, resolving each to
  `native`, `custom` or `unsupported` — and every `unsupported` **must** declare a substitute with
  mechanism, evidence and loss. Plus a `capabilities.yml` with a boolean per capability.
- `check_mapping.py` crosses `rules.yml` × each track's capabilities and **generates**
  `docs/compatibility-matrix.md`. The matrix on disk must equal the generated one or CI fails.
- Semantic guards the schema cannot express live in the check: `sot_eligible` requires
  `durable_history` and `comments`; `RESOLVED` may never map to the same value as `CLOSED`.

## Consequences

- "Which rules need code review" is **output** of the data, not a paragraph someone wrote.
- A new track is a directory that passes `make mapping`; nothing in `core/` changes.
- Renaming a symbol is a **breaking change** to the contract and bumps `VERSION` major.
- Prose in `tracks/` explains *how*; it may not restate *what* — the YAML is the contract.
