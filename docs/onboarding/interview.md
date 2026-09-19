# The interview — from "set this up" to an instance

For the agent running it, or the person reading it. **One block per turn**: ask the block's
questions in the person's language, end your turn, wait for the answers, show them back as a
table. Write **no file** until Block 9 is confirmed — not `instance.yml`, not a context file, not
a rule for your own runtime. When an answer is missing, *offer* the default in the last column
**and say so**; a default the person never saw is a guess (`AP-SILENT-SETUP`). When the default
would be a guess about value, money, access or a person, write
`- [ ] unknown — <what> → <who decides>` and ask.

Every question says where its answer goes. The target file is `instance.yml` unless stated; the
shape is [`instance.example.yml`](../../instance.example.yml).

## Block 0 — Language, purpose, names

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Which language should I use with you, and which language should the artifacts (cards, handoffs, receipts) be written in? | Agents answer in the instance language; the kit's own files stay in English | `language` | `en` |
| What is this environment for — one paragraph: the product or project, who it serves, the one constraint that shapes everything | Becomes the *Product* section every agent reads each session | `AGENT-CONTEXT.md` → *Product* | `unknown` — ask; never invent a product |
| What is the name of the project, company or organization? A name only | The instance's `organization.name` and the title of `AGENT-CONTEXT.md` | `organization.name` | `unknown` — ask |
| What is the product or system this instance delivers — a name only? | Names every iteration (`{product}` in the sprint name) and the agent context | `organization.product` | `unknown` — ask; never invent a product |
| Is anything here confidential — names, customers, systems I should not write into files? | The leak check forbids personal data and private links in the kit; the instance is yours, but say what stays out of it | nothing — a constraint on everything below | Assume names of people never go into files |

## Block 1 — Who accepts

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Is the person who accepts the work inside your organization, or a customer / sponsor outside it? | Decides the profile: `internal` (the PO accepts) or `agency` (a customer signs) — [`choose-your-profile.md`](../choose-your-profile.md) | `organization.profile` | `internal` |
| What is that person called — a role title, not a name? | The Approver's title | `roles.approver.title` | `Product Owner` (internal) · `Client Approver` (agency) |
| Who owns priority and writes the cards — the same person? | The PO's title; whether PO and Approver coincide | `roles.product_owner` | Same as the Approver |

## Block 2 — Topology: humans and agents

Read [`docs/scenarios/README.md`](../scenarios/README.md) with the person if they hesitate.

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| How do you want to use the kit: agents working with a human PO; agents handing work to agents under a sponsor; each agent working alone on its own items; or an existing system of bots? | The topology — who fills each role and who hands work to whom (`core/15-topologies.md`) | `topology` | `agent-to-human` |
| Who hands work to the agents: a person, or an orchestrator agent? | Decides `roles.orchestrator.kind`; `make instance` refuses `agent-to-agent` with a human orchestrator and `independent-agents` with an agent one | `roles.orchestrator` | Person for `agent-to-human` / `independent-agents`; agent otherwise |
| Will an agent play Product Owner? If so, who is the human sponsor, and what may the PO-agent decide alone (the mandate)? | An agent PO is allowed only under a human with a written mandate; the mandate goes on the board and in `CURRENT-FOCUS.md` | `roles.product_owner`, `CURRENT-FOCUS.md` → *Now* | Human PO |
| Do you already run a team of bots — a manager bot, worker bots, a reviewer bot? What is each called, how is it triggered, where does it keep its memory? | Maps their roles onto the roster and tells us whether an adapter is needed ([`docs/scenarios/bot-team.md`](../scenarios/bot-team.md)) | `roles.*.title`, a new `adapters/<name>/` | No existing system |
| Could two agents ever touch the same files? | If yes, claims and an orchestrator matter (`RULE-SINGLE-WRITER`); if never, `independent-agents` is enough | `topology`, `agents/ownership.yml` scopes | Yes — assume they could |
| How should the agents communicate — where does a handoff, a question, a status live? | The answer is always *on the work item*; a channel only notifies (`RULE-TOPOLOGY-COORDINATION`). Ask to find out what they do today and what has to change | `mirrors` (a channel), `AGENT-CONTEXT.md` → *Rules* | Item comments; a notification channel if they have one |

## Block 3 — The tool that holds the work

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Where will the backlog live — Azure DevOps, GitHub Projects, Notion, a spreadsheet, something else? | The source of truth. One tool, with durable history; a chat tool can never be it ([`choose-your-track.md`](../choose-your-track.md)) | `source_of_truth.track` | `unknown` — ask; there is no sensible default |
| Which board / project / database in it, by name? | The instance's board name | `source_of_truth.board` | `unknown` — ask |
| Will a chat tool mirror it for notifications and human gates? Which channel? | A mirror, `purpose: notifications` — never the source of truth | `mirrors` | none |
| If the tool is none of the five tracks: does it keep attributable history? custom fields? parent/child links? comments? attachments? a pull-request object? CI? a sprint entity? webhooks? saved queries? | The eleven capability questions from `core/model/capabilities.yml`; the answers say whether it can be a source of truth and what must be substituted | A new `tracks/<name>/` from [`tracks/_contract/`](../../tracks/_contract/track-contract.md) | Pair the tool with one that can be the source of truth |

