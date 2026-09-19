---
id: RULE-STATES
canon: true
---

# States and the PACT phases

Two levels, on purpose. **Five categories** carry the method: every rule, every gate and every
track speaks in them, and they never change. **Twelve default states** carry the board: what a
team sees from day to day, what a tool stores, what an instance may rename or drop.

```
 NEW                              ACTIVE                RESOLVED                                        CLOSED
 ┌──────────────────────────┐    ┌─────────────────┐    ┌────────────────────────────────────────────┐  ┌────────┐
 │ New                      │    │ In development  │    │ Awaiting test                              │  │ Closed │
 │  → In analysis           │ ─► │   ⇄ Blocked     │ ─► │  → Prepare homologation                    │─►│        │
 │  → Awaiting development  │    │                 │    │  → Key-user homologation                   │  │ human  │
 └──────────────────────────┘    └────────▲────────┘    │  → Prepare release → Integration test      │  │ only   │
                                          │             └──────────────────┬─────────────────────────┘  └────────┘
                                          └── rejected: back with one objective note ─┘
 NEW or ACTIVE ──► Removed   (a human; never counts as delivered)
```

## The five categories — `RULE-STATE-CATEGORIES`

| Category | PACT phase | Meaning | Who may enter it |
|---|---|---|---|
| **New** | Plan | Registered; no agent has started | PO, orchestrator |
| **Active** | Act | Pulled; an agent (or a chain) is executing; evidence accrues on the item | Orchestrator; the Approver or PO on rejection |
| **Resolved** | Check | The agent's part is done and evidenced; **people** are validating it | Implementer or orchestrator, after the review gate |
| **Closed** | Transfer | Accepted; counts as delivered | **A human**, always |
| **Removed** | — | Discarded; never counts as delivered | PO |

The categories are the contract:

- Every rule in this method is written against a category. `Resolved ≠ Closed`, the transition
  barrier, the review gate, the human gate — none of them care which of the twelve states an item
  sits in, only which category.
- The PR validator normalises a state id to its category before it checks. A context may name a
  state (`AWAITING_TEST`) or a category (`RESOLVED`); both mean the same to the gate.
- A track maps **every** state (`tracks/<name>/mapping.yml`); a tool that groups its states in
  categories of its own maps each one into the matching group.
- An instance may run **fewer** states, and may label them in its own language
  (`instance.yml` → `lifecycle`). It may never drop a category: at least one state per category,
  always; `Closed` and `Removed` stay human-only whatever they are called.

## The twelve default states

| State | Category | Meaning with agents | Entered by | Left by |
|---|---|---|---|---|
| **New** | New | In the backlog; nobody has looked at it | Creation | Refinement starts |
| **In analysis** | New | Being refined — value, criteria and limits written; DoR not met yet | PO | DoR met |
| **Awaiting development** | New | DoR met; may be pulled — the *Ready* column | PO, orchestrator | Orchestrator pulls it, writes the handoff and the claim |
| **In development** | Active | An implementer holds the claim and works inside it; verification and reviewers run before it leaves | Orchestrator | Implementer posts the conclusion comment, the review gate passes |
| **Blocked** | Active | Pulled, but cannot proceed; an `Issue` names the impediment | Orchestrator, implementer | The Issue is resolved |
| **Awaiting test** | Resolved | Verification and reviewers passed; the change is done and evidenced; a person tests it | Implementer, orchestrator | A person tested; or QA takes it into homologation |
| **Prepare homologation** | Resolved | QA starts the homologation environment for this branch and links it (`core/14-homologation.md`) | QA | `BRANCH` and `HOMOLOG_LINK` on the board, environment up |
| **Key-user homologation** | Resolved | The key user tests on that environment and writes the result on the item | QA | The key-user update is on the item |
| **Prepare release** | Resolved | Transfer review accepted the evidence; the release is prepared — external publication is a human gate (`RULE-HITL`) | Approver, PO | Released to the integration environment |
| **Integration test** | Resolved | The last check before a human accepts the value | QA, orchestrator | Approver accepts (→ `Closed`) or rejects (→ `In development`) |
| **Closed** | Closed | Accepted; counts as delivered | **A human** | — |
| **Removed** | Removed | Cancelled, duplicate, invalid; never counts as delivered | PO | — |

