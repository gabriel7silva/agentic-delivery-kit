---
id: RULE-ROLES
canon: true
---

# Roles

Five roles, named by **function**. Who fills each one — a person, an agent, a script, a rota — is an
instance decision recorded in `instance.yml`. The method only requires that each role exists and that
the boundaries below hold.

| Role | Typically filled by | Owns | Never does |
|---|---|---|---|
| **Product Owner** | A human (or an agent under a human) | Priority, value, acceptance, stakeholders | Executes tasks; edits code |
| **Orchestrator** | An agent or the runtime | Ritual, queue, handoffs, tool impediments | Chooses value scope; moves items to `Closed` |
| **Implementer** | An agent with a clear skill and scope | Executing Tasks — code, analysis, docs, QA | Writes outside its claimed scope; reviews its own work |
| **Reviewer** | A second agent or an automated policy | Checking before `Resolved`; returning findings **and** a risk verdict | Edits the change under review |
| **Approver** | A human | `Closed` on items of value; credentials; anything published | Delegates `Closed` to an agent |

## Boundaries that carry the method

**One approver, always human.** The Product Owner and the Approver may be the same person. When the
customer is external they usually are not: the PO is inside the delivering organisation, the
Approver is at the customer.

**Implementer and Reviewer are never the same agent on the same item.** A model reviewing its own
diff has the same blind spots twice.

**The Orchestrator is a scheduler, not a decision-maker.** It pulls `Ready` items, issues handoffs,
tracks claims and escalates. When a decision of value or risk appears, it stops and hands it to a
human — see `RULE-HITL`.

## Mapping onto a team you already have

If your team has one bot that does everything, that bot is filling four roles. Write that down in
`instance.yml`. The method still holds — the value is in knowing which hat is on when a decision is
taken, so that the Reviewer hat never signs off the Implementer hat's work without a second pass.

## Instance hats — homologation

When `require_homologation_qa` is on, two more hats exist on the instance. They are not a sixth
and seventh method role. They do not set `Closed`. Full text: `core/14-homologation.md`.

| Hat | Owns | Never does |
|---|---|---|
| **QA** | Starts the homologation environment for the feature branch **after Check review**; writes `BRANCH` and `HOMOLOG_LINK` | Tests the product; starts the env before `Resolved` |
| **Key user** | Tests on that environment; writes the result on the item for **Transfer review** | Starts the environment; skips Review |

## What the Product Owner is — and is not

The PO **maximises value**, protects and orders the backlog, connects the business and the team,
makes clear *what* will be done and *why*, facilitates business decisions, negotiates scope,
runs discovery, supports the metrics — and says **no** when a request shows no value. Effort,
deadlines, the technical solution, the management of people and the facilitation of the team's
own rituals belong to other roles.

| The PO is not | Who owns that instead |
|---|---|
| A project manager | Nobody in this method: the board, the iteration and the digest are the plan |
| The team's boss | Nobody: the team owns the *how*; the PO owns the *what* and the *why* |
| A facilitator of the team's rituals | The orchestrator facilitates the agents' rituals; people facilitate their own |
| A developer or the technical lead | Implementers and reviewers; the technical solution and the effort are theirs |
| A status inspector | The conclusion comments and the digest; nobody collects oral status (`RULE-GOLDEN-EVENTS`) |
| The key user | The key user tests on the homologation environment; the PO accepts value (`core/14-homologation.md`) |

Canon: RULE-ROLES
