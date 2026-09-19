# Scenarios — which topology is yours

Four ways to fill the five roles. The method is the same in all of them; what changes is who is a
person, who is an agent, and who hands work to whom. The rule is
[`core/15-topologies.md`](../../core/15-topologies.md); these pages are the reasoning and the
setup, one per topology.

| If … | Topology | Page |
|---|---|---|
| One PO, one or a few agents; you paste prompts or run a coding CLI | **agent-to-human** | [agent-to-human.md](agent-to-human.md) |
| Agents hand work to agents; an orchestrator-agent runs the queue; maybe a PO-agent under a sponsor | **agent-to-agent** | [agent-to-agent.md](agent-to-agent.md) |
| Several specialised agents, each on its own items, dispatched by a person | **independent-agents** | [independent-agents.md](independent-agents.md) |
| A system of bots with its own manager and workers already exists | **bot-team** | [bot-team.md](bot-team.md) |

## Three questions that decide it

1. **Who hands work to the agents?** A person → `agent-to-human` or `independent-agents`. An
   agent → `agent-to-agent`. A system you did not build → `bot-team`.
2. **Do the agents share scopes?** If two agents could ever touch the same paths, you need an
   orchestrator to arbitrate claims — not `independent-agents`.
3. **Who accepts?** A person, in every topology. If that answer is anything else, stop: read
   [`core/05-states.md`](../../core/05-states.md) first.

## What every topology shares

- Coordination happens **on the item** — handoff, claim, conclusion comment, gate request. A
  channel only notifies ([`core/15`](../../core/15-topologies.md), *How agents coordinate*).
- The PR validator reads the same context whoever produced it
  ([`automation/README.md`](../../automation/README.md)).
- `Closed` is a human act. The digest's *Ready for review* section is that person's queue.
- Ceremonies are records with a window: Planning on the iteration's first day, the sprint close —
  review → retrospective → refinement — on its last working day. Agents attend by writing on the
  ceremony item; each page below says who is in the room
  ([participation by topology](../../core/ceremonies/README.md#participation-by-topology--rule-ceremony-participation)).

Set it in `instance.yml` → `topology`. `make instance` refuses a topology that contradicts the
roles (an `agent-to-agent` with a human orchestrator, an `independent-agents` with an agent one).
The onboarding interview asks these questions for you — [`docs/onboarding/`](../onboarding/README.md).