Rejection from any Resolved-category state lands on `In development`. At the sprint close an
unfinished Active-category item may be **returned** to the backlog (`RULE-CARRY-OVER`): its claim
released, its state back to `Awaiting development` or `In analysis` — the one move from Active to
New, and a human's or the orchestrator's decision, never an implementer's. The default order is
`core/model/item-states.yml` → `default_path`; `Blocked` sits beside `In development` rather than
on the path. A team that needs none of the homologation stage simply does not run those states
(the internal example instance under `examples/` does exactly that).

## PACT phases map onto categories — `RULE-PACT-PHASES`

| Phase | Category entered | What the phase produces |
|---|---|---|
| **Plan** | `New` (through *Awaiting development*) | A card that passes the Definition of Ready; a handoff |
| **Act** | `Active` | A claim on a scope; the change itself |
| **Check** | `Resolved` | Passing verification; reviewer findings and a risk verdict; a receipt; then the human tests that follow |
| **Transfer** | `Closed` | A human's acceptance recorded on the item |

The phase names are for people. The categories are what the rules read. The states are what tools
store. All three say the same thing.

## Trace dates and the change — `RULE-GOLDEN-TRACE`

These fields are how a later reader finds the work without opening comments:

| Field | Who writes it | When |
|---|---|---|
| `TARGET_DATE` | PO / Planning | Before the item may become *Awaiting development* |
| `START_DATE` | Orchestrator | The moment the item enters `In development` |
| `BRANCH` | Implementer | The moment the feature branch exists — on the **board field**, never the default branch |
| `CHANGE_LINK` | Implementer | The moment the pull request exists |
| `HOMOLOG_LINK` | QA | The moment the homologation environment for this branch is up — when `require_homologation_qa` is on. The key user tests there |

Writing them only in a template table or a receipt, and not on the tool fields the track maps,
leaves the board empty. That is a defect of the card.

## `Resolved ≠ Closed` — `RULE-STATE-RESOLVED-NOT-CLOSED`

This is the single most important line in the method.

An agent reaching the `Resolved` category means *the agent believes its part is done and has
posted evidence*. It says nothing about whether the value is real, whether the acceptance
criteria were understood correctly, or whether the change should exist at all. Those are questions
of value, and value is decided by a human — after whatever tests the instance runs between
*Awaiting test* and *Integration test*.

Therefore:

- No agent, orchestrator, policy or automation may set `Closed`. Neither may an instance hat
  (QA, key user).
- A track that cannot distinguish the `Resolved` states from `Closed` must add a field that can.
- A board column named `Done` is reached **only** by `Closed`.
- Metrics count `Closed`. Everything in `Resolved` is work in flight, however many states it has.

## Rejection — `RULE-STATE-REJECT`

An Approver who does not accept moves the item back to `In development` with **one objective
note** on the item: which criterion failed and what evidence would satisfy it. "Not good enough"
is not a rejection note; it is a missing acceptance criterion, and it goes back to the PO, not the
implementer. QA and the key user reject the same way, from their own states.

## `Removed` is not `Closed` — `RULE-STATE-REMOVED`

Discarding an item is a legitimate outcome. Counting it as delivery is a lie in the metrics. The
two categories exist so that the lie is impossible.

> 🟢 **Closed** — "Delivered and accepted."
> 🗑️ **Removed** — "Will not happen."

Canon: RULE-STATES · RULE-STATE-CATEGORIES · RULE-PACT-PHASES · RULE-STATE-RESOLVED-NOT-CLOSED · RULE-STATE-REJECT · RULE-STATE-REMOVED
