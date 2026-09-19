# ADR 0004 — Single writer per scope, enforced by the gate, claims in the source of truth

**Status:** accepted · **Applies to:** `core/09-concurrency.md`, `agents/ownership.yml`, `agents/concurrency.yml`, `automation/scripts/validate_pr.py`

## Context

The explicit requirement was *organised sub-agents that do not collide*. The prior policy was
"one agent, self-review only" — safe, but it forbade the parallel review that makes a factory
worth having. And any rule that depends on the model obeying a prompt is not a guarantee.

## Options

1. Keep one agent at a time.
2. Rely on the runtime's locking or sub-agent features.
3. **Parallel readers, one writer per scope; claims recorded in the source of truth; the PR
   validator as the binding check.**

## Decision

Option 3.

- **Reading is parallel and safe.** Reviewers are read-only by schema and run at the same time.
- **Writing is exclusive per scope.** `agents/ownership.yml` maps path globs to one writer and its
  required reviewers. The same glob must not appear in two scopes (a schema-check failure).
  Nested paths are allowed; the most-specific glob wins (`src/storage/**` beats `src/**`).
- **A claim lives in the source of truth** — a field or label on the work item — never in a
  repository file. A claim in a file is something two agents would race to edit; the anti-conflict
  mechanism must not be a conflict point.
- **The PR validator enforces it.** It refuses a change whose paths fall outside the claimed
  scope, a second open claim on the same scope, a missing required reviewer, and the rest of the
  gate. It does not know which runtime produced the change.
- The runtime may add enforcement (locks, tool allowlists). It is welcome and it is **advisory**;
  each adapter says which it provides.

## Consequences

- Several agents can work one repository at once, on disjoint scopes, with parallel review — and
  the guarantee holds even on a runtime that enforces nothing.
- Editing `ownership.yml` or the floors is itself a high-risk change, gated by a named human,
  so an agent cannot widen its own scope to pass.
- Option 1 was rejected as too slow; option 2 because it would tie the method to a runtime and
  break the agnosticity the whole kit rests on.
