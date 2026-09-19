# Track — Azure DevOps

The lowest-friction track. The method's work-item vocabulary — `Epic → Feature → User Story →
Task`, states grouped in categories (*Proposed → In Progress → Resolved → Completed*, plus
*Removed*), Area Path, Iteration Path — **is** the Azure DevOps process model. The lifecycle's
twelve states are custom states on an inherited process, each in its category. Most of what other
tracks add as custom fields is native here.

| Capability | Status | Note |
|---|---|---|
| Source of truth | ✅ eligible | Boards + Backlogs + Queries in one Team Project |
| Hierarchy | ✅ native | Parent/Child links, multiple levels |
| Iterations | ✅ native | Iteration Path with dates |
| Code review | ✅ native | Azure Repos pull requests, required reviewers, branch policies |
| CI | ✅ native | Azure Pipelines; `automation/ci/azure-pipelines/` is copy-ready |
| Two state axes | ✅ | WI-State is the native `State`; Status is the Board Column |
| Claims | custom | One text field, or a tag convention — see `fields.md` |

## What comes for free

Fifteen of the method's twenty-one fields are native (`fields.md`); six are custom (`PACT.Role`,
`PACT.Risk`, `PACT.Claim`, `PACT.Homolog`, and the optional `PACT.Retro` and `PACT.ExternalRef`).
The review gate is a branch policy.
Burndown and velocity are Analytics views you do not have to build. If you are choosing a tool
from scratch and want the least translation, this is it.

## What to watch

- **Blocker — setup step 4.** The twelve states are created on the inherited process, each in
  its Azure category. The default Agile **Task** has no *Resolved* category at all; do not go live
  until you add it. Tasks that skip *In Progress* → *Completed* break
  `RULE-STATE-RESOLVED-NOT-CLOSED` for the type agents execute.
- Board columns are per backlog level. Configure the Story board and the Task board separately.

## Files

[`mapping.yml`](mapping.yml) · [`capabilities.yml`](capabilities.yml) · [`fields.md`](fields.md) · [`setup.md`](setup.md) · [`policies.md`](policies.md) · `queries/` ([gate queue](queries/gate-queue.wiql), [digest](queries/digest.wiql))
