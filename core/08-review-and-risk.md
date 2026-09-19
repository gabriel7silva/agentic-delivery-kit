---
id: RULE-REVIEW-RISK
canon: true
---

# Review gates and risk

The **Check** phase. A change leaves `Active` only through a review gate, and the gate's output is
two things at once: findings **and** a risk level. Risk is not classified *after* the review by a
separate step — it comes *out of* the review.

## The review gate — `RULE-REVIEW-GATE`

A gate is passed when all of the following hold:

1. **Deterministic verification** passed — whatever `verification_commands` in `instance.yml` say
   (lint, tests, build, a headless smoke). Machines first; they are cheaper than reviewers and they
   do not get tired.
2. **Every required reviewer** for the touched scopes (`agents/ownership.yml`) has returned a
   verdict. Reviewers run **in parallel** and **read-only** — see `RULE-SINGLE-WRITER`.
3. **No blocking finding** is open. A finding is blocking when the reviewer says so; "nit" and
   "optional" are not blocking, and the implementer may leave them for a later change.
4. **The risk level's requirements are met** — see below.

What a reviewer returns, always in this shape, so tooling can read it:

```
verdict: pass | pass-with-findings | block
risk: low | medium | high
findings:
  - severity: blocking | non-blocking
    where: <path or criterion>
    what: <one sentence>
```

## Risk — `RULE-RISK`

```
risk = MAX( highest reviewer verdict , floor of every touched path )
```

Two inputs, deliberately:

| Input | Protects against | Defined in |
|---|---|---|
| **Reviewer verdict** | A blind rule — a docs-only diff that a security reviewer flags as suspicious *goes up* | Each reviewer, per change |
| **Path floor** | An optimistic reviewer — a change under a sensitive path *cannot go below* its floor, whatever anyone says | `agents/policies/risk-floors.yml`, per instance |

Reviewers may **raise** risk. Nobody may lower it below the floor. The floor itself changes only by
a reviewed change to the policy file — an agent that edits the floor to pass its own change is
anti-pattern `AP-FLOOR-EDIT`.

## What each level requires — `RULE-RISK-GATES`

Defaults; instances override in `agents/policies/gates.yml`.

| Level | Required to reach `Resolved` | Required to reach `Closed` |
|---|---|---|
| **low** | Verification + one reviewer | PO acceptance |
| **medium** | Verification + all scope reviewers | PO acceptance |
| **high** | Verification + all scope reviewers + **a named human reviewer** before `Resolved` | Approver acceptance, in writing |

When `require_homologation_qa` is on, QA starts the homologation environment only **after**
this Check review has passed. `Closed` then needs the key-user test on that environment
**and** Transfer review of that evidence (`core/14-homologation.md`). That is not a sixth
risk level; it is the rest of the pipeline.

A `high` change therefore hits a human gate **twice**: once before the agent may even say it is
done, once at acceptance. That is the cost of touching what the floor says is sensitive, and it is
the reason floors should be narrow and honest rather than applied to everything.

## Sensible floors

Every instance is different, but the shape of a good floor list is the same: paths where a mistake
is **hard to reverse** or **crosses a trust boundary**.

| Floor `high` | Floor `low` |
|---|---|
| Code that reads or writes user data on disk or over the network | Documentation, changelogs, receipts |
| Permission manifests, content-security policy, capability declarations | Test files |
| Schemas of anything persisted or exchanged with a client | Diffs under ~100 lines inside one package |
| Anything an acceptance criterion of a product Story names | Generated files that are rebuilt by tooling |

Canon: RULE-REVIEW-RISK · RULE-REVIEW-GATE · RULE-RISK · RULE-RISK-GATES
