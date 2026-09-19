---
id: RULE-CEREMONIES
canon: true
---

# Ceremonies with agents

The five Scrum ceremonies survive, and four of them meet in two sessions per iteration:
**Planning** opens the iteration on its first day; the **sprint close** — Review, then
Retrospective, then Refinement, in that order, one session — ends it on its last working day.
What changes is the PO's role in each and what "attending" means for an agent: never oral status,
never being in a room (`RULE-GOLDEN-EVENTS`). An agent attends by **writing on the ceremony item**,
within the session's window (`RULE-CEREMONY-PARTICIPATION`, below).

| Ceremony | PO's role | Focus with agents | Minutes |
|---|---|---|---|
| [Planning](planning.md) | **Protagonist** | Scope, iteration goal, assignment to skills | `templates/ceremonies/planning-minutes.md` |
| [Daily sync](daily.md) | **Observer** | A digest, blockers, decisions needed from a human | Not a document — a generated digest |
| [Sprint close](sprint-close.md) | **Central, then member, then owner** | One session: Review, Retrospective, Refinement; the carry-over of what did not finish; the next iteration named | `templates/ceremonies/sprint-close-minutes.md` |
| [Review](review.md) | **Central** | Human acceptance with evidence — the Transfer phase | Part 1 of the sprint close; `templates/ceremonies/review-minutes.md` when held apart |
| [Retrospective](retrospective.md) | **Member** | Cards from people and agents; skills, briefs, floors, DoR — the system, not the model | Part 2 of the sprint close; `templates/ceremonies/retrospective-minutes.md` when held apart |
| [Refinement](refinement.md) | **Owner** | Cards that pass the Definition of Ready | Part 3 of the sprint close; `templates/ceremonies/refinement-minutes.md` when held apart |

## Cadence

Set in `instance.yml` under `cadence:`. The default is one **seven-day iteration**: Planning on
its first day (`cadence.iteration_start_day`), the digest every working day, the sprint close on
its last working day (`cadence.sprint_close`). An instance may run a longer iteration
(`iteration_length_days`, five to thirty) and may hold the three parts of the sprint close apart;
the method's requirements do not move: Review and Retrospective happen **at least once per
iteration**, Refinement happens **before** Planning — never during it — and the sprint close
precedes the next Planning, which is why the two sit on different days.

## Iteration naming — `RULE-ITERATION-NAMING`

An iteration has one name, rendered from one pattern, and that name is what the board, the
digest, the minutes (as their H1) and the ceremony item carry. The pattern and its reset are the
model's defaults (`core/model/iterations.yml` → `naming`); an instance may override them under
`cadence.iteration_name_pattern` and `cadence.sequence_resets`.

| Placeholder | Meaning |
|---|---|
| `{seq}` · `{seq:02}` | Sequence number since the last reset — every year, every quarter, or never; `:02` zero-pads |
| `{yy}` · `{yyyy}` | Year of the start date, two or four digits |
| `{quarter}` · `{half}` | Quarter (1 to 4) or half (1 or 2) of the start date |
| `{product}` | `organization.product` — the instance must set it when the pattern uses it |
| `{start}` · `{end}` | The iteration's dates, ISO 8601 |

The default pattern, `Sprint {seq:02} {yy} Q{quarter} {product}`, names the second week of 2026
at a fictitious product *Sprint 02 26 Q1 Acme Portal*. `automation/scripts/iteration_name.py`
prints the name for a start date and derives the sequence for seven-day iterations, so nobody
counts weeks by hand. The next iteration's name is written at the sprint close, before Planning.

## Participation by topology — `RULE-CEREMONY-PARTICIPATION`

A ceremony is a **record with a window**, not a meeting an agent joins. People may sit in a room;
agents attend by writing on the ceremony item (`sprint-close.md`), and the minutes are compiled
from what is on it. Coordination stays on the source of truth (`RULE-TOPOLOGY-COORDINATION`).

| Topology | Who is in the room | How agents take part | Who decides |
|---|---|---|---|
| **agent-to-human** | The PO, the Approver, the people who test | The orchestrator posts the agents' cards and evidence on the ceremony item **before** the session, from item evidence only | The PO; `Closed` by the Approver |
| **agent-to-agent** | Nobody — or the sponsor, reading | A **written round**: the orchestrator-agent opens the ceremony item at the sprint-close time; every role posts its part within the window; the orchestrator compiles the minutes | The PO-agent inside its mandate; the sponsor reads the digest and decides the rest, `Closed` included |
| **independent-agents** | The dispatcher | Each agent posts its cards on the items it worked | The dispatcher |
| **bot-team** | Whoever the system reports to | The system's own channel may host the round, **provided** the transcript or its summary is attached to the ceremony item before the minutes are signed | The system's manager inside its mandate; the human Approver otherwise. A decision that is not on the item was not taken |

What no topology changes: the order of the three parts, the carry-over rule (`RULE-CARRY-OVER`),
the cards rule (`RULE-RETRO-CARDS`), and that `Closed` and `Removed` stay human acts.

## Shared minutes header — `RULE-CEREMONY-META`

Every set of minutes opens with the same block, provided as the fenced fragment
`templates/_fragments/ceremony-meta.md`: date and time with timezone, ceremony, iteration — by
its name —, roles present, where the round happened, and the link to the board view that was on
screen. Roles, not names — a set of minutes that says "the PO and the orchestrator" is as
traceable as one that names people, and it does not age.

## Every ceremony page has the same shape

- **PO's role** in one line.
- A table of **Do / Don't** — what the PO does, and the mistake that looks like doing it.
- **Output** — what exists after the ceremony that did not exist before.

Canon: RULE-CEREMONIES · RULE-CEREMONY-META · RULE-ITERATION-NAMING · RULE-CEREMONY-PARTICIPATION
