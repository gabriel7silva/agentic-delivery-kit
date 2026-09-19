# Azure DevOps — setup

From an empty organisation to a board that runs PACT. About an hour the first time.

**Do not skip step 4.** The default Agile process has four or five states per type and none of
the lifecycle's twelve; Tasks lack the *Resolved* category altogether. Without step 4 the unit
agents execute cannot honour `RULE-STATE-RESOLVED-NOT-CLOSED`.

## 1. Process

1. Organization settings → Process → create an **inherited** process from **Agile**. Name it
   `PACT-Agile`.
2. Create or switch the project to that process.

## 2. Custom fields

Process `PACT-Agile` → each of **User Story**, **Task**, **Bug**:

| Field | Type | Values |
|---|---|---|
| `PACT.Role` | Picklist (string) | your `instance.yml` role ids |
| `PACT.Risk` | Picklist (string) | `low`, `medium`, `high` |
| `PACT.Claim` | Text (multiple lines) | — |
| `PACT.Homolog` | Text (single line) | running homologation URL for this item's branch |
| `PACT.Retro` (optional) | Text (multiple lines) | — |
| `PACT.ExternalRef` (when `require_external_ref` is on) | Text (single line) | the request's id in the external system; the title starts with `[<ref>]` |

Add `PACT.Risk` to Feature too if you gate Features. Story Points (or Effort), Remaining Work and
Business Value are native — put them on the card and on the Taskboard when `track_sprint_metrics`
is on; nothing to create.

## 3. Iterations

Project settings → Boards → Project configuration → Iterations. Create them with **start and end
dates**; the length comes from `instance.yml` `cadence.iteration_length_days`.

## 4. States, by category

Process `PACT-Agile` → each of **User Story**, **Task**, **Bug** → States. Azure DevOps groups
states in categories (*Proposed*, *In Progress*, *Resolved*, *Completed*, *Removed*) — those are the
PACT categories under other names, so create each state in the category shown. Rename the
defaults where the name differs; add the rest.

| State | Azure category | PACT category |
|---|---|---|
| New | Proposed | NEW |
| In analysis | Proposed | NEW |
| Awaiting development | Proposed | NEW |
| Blocked | In Progress | ACTIVE |
| In development | In Progress | ACTIVE |
| Awaiting test | Resolved | RESOLVED |
| Prepare homologation | Resolved | RESOLVED |
| Key-user homologation | Resolved | RESOLVED |
| Prepare release | Resolved | RESOLVED |
| Integration test | Resolved | RESOLVED |
| Closed | Completed | CLOSED |
| Removed | Removed | REMOVED |

Task has no *Resolved* category in the default Agile process — add it, or Tasks skip from
*In Progress* to *Completed* and `RULE-STATE-RESOLVED-NOT-CLOSED` cannot hold for the type agents
execute. An instance that runs fewer states (`instance.yml` → `lifecycle`) creates only those,
keeping at least one per category. A label in another language goes on the state name; the
category is what the rules read.

## 5. Board columns

Boards → Stories board → Column options. One column per state, in this order:

| Column | Mapped State |
|---|---|
| Backlog | New |
| In analysis | In analysis |
| Ready | Awaiting development (the column's *definition of done* = your DoR) |
| Blocked | Blocked |
| In development | In development |
| Awaiting test | Awaiting test |
| Prepare homologation | Prepare homologation |
| Key-user homologation | Key-user homologation |
| Prepare release | Prepare release |
| Integration test | Integration test |
| Done | Closed |

Repeat for the Tasks board. Set the WIP limit on **Awaiting test** to the realistic daily
capacity of the people who test — they are the human bottleneck (`core/ceremonies/planning.md`).

## 6. Repository and branch policies

Repos → link the repository. Then `policies.md`: minimum reviewers, required reviewers per path,
linked work item required, build validation. That is the review gate.

Create the feature branch from the work item (Development → New branch) so `BRANCH` fills. A
branch that only exists in the repo does not appear on the item. Set **Target Date** in
Planning; set **Start Date** the day the item becomes Active.

## 7. Tags

Pre-create `needs-human`, `spike`, `gap`, `improvement`, `tooling`, `doc`, `qa`.

## 8. Queries and dashboard

Import `queries/*.wiql` as shared queries. Add **Gate queue** and **Daily digest** to a dashboard the
PO opens every morning. **Feature Timeline** and **Epic Roadmap** (Boards → Backlogs) show the
hierarchy over time with no setup; **Analytics** gives burndown and velocity from Remaining Work
and Effort when `track_sprint_metrics` is on.

## 9. Verify

Create one User Story from `templates/work-items/user-story.md`, move it through every column, and
confirm the State changes underneath match `mapping.yml`. If a column change does not change the
State, the column mapping in step 5 is wrong.
