---
id: RULE-ANTI-PATTERNS
canon: true
---

# Anti-patterns

Each row is something teams do with agents that looks reasonable and is not. The id lets other files
point at a specific failure mode.

## Method

| Id | Anti-pattern | Why it fails | Prefer |
|---|---|---|---|
| `AP-GIANT-PROMPT` | One huge prompt instead of an item with acceptance criteria | No acceptance, no trace, no way to reject one part | One item, clear ACs, short Tasks |
| `AP-AGENT-CLOSES` | An agent moves an item to `Closed` | Value delivered with no product owner | `Resolved` → human review → `Closed` |
| `AP-THRASH` | Re-prioritising the iteration every time a tool fails | The iteration never converges | An `Issue` and a retry; the PO intervenes only for value |
| `AP-BUG-FOR-GAPS` | Filing every product gap as a Bug | Defect metrics become meaningless | A Story tagged `gap` |
| `AP-REMOVED-AS-CLOSED` | Using `Removed` as a way to "finish" | Delivery metrics lie | Keep discard and delivery separate |
| `AP-STANDUP` | Asking agents for oral status | Costs tokens, produces nothing the item does not already have | Read the conclusion and evidence comments |
| `AP-INVENTED-STATUS` | Moving a card without evidence on the item | The board stops being true | No transition without the conclusion comment |
| `AP-SILENT-SETUP` | Writing the instance from defaults without asking | The topology, the board and the roles are guesses nobody made; the method starts on an invented foundation | The onboarding interview, one block per turn, the answers shown back before any file exists (`RULE-GOLDEN-NO-INVENTION`) |

## Factory

| Id | Anti-pattern | Why it fails | Prefer |
|---|---|---|---|
| `AP-REVIEW-BEFORE-CI` | Enabling parallel review before deterministic verification exists | Reviewers spend their pass on what a test would catch for free | Verification first, reviewers second |
| `AP-FLOOR-EDIT` | An agent edits the risk floor to pass its own change | The floor exists precisely against the agent's optimism | Floors change only by a reviewed change to the policy |
| `AP-CLAIMED-SMOKE` | Declaring a manual check that was not run | False evidence on a value item | If there is no log or screenshot, it goes in *Not verified* |
| `AP-BOT-CHATTER` | Agents talking to agents in a channel | Consumes budget, produces neither a diff nor a trace on the item | Trace on the work item; the channel carries notifications. The one exception is a ceremony round hosted in a bot system's own channel — valid only once the transcript or its summary is on the ceremony item (`RULE-CEREMONY-PARTICIPATION`) |
| `AP-SELF-MERGE` | An agent merges its own change without a gate | The implementer's blind spots are the reviewer's blind spots | Review gate, then merge |
| `AP-SWARM` | Several agents writing to the same tree | Conflicts, half-applied changes, two agents each "done" | N readers, one writer (`RULE-SINGLE-WRITER`) |
| `AP-CLAIM-IN-FILE` | Recording scope claims in a repository file | The anti-conflict mechanism becomes a conflict point | Claims live in the source of truth |
| `AP-CHANNEL-AS-SOT` | Treating a chat tool as the source of truth | Messages are ephemeral, unsearchable, unversioned | One SoT with durable history; the channel mirrors it |
| `AP-HOMOLOG-SKIP` | QA or a key user tests without the branch and the homologation URL on the board, or QA tests the product, or Transfer review is skipped and the PO is updated only in a chat | The PO accepts a change nobody can reopen on the environment that was supposed to prove it | Check review, then QA links the env, then the key user tests, then Transfer review reads that evidence (`RULE-HOMOLOG-QA`) |
| `AP-HOMOLOG-BEFORE-REVIEW` | QA starts the homologation environment while the item is still `Active`, or before the review gate has passed | Homologation proves a change Review has not accepted | Reviewers first; `Resolved`; then QA starts the environment for that branch |

Canon: RULE-ANTI-PATTERNS
