# Core — the PACT method

Everything in this directory is **canon**: each rule lives in exactly one file and everything else in
the kit points to it by id (`Canon: RULE-…`). Nothing here names a tool, a vendor, a runtime or a
profile. A CI check fails the build if that ever changes.

## Reading order

| # | File | Owns | Read when |
|---|---|---|---|
| 01 | [roles.md](01-roles.md) | Who does what — five roles, by function | first day |
| 02 | [golden-rules.md](02-golden-rules.md) | The five rules that everything else derives from | first day |
| 03 | [human-in-the-loop.md](03-human-in-the-loop.md) | The five triggers that force a human decision | first day |
| 04 | [work-item-model.md](04-work-item-model.md) | Epic → Feature → Story → Task; the two state axes | setting up a board |
| 05 | [states.md](05-states.md) | Five fixed categories, twelve default states; PACT phases; `Resolved ≠ Closed` | setting up a board |
| 06 | [ready-and-done.md](06-ready-and-done.md) | Definition of Ready, Definition of Done | writing the first card |
| 07 | [evidence.md](07-evidence.md) | The conclusion comment and the transition barrier | closing the first item |
| 08 | [review-and-risk.md](08-review-and-risk.md) | Review gates; `risk = MAX(verdict, floor)` | wiring the Check phase |
| 09 | [concurrency.md](09-concurrency.md) | N readers, one writer; scopes; claims | running more than one agent |
| 10 | [merge-rituals.md](10-merge-rituals.md) | What may merge, under which conditions, by change type | wiring the Check phase |
| 11 | [docs-in-the-code.md](11-docs-in-the-code.md) | Agent context vs audit trail — where each document lives | setting up a repository |
| 12 | [anti-patterns.md](12-anti-patterns.md) | What fails, why, and what to prefer | when something feels off |
| 13 | [not-in-this-factory.md](13-not-in-this-factory.md) | What this method deliberately does not cover | before adopting |
| 14 | [homologation.md](14-homologation.md) | QA starts the env and links branch + URL; the key user tests there and updates the PO | when `require_homologation_qa` is on |
| 15 | [topologies.md](15-topologies.md) | Who fills each role — people or agents — and how agents coordinate through the source of truth | before the first item; when adding agents |
| 16 | [writing-standard.md](16-writing-standard.md) | The one shape every answer, spec, handoff and report takes; ten icons with fixed meaning; what a machine parses stays exact | writing anything a person reads |
| — | [ceremonies/](ceremonies/README.md) | Planning, daily sync, the sprint close (review, retrospective, refinement in one session), iteration naming, participation by topology | running an iteration |
| — | [model/](model/README.md) | The same method as YAML, for machines | building tooling |

## How canon is referenced

A rule id looks like `RULE-STATE-RESOLVED-NOT-CLOSED`. Templates, tracks and profiles cite it on a
line of the form:

```
Canon: RULE-STATE-RESOLVED-NOT-CLOSED
```

They never restate the rule. If you find the same table in two places, one of them is wrong — see
`CONTRIBUTING.md`.

## The one-sentence version

The PO defines the *what* and the *why*; agents execute the *how*; a human accepts the value — and
every step leaves evidence on the work item.
