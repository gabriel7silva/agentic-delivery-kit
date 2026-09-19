# Contributing

Three kinds of change, three sets of rules.

## Changing the method (`core/`)

- Every rule has **one** home. Before adding, search for an existing owner (`core/README.md` is the index).
- Anything that changes the meaning of a symbol in `core/model/` bumps `VERSION` (SemVer) and gets a
  `CHANGELOG.md` entry. Prose improvements do not.
- `core/` must never mention a tool, a vendor, a runtime or a profile. CI greps for it.
- Optional rules carry `optional: true` in `core/model/rules.yml`. Everything else is mandatory in
  every instance.

## Adding a track (`tracks/<name>/`)

Read `tracks/_contract/track-contract.md`. In short: a `mapping.yml` covering **100 %** of neutral
symbols, a `capabilities.yml`, a `README.md`, `fields.md`, `setup.md`, and — for every capability
the tool lacks — a `substitutes.md`. `make mapping` tells you what is missing.

## Adding a runtime adapter (`adapters/<name>/`)

Read `adapters/_contract/adapter-spec.md`. An adapter is a pure, one-way generator: it reads
`agents/` and its own `mapping.yml`, writes `out/`, and never edits anything upstream. Copy
`adapters/_template/` to start.

## Changing the lifecycle

- The five categories are fixed. A rule, a gate or a track speaks in categories, never in states.
- A state is data in `core/model/item-states.yml`: id, name, category, who sets it. Adding one is a
  minor bump; every track's `mapping.yml` must map it (`make mapping`), and the example instances
  must still pass `make instance`.

## The entry point and its pointers

`AGENTS.md` holds the instructions an agent follows in this repository. Every other runtime file —
`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/pact.mdc`, `.github/copilot-instructions.md`,
`.windsurf/rules/pact.md` and the rest — is a **pointer**, generated from one template by
`automation/scripts/entry_points.py`. Edit the generator, never a pointer: `make entry` refuses a
pointer that drifted, `python3 automation/scripts/entry_points.py` rewrites them all. A new runtime
is one line in `automation/scripts/lib/entry_points.py`. A pointer says two things and nothing
else: read `AGENTS.md`, and a setup starts with the interview — a rule that lives only in a pointer
is a rule one runtime sees and the others do not.

## Before you open a pull request

```bash
make check
```

On Windows, if `make` is not on `PATH`:

```powershell
.\check.ps1
```

That is what CI runs. If `make leaks` (or the L0 step in `check.ps1`) fails, fix it first — nothing downstream matters until it passes.

Literal origin names are optional and stay out of git: copy `.leakcheck-denylist.example` to `.leakcheck-denylist` and add terms, or set `PACT_DENYLIST`. CI reads the same list from the `PACT_DENYLIST` repository secret. An empty secret is structural rules only.

## Publishing

This kit does not ship a `git remote`. Add one when you publish to an **organization**, never a personal account, and keep personal names out of badges and URLs (`L0` will refuse `github.com/<owner>/<repo>` that is not `example-org` / `your-org`).

`check_leaks` reads files, not git metadata. A commit that still carries a personal mailbox is a leak in the history even when L0 is green. Use a project identity (`user@example.com` is the placeholder) before the first public push — rewriting history after a push is a different decision.

## Language

English throughout, including comments, commit messages and YAML keys.
