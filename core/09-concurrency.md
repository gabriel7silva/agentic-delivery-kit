---
id: RULE-CONCURRENCY
canon: true
---

# Concurrency: N readers, one writer

Running several agents at once is the whole point of a factory. Running them **into each other** is
the fastest way to lose a day. This file is the difference.

## The rule — `RULE-SINGLE-WRITER`

| | Allowed | Forbidden |
|---|---|---|
| **Reading** | Any number of agents may read the same files at the same time — reviewers run in parallel by design | — |
| **Writing** | **Exactly one** agent writes to a given *scope* at a time | Two agents editing the same tree; an "implementation swarm"; a reviewer that edits |

Parallelism on the read side is cheap and safe. Parallelism on the write side produces merge
conflicts, half-applied refactors, and — worse — two agents each convinced they finished. The rule
replaces the older "only ever run one agent" advice while keeping its reason.

## Scopes — `RULE-SCOPE`

A **scope** is a named set of path globs with a declared writer and required reviewers, in
`agents/ownership.yml`:

```yaml
scopes:
  - id: api
    paths: ["services/api/**"]
    writer: implementer
    reviewers: [reviewer-correctness, reviewer-security]
    floor: high
```

Identical globs may not appear in two scopes — that is a configuration error the schema check
rejects. Nested paths are allowed: a more specific glob wins (`src/storage/**` beats `src/**`).
A path that matches no scope belongs to a default scope with the most conservative floor.

## Claims — `RULE-CLAIM`

Before an agent writes to a scope it **claims** it. The claim is recorded **in the source of truth**
— a field or label on the work item — never in a file in the repository. A claim in a file is itself
something two agents would race to edit; the mechanism against conflict must not be a source of it.

| Property | Rule |
|---|---|
| Cardinality | One open claim per scope |
| Lifetime | A claim has a TTL (`agents/concurrency.yml`, default 4 h). Expired claims are released by the orchestrator, with a comment |
| Release | On `Resolved`, on rejection, or explicitly by the holder |
| Visibility | The handoff names the scopes the agent may claim; claiming outside the handoff is out of scope |

## When a conflict happens anyway — `RULE-ARBITRATION`

1. The **earlier claim wins**. The later agent stops, releases nothing (it holds nothing), and posts
   an `Issue` linking both items.
2. The orchestrator decides whether the later item waits or is re-scoped. It does not merge the two.
3. If both items are genuinely on the same lines, one of them was refined wrong — it goes back to
   the PO with `decision: split` or `decision: defer`.

## Enforcement

The runtime you use may or may not enforce any of this. **The PR validator does**, on the
context it is given: touched paths outside the claimed scope, a second open claim on the same
scope, or a missing required reviewer all fail the gate. Treat the runtime as a convenience and
the validator as the guarantee of that declaration.

Canon: RULE-CONCURRENCY · RULE-SINGLE-WRITER · RULE-SCOPE · RULE-CLAIM · RULE-ARBITRATION
