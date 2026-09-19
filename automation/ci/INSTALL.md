# Installing the gate in your repository

The workflows expect the kit at **`.pact/`** in your repository, so the scripts find their own
`agents/`, `core/model/` and `schemas/` relative to themselves and your paths (`src/**`, `docs/**`)
match the globs in `.pact/agents/ownership.yml` as you edit them.

## 1. Vendor the kit

Either:

```bash
git subtree add --prefix .pact <kit-remote> main --squash     # updates: git subtree pull …
```

or:

```bash
git submodule add <kit-remote> .pact
```

Subtree keeps your repo self-contained; submodule keeps the kit's history separate. Both work.

## 2. Make the policy yours

Edit, inside `.pact/`:

- `agents/ownership.yml` — your scopes, your paths, your reviewers.
- `agents/policies/risk-floors.yml` — your floors, with a `why` per line.
- Copy `instance.example.yml` to `instance.yml` at **your** repository root and fill it in.

## 3. Copy a workflow

| Host | Copy | To |
|---|---|---|
| GitHub | `.pact/automation/ci/github-actions/delivery-guard.yml` | `.github/workflows/` |
| GitHub | `.pact/automation/ci/github-actions/docs-lint.yml` | `.github/workflows/` |
| Azure DevOps | `.pact/automation/ci/azure-pipelines/azure-pipelines.yml` | repository root (or merge into yours) |

Then make the guard a **required check** — a branch ruleset on GitHub, build validation in a branch
policy on Azure DevOps (`tracks/azure-devops/policies.md`).

## 4. Give the guard its context

The validator needs to know the item, its claims and the reviewer verdicts. Two ways:

**In the PR body** — the orchestrator (or a person) pastes a fenced block:

````markdown
```pact-context
{
  "item": {"id": "WI-42", "type": "STORY", "wi_state": "ACTIVE", "risk": "low"},
  "actor_role": "implementer",
  "target_state": "RESOLVED",
  "handoff_scopes": ["app"],
  "claims": {"this_item": ["app"], "open_elsewhere": {}},
  "verification": {"passed": true},
  "verdicts": [{"reviewer": "reviewer-correctness", "verdict": "pass", "risk": "low", "findings": []}],
  "human_review": {"present": false}
}
```
````

**From the tool** — a step **you write** queries the source of truth and writes `context.json`.
The workflows call `validate_pr.py --context context.json` when that file exists. The sync
connectors in `.pact/automation/sync/` are read / dry-run reference code; they do **not**
populate `context.json` for you.

Until that step exists, a passing guard proves the context the author pasted, not the board.

The receipt and the conclusion comment are read from the PR body under `## Receipt` and
`## Conclusion`, or from files via `--receipt` / `--conclusion`. The method still wants those
six fields **on the work item**; the guard only sees the PR body.

## 5. Try it

Open a pull request that touches a path in one scope with a context that claims a *different*
scope. The guard must fail with `RULE-SCOPE`. If it passes, the paths in `ownership.yml` do not
match your layout.
