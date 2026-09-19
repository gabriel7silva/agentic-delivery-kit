# Automation

Two audiences, kept apart:

| For | What | Needs |
|---|---|---|
| **Adopters** who want the automated gate | `ci/` — copy-ready workflows that run the PR validator in GitHub Actions or Azure Pipelines | the kit vendored at `.pact/` in your repo (see [`ci/INSTALL.md`](ci/INSTALL.md)) |
| **Maintainers** of the kit | `scripts/check_*.py`, `tests/` — everything `make check` runs | `pip install -r requirements.txt` |

Adopters who want **no** automation skip this directory entirely. The method works on paper.

## The validator

`scripts/validate_pr.py` is the binding layer of the concurrency guarantee (`agents/README.md`). It
takes three tool-neutral inputs — the changed paths, a JSON context describing the item, and the PR
body (or explicit receipt and conclusion files) — and refuses the change when:

| Finding | Rule |
|---|---|
| A path falls in a scope the item has not claimed | `RULE-SCOPE` |
| A claimed scope is not in the handoff | `RULE-GOLDEN-SCOPE` |
| Another item holds an open claim on a touched scope | `RULE-CLAIM` |
| A required reviewer has not returned a verdict, or returned `block`, or left a blocking finding | `RULE-REVIEW-GATE` |
| `MAX(verdicts, floors)` disagrees with the item's risk field | `RULE-RISK` |
| Risk is `high` and no named human reviewed | `RULE-RISK-GATES` |
| Verification has not passed | `RULE-REVIEW-GATE` |
| An agent tries to set `Closed` | `RULE-STATE-RESOLVED-NOT-CLOSED` |
| No conclusion comment at all | `RULE-TRANSITION-BARRIER` |
| The conclusion comment lacks a field, or says `closed`, or has prose where evidence should be | `RULE-CONCLUSION-COMMENT`, `RULE-EVIDENCE` |
| The receipt lacks *Not verified / not claimed*, has no per-AC rows, or has a failing AC | `RULE-DOD` |
| `require_client_signoff` is on and `Closed` has no recorded client sign-off | `RULE-OPT-CLIENT-SIGNOFF` |
| `require_homologation_qa` is on and `Closed` has no feature branch, homologation URL, QA handoff, or key-user test | `RULE-OPT-HOMOLOG-QA` |
| A New-category state straight to a Resolved-category one (nothing was executed); `Closed` from outside the Resolved category; a state the model does not know | `RULE-STATES` |

Reviewer count and human-only transitions come from `agents/policies/gates.yml` and
`core/model/transitions.yml` (`lib/policy.py`). Low risk needs **one** reviewer from the
scope pool; medium and high need every reviewer on the touched scopes.

Where the context comes from is a track concern: the orchestrator posts a fenced
```` ```pact-context ```` JSON block, and optionally a CI step writes `board-snapshot.json`.
`scripts/build_context.py` overlays board fields on that declaration. The validator does not
call the board API. It **does** read `instance.yml` when present (or `--instance`) and the
defaults of the profile it names, so `require_homologation_qa` / `require_client_signoff`
cannot be skipped by omitting them from the context or from the instance. A green run with
`source: declared` is not proof of a claim on the item.

## Sync

`sync/` mirrors items between tracks (one writer, the source of truth; the rest read-only) and posts
events to Slack. Every connector runs `--dry-run` by default and needs a token from the environment
to do anything — [`sync/SECURITY.md`](sync/SECURITY.md). Details in [`sync/README.md`](sync/README.md). Nothing here runs in the kit's own CI against a live API.

## Scripts

| Script | Level | Checks |
|---|---|---|
| `check_leaks.py` | L0 | Origin traces — machine paths, e-mails, board links, handles, denylist. Structural rules always run. Literal names are optional: `PACT_DENYLIST` or a git-ignored `.leakcheck-denylist` copied from `.leakcheck-denylist.example`. The list file is not scanned, so it cannot fail against itself. |
| `check_links.py` | L1 | Links, anchors, orphans, rule ids, **core/ agnosticity**, the entry point and its pointers |
| `entry_points.py` | L1 | The pointer files for every runtime, from one template; `--check` refuses drift (`make entry`), `--root <dir> --kit .pact` writes them for an adopter |
| `check_schemas.py` | L2 | Every YAML against `schemas/`; ids that must exist; duplicate globs; floor agreement |
| `check_mapping.py` | L2 | 100 % symbol coverage per track; substitutes present; the compatibility matrix is current |
| `validate_pr.py` | L3 | The gate above; golden-tested in `tests/` |
| `build_context.py` | L3 | Overlay a board snapshot on a declared `pact-context`; writes `context.json` |
| `check_canon.py` | L5 | Fenced copies match fragments; placeholders resolve; canon only in `core/` |
| `check_instance.py` | L6 | An instance is complete and coherent with the tracks and profiles it names — lifecycle, topology, cadence and the iteration name pattern included |
| `render.py` | — | Optional: expand placeholders from an instance |
| `iteration_name.py` | — | Optional: print an iteration's name from the instance's pattern (`--start`, `--seq`, `--json`); derives the sequence for seven-day iterations |

All of them print one `PASS`/`FAIL` line and, on failure, `path:line  rule  message` per finding.