## Block 4 — Where everything else lives

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Where is the code, and what commands prove a change is fine (lint, tests, build)? | The verification commands the gate runs; the code host decides where the review gate lives | `conventions.verification_commands` | `unknown` — ask |
| Where are sprints or iterations kept, how long is one, and on which day does it start? | The iteration entity and the cadence; the kit's default is one week, Planning on the first day | `cadence.iteration_length_days`, `cadence.iteration_start_day`, track setup | 7 days, starting Monday |
| Where do blockers and impediments go? | `Issue` items in the source of truth, not a chat | track setup — Issue type | The board |
| Where do specifications, decisions and minutes live? | The audit trail (`core/11-docs-in-the-code.md`): a `docs/` tree or the tool's pages | `AGENT-CONTEXT.md` → *Repository* | `docs/` in the repository |
| How are branches named? | The branch pattern agents follow | `conventions.branch_pattern` | `{type}/{item-id}-{slug}` |

## Block 5 — Lifecycle and board

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| The kit's board runs twelve states in five categories (`core/05-states.md`). Which of them do you use? Is there a homologation stage with QA and a key user? An integration test? | The subset of states the instance runs; categories are never dropped | `lifecycle.states`, `optional_rules.require_homologation_qa`, `roles.qa`, `roles.key_user`, `conventions.homologation_environment` | All twelve; homologation off |
| What do you call each state on your board, in your language? | Labels on the board; the ids stay neutral | `lifecycle.labels` | The English names |
| Do you use tags? Which families — year, external ticket id, category, module, project, current sprint, blocked? | The tag taxonomy is an instance convention; `needs-human` is the one tag every instance keeps | `conventions.tags`, track labels | `needs-human`, `spike`, `gap`, `improvement`, `tooling`, `doc`, `qa`, `ceremony` |
| Do items reference an external ticket (a service-desk id) that must stay visible in the title? | A traceability convention: `[<ref>] <title>` and an external-reference field | `optional_rules.require_external_ref` | off |

## Block 6 — Cadence

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Timezone? | Every date on the board and in the digest | `cadence.timezone` | `UTC` |
| When is Planning, and when is the sprint close — review, retrospective and refinement in one session on the iteration's last working day? Is the daily a meeting or a digest? | The ceremonies exist in every instance; the daily is a digest, never a meeting (`RULE-GOLDEN-EVENTS`); the sprint close precedes the next Planning (`RULE-CEREMONY-SPRINT-CLOSE`) | `cadence.sprint_close`, `cadence.planning`, `cadence.refinement`, `cadence.review`, `cadence.retrospective`, `cadence.sync` | Planning Monday · sprint close Friday · sync daily |
| How are sprints named? Show the pattern: `Sprint {seq:02} {yy} Q{quarter} {product}` gives `Sprint 02 26 Q1 <product>`; the sequence restarts every year | One name per iteration — on the board, in the minutes, in the digest (`RULE-ITERATION-NAMING`) | `cadence.iteration_name_pattern`, `cadence.sequence_resets` | The default pattern, reset every year |
| When agents take part in a ceremony, where do they write — on the ceremony item, or in your bot system's own channel with the transcript attached? | An agent attends by writing on the ceremony item; a bot system's channel may host the round if the transcript lands on the item (`RULE-CEREMONY-PARTICIPATION`) | `AGENT-CONTEXT.md` → *Rules* | The ceremony item |

## Block 7 — Risk and human gates

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Which paths are sensitive — user data, permissions, schemas, money, deployment? | The risk floors: a change under those paths cannot be below `high` whatever a reviewer says | `agents/policies/risk-floors.yml`, `agents/ownership.yml` | The kit's example scopes — replace the globs |
| Who is the named human that reviews a high-risk change before the agent may say it is done? | `RULE-RISK-GATES` needs a person, by role | `roles.approver` or a note in `AGENT-CONTEXT.md` | The Approver |
| What must an agent never do without asking — deploy, pay, delete data, contact a customer? | The five human-in-the-loop triggers, made concrete for this instance | `AGENT-CONTEXT.md` → *Rules*; handoff *Out of scope* | The five triggers of `core/03` |

## Block 8 — Conventions and optional rules

| Ask | Why we ask | Writes to | Default |
|---|---|---|---|
| Does a customer sign acceptance? Do you want a changelog line per closed item? An iteration report? Effort and remaining-work tracking in sprints? | The optional rules an instance may switch on | `optional_rules.*` | Profile defaults (`profiles/<profile>/profile.yml`) |
| Which agent runtime will run the roles — a chat, an IDE agent, a coding CLI, your bot system? | Decides whether the prompt pack is enough or an adapter is needed ([`adapters/README.md`](../../adapters/README.md)) | `adapters/<name>/`, `AGENT-CONTEXT.md` | The prompt pack |

## Block 9 — Confirm, then write

Show one table: every decision above, its value, and whether it came from an answer or a
default. Ask for one confirmation. A table whose every row says *default* means the interview did
not happen — go back to Block 0. Nothing is written before the yes. Then produce the outputs in
[`setup-plan.md`](setup-plan.md).

## Stop conditions

Never write a file before Block 9 is confirmed; that is `AP-SILENT-SETUP`. Stop and ask — do not
decide — when an answer would need you to: name a person; choose a
source of truth; spend money or create anything in an external tool; grant or use credentials;
pick a value, a priority or a customer commitment; or resolve two answers that contradict each
other. Those are `RULE-HITL` triggers, and the interview is not exempt from the method it sets up.
