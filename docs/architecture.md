# Architecture

Why the kit is shaped the way it is. The decisions are recorded one per file in
[`decisions/`](decisions/0001-canon-blocks-instead-of-template-engine.md); this page is the map.

## Layers, and the arrow between them

```
core/        the method. One home per rule. Names no tool, vendor, runtime, profile.
  model/     the same method as YAML — the symbols machines check.
templates/   artifacts that leave the repo. Cite rules; never restate them.
tracks/      translation onto one tool each. Zero method.
agents/      roster, ownership, concurrency, risk policy. Neutral of runtime.
adapters/    the only place a runtime is bound. One-way generators.
profiles/    agency | internal overlays. Add and configure; never redefine.
automation/  the gate (validate_pr), the maintainer checks, copy-ready CI, sync.
```

The dependency arrow points **down** only. `core/` imports nothing. `tracks/` read `core/model/`.
`adapters/` read `agents/`. Nothing reads `instance.yml` except the optional renderer, the
instance check and the PR validator (for the optional-rule toggles). A grep in CI fails the build if `core/` mentions a tool, a vendor, a runtime or a
profile — the agnosticity is a test, not a claim.

## Four decisions that shape everything

### 1. Canon and fenced copies, not a template engine — [ADR 0001](decisions/0001-canon-blocks-instead-of-template-engine.md)

Every rule lives in one file and is cited by id. Blocks that must leave the repo inside a
template are copied inline between HTML-comment fences and byte-compared with their source by
`check_canon.py`. Instance values are readable `{{source_of_truth.board}}` placeholders. Result: the kit is
adoptable with **no build step**, and duplication is a CI failure instead of a slow divergence.

### 2. The neutral model is a YAML contract — [ADR 0002](decisions/0002-neutral-model-as-yaml-contract.md)

`core/model/` defines symbols, states, fields, gates, capabilities and rules as data. A track is
a `mapping.yml` that must cover 100 % of the symbols, plus a `capabilities.yml` answered honestly.
`rules.yml` says what each rule *requires*; crossing that with capabilities **generates** the
compatibility matrix. "Which rules need code review" is output, not opinion.

### 3. Adapters generate one way — [ADR 0003](decisions/0003-adapters-are-one-way-generators.md)

A runtime adapter reads the roster and writes its own `out/`, deterministically, never editing
upstream. Briefs are included verbatim. The prompt pack — no runtime at all — is the proof that
the roster is neutral. Drift between a brief and generated output is caught by regeneration in CI.

### 4. Single writer per scope, enforced by the gate — [ADR 0004](decisions/0004-single-writer-per-scope.md)

"N readers, one writer" is data in `agents/ownership.yml`. Claims live in the source of truth,
never in a repository file. The runtime may help; the PR validator is the guarantee. This is the
answer to *how do several agents work on one repository without colliding*, and it does not
depend on any runtime feature.

## What is verified, by level

| Level | Check | Catches |
|---|---|---|
| L0 | `check_leaks` | Traces of a private origin in any file |
| L1 | `check_links` | Broken links and anchors, orphans, unknown rule ids, a missing entry point or pointer, **core naming a tool** |
| L2 | `check_schemas`, `check_mapping` | Invalid YAML, missing ids, identical globs in two scopes, incomplete track coverage, stale matrix |
| L3 | `pytest` | Documented validator refusals, walkthrough, leaks/links/canon/instance/sync |
| L4 | — | Unused. The numbers stay so citations do not churn |
| L5 | `check_canon`, `make adapters` | Fenced copy drift, unresolved placeholders, canon outside `core/`, adapter output drift |
| L6 | `check_instance` | An instance naming a non-eligible SoT, toggling a mandatory rule, lowering a profile toggle, dropping a lifecycle category, a topology the roster contradicts, a name pattern with an unknown placeholder or `{product}` without a product, a weekend or same-day start and sprint close, or a missing profile |

`make check` runs them all. [`verification.md`](verification.md) says what "works" means for a
repository that is mostly documentation — and what is deliberately not checked.
