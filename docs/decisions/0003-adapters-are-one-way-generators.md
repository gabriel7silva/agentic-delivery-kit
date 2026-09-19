# ADR 0003 — Adapters are one-way generators

**Status:** accepted · **Applies to:** `adapters/`, `agents/`

## Context

The method must not depend on any AI runtime, yet every runtime wants agent definitions in its
own shape. The source material was written for one runtime and named it throughout.

## Decision

- `agents/` is the **neutral** layer: a roster (id, kind, purpose, inputs, outputs, gate served),
  briefs in prose, ownership, concurrency, policies. No runtime or vendor name appears there;
  `check_links.py` extends the same agnosticity grep it applies to `core/`.
- An adapter is a directory under `adapters/` with a `generate.py` that **reads** `agents/` and
  **writes** its own `out/`. It includes each brief **verbatim**. It is deterministic. It never
  edits upstream. `out/` is committed and `--check` fails CI on drift.
- Each adapter's `mapping.yml` states, per concept, whether the runtime **enforces**, **advises**
  or **does not support** it, and what stands in when it does not — always the PR validator.
- The **prompt pack** ships as the reference adapter: one prompt per agent, usable in any chat.
  If the roster works with no runtime feature, it is neutral.
- No vendor-specific adapter ships in the kit. `_template/` makes contributing one a single
  directory.

## Consequences

- A change to a brief that is not regenerated is a CI failure.
- The method's guarantees never rest on a runtime feature; runtimes only add convenience.
- Adopters of a runtime without an adapter still have the prompt pack on day one.
