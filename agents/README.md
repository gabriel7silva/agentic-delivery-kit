# Agents — organised, and unable to collide

Everything needed to run several agents on one repository without them writing over each other.
Nothing here names a runtime or a vendor; `adapters/` turns these files into whatever your runtime
expects.

## Three files, one guarantee

| File | Says | Enforced by |
|---|---|---|
| `roster.yml` | Which agents exist, what each consumes and produces, which gate each serves | schema; adapters generate from it |
| `ownership.yml` | Which paths form a **scope**, who may **write** to each, who must **review** each, and the risk **floor** | the PR validator, on every change |
| `concurrency.yml` | How long a claim lives, that there is one per scope, who arbitrates a collision | the PR validator + the orchestrator |

Plus `policies/`: the risk floors (`risk-floors.yml`), what each risk level demands
(`gates.yml`), and the human-in-the-loop triggers as conditions (`escalation.yml`). The PR
validator binds `risk == high`. The five HITL triggers are for the orchestrator and for humans
unless they show up as that high-risk gate.

## The guarantee has two layers, on purpose

**Layer 1 — the runtime (advisory).** Your agent runtime may support sub-agents, parallel
reviewers, file locks. `adapters/` maps the roster onto that. Helpful; not trusted.

**Layer 2 — the PR validator (binding on its inputs).** `automation/scripts/validate_pr.py` reads
the diff and a context JSON (from a `pact-context` block or a file you supply). It does **not**
read the board. It refuses the change when a path is outside the claimed scope, when another claim
is open on the same scope, when a required reviewer is missing, when risk demands a human gate
that is absent, or when the conclusion comment or receipt is incomplete. A green run proves the
declaration it was given. It does not care which runtime produced the change.

The rule "N readers, one writer" (`core/09-concurrency.md`) is therefore **data** in
`ownership.yml`, not advice in a prompt.

## Briefs

`briefs/` holds one prose brief per agent in the roster — [orchestrator](briefs/orchestrator.md),
[implementer](briefs/implementer.md), [reviewer · correctness](briefs/reviewer-correctness.md),
[reviewer · security](briefs/reviewer-security.md), [reviewer · docs](briefs/reviewer-docs.md),
[reviewer · delivery compliance](briefs/reviewer-delivery-compliance.md): role, inputs, what to do, what never to
do, the shape of its output, when to stop. They are written for a reader with no context and no
runtime — a person could follow them. Adapters copy them verbatim into runtime-specific files;
they never rewrite them.

One agent in the roster is an **advisor** rather than a worker: [`po-assistant`](briefs/po-assistant.md)
guides people on the method — ceremonies, the PO's role, items, states — and turns a raw request
into a refined specification. It never claims a scope and never sets a state; its prompt is the
one to paste into any chat when the PO wants a guide beside them.

When `require_homologation_qa` is on, two **human** briefs apply and are not in the roster:
[QA](briefs/qa.md) starts the homologation environment and links branch + URL;
[key user](briefs/key-user.md) **tests** on that environment and writes the update for the PO.

## Changing any of this

A change to `ownership.yml` or `policies/risk-floors.yml` is itself a change under a `high`
floor: it goes through the review gate with a named human. An agent editing the floor to pass its
own change is `AP-FLOOR-EDIT`, and the validator treats a diff that touches these files as `high`
regardless of what else it touches.
