# Verification — what "works" means here

A repository that is mostly documentation needs an operational definition of *working*. This is
it. Everything below runs in `make check` and in the kit's own CI.

## Levels

| Level | Command | Passes when |
|---|---|---|
| **L0 — Leaks** | `make leaks` | No file carries a machine path, a real e-mail, a link to one specific board / issue / repository / workspace, a user handle, or a denylisted term. Extensionless text (`LICENSE`, `Makefile`, …) is included. Runs first; nothing else matters if it fails |
| **L1 — Structure** | `make links` | Every internal link and anchor resolves; no document under a content root is unreachable; every `RULE-…` cited is defined and every rule's canon file mentions it; **`core/` mentions no tool, vendor, runtime or profile**; the entry point `AGENTS.md` exists and every runtime pointer file points to it, names the interview and matches the generator (`make entry`) |
| **L2 — Data** | `make schemas`, `make mapping` | Every YAML validates; ids referenced across files exist; identical globs do not appear in two scopes (nested paths are allowed; most-specific wins); floors agree; every track maps 100 % of the thirty-five symbols; every `unsupported` has a substitute; no Resolved-category state shares a tool value with `Closed` in any track; the compatibility matrix on disk is current |
| **L3 — Behaviour** | `make test` | Pytest: each documented validator refusal has a case, plus a clean pass — not one test per canon rule; the model's categories, human-only states and default path hold. The walkthrough example passes the gate and fails when tampered with; sync diffs in memory and connectors refuse to run without a token |
| **L4** | — | Unused. The numbers stay so citations do not churn |
| **L5 — Anti-duplication** | `make canon`, `make adapters` | Every fenced copy is byte-equal to its fragment; every `{{source_of_truth.board}}` resolves in the example instance; no `canon: true` outside `core/`; every adapter's `out/` equals a fresh generation |
| **L6 — Adoption** | `make instance` | `instance.example.yml`, every `examples/instance-*.yml`, and every `profiles/*/instance.example.yml` validate, name an existing SoT-eligible track, toggle only optional rules, keep every lifecycle category when they run a subset of states, name a topology the roster agrees with, render an iteration name from a valid pattern with a product behind `{product}`, put the planning day and the sprint close on different working days, and point at existing policy and roster files |

## What passing means

- A reader can follow any link and land somewhere.
- A rule has one home, and everything that cites it agrees with it.
- A track that claims to support the method actually maps all of it, and says what it cannot do.
- The gate does what its documentation says, proven by tests you can read.
- The kit's own example survives the kit's own gate.
- Nothing about the kit's origin is in the kit.

## What is deliberately **not** verified

Written here so that a green build is never mistaken for more than it is.

| Not checked | Why | What covers it |
|---|---|---|
| Real tool APIs (Azure DevOps, GitHub, Notion, Slack) | No credentials in CI, by design; APIs change | Connectors are read / dry-run reference code; writes are stubs. Step 9 of every `setup.md` is a manual check |
| That the PR context matches the board | The copy-ready workflow reads a declaration in the PR body | A CI step you write builds `context.json` from the SoT |
| The five HITL triggers (except high risk) | Conditions live in `escalation.yml`; the gate only binds `risk == high` | Orchestrator or a thicker gate |
| The quality of a reviewer's judgement | The validator checks a verdict exists and has the right shape, not that it was wise | Retrospectives adjust briefs and floors — `core/ceremonies/retrospective.md` |
| That your runtime enforces read-only or single-writer | Runtimes differ; some enforce nothing | The PR validator, on the context it is given |
| That a runtime reads `AGENTS.md` | Some load it natively, some load their own rule file — the kit generates one per runtime it knows — and all of them read only the folder that was opened | The prompt pack, pasted by hand; the gate, which does not care who read what; `docs/onboarding/README.md` says where to open the kit |
| The onboarding interview's answers | They are what the adopter said; the kit cannot see their board | `make instance` on the file the agent wrote; step 9 of the track's `setup.md` against the real tool |
| That the copy-ready workflows run on *your* repository layout | Your paths differ from the example globs | `automation/ci/INSTALL.md` step 5: open a PR that must fail, and see it fail |
| Slack as a durable record | It is not one | Every decision is copied to the SoT; `tracks/slack/channels.md` |
| Prose quality, tone, translation | Not machine-checkable | Review |

## Running it

```bash
pip install -r automation/requirements.txt
make check
```

On Windows, if `make` is not on `PATH`: `.\check.ps1`.

About ten seconds. A failing level prints `path:line  rule  message` per finding, and the rule
name is the thing to search for in `core/` or `automation/scripts/`.

## The one human metric

Every release, someone who has never seen the kit runs [`quickstart-30min.md`](quickstart-30min.md)
and reports the time to their first accepted item. Target: thirty minutes. Above that, the
documentation is wrong somewhere, and no check above will find it.
