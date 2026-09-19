---
id: RULE-HONESTY
canon: true
---

# Not in this factory

Adopting a process whose gaps are written down beats adopting one that pretends to have none. This
file is the method's own **honest placeholder** (`RULE-GOLDEN-NO-INVENTION`, applied to itself).

## What PACT does not cover

| Area | Why not | What to do instead |
|---|---|---|
| **Production monitoring** — an agent watching graphs, signals and alerts | Requires observability infrastructure the method cannot assume. A desktop tool, a library, an internal script have none | If you have it, the *Transfer* phase is where a post-release observation window belongs. Add it as an optional rule in your instance |
| **Performance regression detection** | Needs load, an SLO and a baseline. Most teams adopting this have none of the three yet | Add a performance verification command when a baseline exists; until then it is `unknown` |
| **Incident response** | An incident bot needs a production to have incidents in | Out of scope. An incident is an `Issue` with the highest priority; the method's job ends at making that visible |
| **Progressive rollout / feature flags** | A deployment concern, not a delivery-process concern | *Transfer* records that a human released. How the release is staged is your platform's business |
| **Estimation** | Deliberately optional. The unit of sizing is "fits one handoff" (`RULE-DOR-DOD`); no gate reads a number | Teams that plan by capacity turn on `track_sprint_metrics` (`RULE-OPT-SPRINT-METRICS`): effort, remaining work and business value live on the board fields and in the planning minutes, never in a gate. Dates come from iteration reports |
| **Judging reviewer quality** | The method checks that a reviewer ran and returned a verdict, not that the verdict was wise | Retrospectives adjust reviewer briefs and floors. That is the feedback loop |

## What the kit does not verify

Written down in `docs/verification.md`, and repeated here so it is not missed:

- It does not call real tool APIs in CI. Track mappings are checked against the YAML, not a live board.
- It does not guarantee anything about a chat tool as a durable record. That is by design
  (`AP-CHANNEL-AS-SOT`).
- It does not ensure your runtime enforces single-writer. The PR validator checks the context it
  is given; the runtime is a convenience.

## What the gate still does not check

| Hole | What happens today | What would close it |
|---|---|---|
| Context is self-declared | Copy-ready CI reads `pact-context` from the PR body | A job that builds `context.json` from the source of truth |
| Five HITL triggers | Only `risk == high` is refused | Orchestrator evaluates `escalation.yml`, or the gate grows those conditions |
| Optional instance rules | `require_client_signoff` and `require_homologation_qa` are on when the context, `instance.yml`, **or** the profile it names sets them true; changelog and iteration-report are not | Carry those two remaining toggles on the context too |
| Sync writes | `--apply` writes only `.state/`; connectors print and do not send HTTP | Implement a separate `--post` if a team wants a live notification, or keep print-only |
| Conclusion on the item | The gate parses the PR body | Orchestrator copies the comment to the work item and the context confirms it |
| Branch and dates on the board | Creating an item leaves `BRANCH`, `CHANGE_LINK`, `START_DATE` and `TARGET_DATE` empty | Humans and agents write the **tool fields** (see each track's `fields.md`). Sync does not fill them |
| The interview is self-declared | An agent writes the instance from what a person answers; nothing compares those answers with the real board | `make instance` checks the file; step 9 of the track's setup guide is the manual check against the tool |
| The board is not created | The kit writes the instance and the context files; columns, fields and views are made by hand from the track's setup guide | A provisioning script per track would close it; none ships |
| The entry file is advice | `AGENTS.md` and its pointers tell an agent what to do; a runtime may ignore them | The gate, which reads the context whoever produced it |

## How to use this file

Before adopting, read the first table and ask which rows your context **needs**. If you need
production monitoring, PACT alone is not enough — pair it with a platform practice. Write that
pairing in your instance's `AGENT-CONTEXT.md` so the agents know the boundary too.

When you find a gap that is not listed here, add it here **before** working around it. A gap that
is written down is a known limit; a gap that is worked around silently becomes an invented process.

Canon: RULE-HONESTY
