---
id: RULE-TOPOLOGY
canon: true
---

# Topologies — who fills the roles, and how they coordinate

The method names five roles by function (`RULE-ROLES`). A **topology** is the answer to two
questions an instance must settle before its first item: *who fills each role — a person or an
agent* — and *who hands work to whom*. Four topologies cover what teams actually run. Every one
of them ends with a human: `Closed` is a human act in all four (`RULE-STATE-RESOLVED-NOT-CLOSED`).

| Topology | Product Owner | Orchestrator | Implementer | Reviewer | Approver | Typical for |
|---|---|---|---|---|---|---|
| **agent-to-human** | Human | Agent, or the PO by hand | Agent | Agent | **Human** | One PO and one or a few agents. The supervised and unattended modes both live here |
| **agent-to-agent** | Agent, under a human sponsor — or human | Agent | Agents | Agents | **Human** (the sponsor) | An agent-run team: agents hand work to agents; the PO-agent refines and recommends; a person accepts, in batch if they like |
| **independent-agents** | Human | Nobody — a person dispatches each item | One agent per item | Agent | **Human** | Several specialised agents that never share a scope; no queue worth an orchestrator |
| **bot-team** | Theirs — agent or human | Theirs | Theirs | Theirs, or the roster's | **Human, outside the system** | A system of bots that already exists, with its own manager and workers. PACT wraps it; it does not replace it |

## What a topology may and may not change — `RULE-TOPOLOGY`

A topology is recorded once, in `instance.yml` → `topology`, and it decides the `kind` of each
role (`human` or `agent`) and the title the instance gives it. That is all it decides.

It may not change:

- **The Approver is human.** In every topology. An agent that "accepts" produces a recommendation
  on the item — a Resolved-category state plus a comment — and stops. The human sets `Closed`.
- **Implementer and Reviewer are never the same agent on the same item** (`RULE-ROLES`).
- **One writer per scope**, with the claim in the source of truth (`RULE-SINGLE-WRITER`).
- **The gate.** The PR validator reads the same context whoever produced it.
- **The source of truth.** One, durable, never a channel (`AP-CHANNEL-AS-SOT`).

**An agent as Product Owner** is allowed by `RULE-ROLES` — *under a human*. Concretely: the human
sponsor writes the **mandate** on the board (an Epic, or `CURRENT-FOCUS.md`) — what the PO-agent
may prioritise, split and refine without asking. Inside the mandate the agent writes cards,
walks the Definition of Ready and orders the backlog. At the edge of the mandate every decision is
a human gate (`RULE-HITL`, triggers 3 to 5). Money, access and publication are never inside a
mandate.

## How agents coordinate — `RULE-TOPOLOGY-COORDINATION`

Whatever the topology, coordination goes **through the source of truth**, never around it. The
same six mechanisms serve a person handing work to one agent and an orchestrator-agent feeding
ten:

| Need | Mechanism | Never |
|---|---|---|
| Give work to an agent | A handoff (`templates/flow/handoff.md`) linked from the item | A chat message; a prompt pasted with no item behind it |
| Say who is writing where | A claim on the item (`RULE-CLAIM`) | A lock file; an announcement in a channel |
| Report progress or completion | Conclusion and evidence comments on the item (`RULE-CONCLUSION-COMMENT`) | A standup; a direct message |
| Ask another agent for something | A comment on the item, or an `Issue` that blocks it and names who unblocks it | Bot-to-bot chatter in a channel (`AP-BOT-CHATTER`) |
| Escalate to a human | A gate request naming the trigger and the deciding role (`RULE-HITL`), mirrored to the channel | Waiting silently; deciding alone |
| Know what is going on | The daily digest (`RULE-DAILY-DIGEST`) | Asking each agent |

A message between two agents that is not recorded on an item did not happen (`RULE-GOLDEN-TRACE`).
The channel mirror carries **notifications** of these traces; it is never where they are made.
An agent that must talk to another agent writes on the item both of them read.

## What changes per topology

### agent-to-human

The default. A person plans and accepts; agents execute and review. The orchestrator hat may be
worn by an agent (unattended) or by the PO with the prompt pack (supervised). Nothing else in the
method changes.

### agent-to-agent

Agents hand work to agents. The orchestrator is an agent; the Product Owner may be one, under a
sponsor. What changes:

- **Plan** — the PO-agent refines inside the mandate and marks *Awaiting development*; anything
  outside the mandate stops at an `Issue` for the sponsor.
- **Act / Check** — as in the core. More agents in parallel means claims matter more, not less;
  the orchestrator arbitrates collisions (`RULE-ARBITRATION`).
- **Transfer** — the PO-agent's last word is *recommended for acceptance*, written on the item
  with the evidence it read. The sponsor accepts or rejects; a daily or weekly batch is fine,
  and the digest's section 4 is the queue.
- **Sprint close** — a written round on the ceremony item
  ([participation by topology](ceremonies/README.md#participation-by-topology--rule-ceremony-participation)):
  the orchestrator-agent opens it, every role posts its part, the PO-agent decides the carry-over
  inside the mandate and the sponsor decides the rest. The PO-agent's brief is one of the things a
  retrospective changes.

### independent-agents

No orchestrator. A person writes the handoff, records the claim and sets *In development*;
each agent works one item alone and stops at *Awaiting test*. Ownership still has one writer
per scope — two agents on unrelated items may not share a scope. The digest is a saved query
the person reads; the review gate and the validator are unchanged. The sprint close is the
dispatcher's: each agent posts its cards on the items it worked
([participation by topology](ceremonies/README.md#participation-by-topology--rule-ceremony-participation)).

### bot-team

A system of bots that already has a manager and workers adopts PACT **around** itself:

- Its manager wears the **orchestrator** hat; its workers are **implementers**; its reviewers,
  if it has any, are **reviewers** — otherwise the roster's reviewers run beside it. Each hat is
  written as a role in `instance.yml` with the bot's own name as the title.
- Its internal memory or channel is **not** the source of truth. The board is. Every handoff,
  claim, conclusion and gate request lands on the item; the system may keep its own copy.
- The runtime adapter (`adapters/`) declares, concept by concept, what the system **enforces**,
  **advises** or **does not support**; the PR validator stands in for whatever it does not.
- Its ceremonies may run in its own channel — the sprint close included — provided the transcript
  or its summary lands on the ceremony item before the minutes are signed
  ([participation by topology](ceremonies/README.md#participation-by-topology--rule-ceremony-participation)).
  A decision that is not on the item was not taken.
- The Approver is a person outside the system. The system may propose; it never closes.

Canon: RULE-TOPOLOGY · RULE-TOPOLOGY-COORDINATION
