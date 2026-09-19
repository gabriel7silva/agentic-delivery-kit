# Changelog

Versions track the **neutral contract** — the symbols in `core/model/`, the fields, the states and
the track mapping schema — not the prose. Prose can improve without a version bump; a symbol that
changes meaning cannot.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: SemVer on the contract.

## [Unreleased]

### Fixed
- **Leak denylist file.** `check_leaks` no longer applies the denylist rule to
  `.leakcheck-denylist` or `.leakcheck-denylist.example`, so configuring literal
  terms via the git-ignored file does not fail the list against itself.
  `.leakcheck-denylist.example` documents the format.
- **L0 coverage.** Extensionless text (`LICENSE`, `Makefile`, …) is scanned. A
  `github.com/<owner>/<repo>` URL that is not `example-org` / `your-org` is a
  `repo-url` leak. The README CI badge no longer points at a personal account.
- **Slack connector.** `_post` only prints. Live `chat.postMessage` is not wired;
  `--apply` stays snapshot-only.

### Changed
- **L4** is written down as unused so the level numbers stay stable.
- **Windows.** `check.ps1` runs the same steps as `make check` when `make` is
  missing. `CONTRIBUTING.md` says how to arm the denylist and that git metadata
  is outside L0.

## [0.4.3] — 2026-09-18

Patch: the person gets an instruction of their own.

### Added
- **The kick-off prompt** (`docs/onboarding/kickoff-prompt.md`): the message to paste when the
  entry point did not load — kit in a subfolder, a runtime the kit has no pointer for, a chat with
  no access to files — so that any agent runs the interview one block per turn and writes nothing
  before the person confirms. Linked from the README, the onboarding index, start-here and the
  quickstart; the setup protocol in `AGENTS.md` names it.

## [0.4.2] — 2026-09-18

Patch: two gaps in the entry point, found while writing the test that tells the agent nothing.

### Fixed
- **Vendored kit, no setup yet.** The pointers an adopter generates with `--kit .pact` sent the
  runtime to an `AGENTS.md` that does not exist before the interview. They now fall back to
  `.pact/AGENTS.md` — the kit's entry point, which interviews the person into their own.
- **First contact.** `AGENTS.md` says what to do with a vague first message — a greeting, "what is
  this?" — offer the three requests, write nothing — and that a setup request in any wording
  starts the interview at Block 0 without asking what to do.

## [0.4.1] — 2026-09-18

Patch: the onboarding interview was easy to skip, and only four runtimes had a pointer file.

### Fixed
- **The interview comes first, in writing.** `AGENTS.md` carries a setup protocol: the first
  reply to a setup request is Block 0 of the interview and nothing else; one block per turn; no
  file — not `instance.yml`, not a rule file — before the person confirms Block 9; "use the
  defaults" is shown in the confirmation table, never assumed. The interview, the setup plan and
  the onboarding index say the same; `AP-SILENT-SETUP` names the failure.
- **Where to open the kit.** Runtimes read `AGENTS.md` and their rule files from the folder that
  was opened, never from a subfolder. The README, the onboarding index and `AGENTS.md` say so,
  and what to type: *Read `AGENTS.md` and set this up for my team*.

### Added
- **A pointer file for every runtime, generated.** `automation/scripts/lib/entry_points.py`
  lists the runtimes; `automation/scripts/entry_points.py` writes the pointers from one template
  — Claude Code, Gemini CLI, Qwen Code, Warp, Aider, Cursor, GitHub Copilot, Windsurf, Cline,
  Roo Code, Kilo Code, Continue, JetBrains Junie, Kiro, Amazon Q Developer, Trae, Augment — and,
  with `--root <dir> --kit .pact`, for an adopter's repository. `make entry` refuses a pointer
  that drifted from the generator; every pointer names the interview.

## [0.4.0] — 2026-09-18

Minor under `0.x`: the cadence gains keys, the iteration gains a name, one transition is added.
The migration note says what an adopter touches.

### Added
- **Sprint close** (`core/ceremonies/sprint-close.md`; `RULE-CEREMONY-SPRINT-CLOSE`,
  `RULE-CARRY-OVER`): one session on the iteration's last working day — Review, then
  Retrospective, then Refinement — with a ceremony item on the board (`Task`, tag
  `process: ceremony`, child of the standing *Ceremonies <year>* Story) and one carry-over
  decision per open item: carry, return or remove. Minutes template
  `templates/ceremonies/sprint-close-minutes.md`; rendered example
  `examples/ceremonies/sprint-close-example.md`.
- **Retro cards** (`RULE-RETRO-CARDS`): `went-well`, `went-wrong`, `recurring-impediment`,
  `improvement` — each with the iteration name, the author as role · human/agent and the items it
  cites; agents write them from evidence only. Fragment `templates/_fragments/retro-cards.md`.
- **Participation by topology** (`RULE-CEREMONY-PARTICIPATION`): an agent attends a ceremony by
  writing on the ceremony item within the window; a bot system's own channel may host the round
  when the transcript lands on the item. `AP-BOT-CHATTER` carries that one exception.
- **Iteration naming** (`RULE-ITERATION-NAMING`): `core/model/iterations.yml → naming` — pattern
  `Sprint {seq:02} {yy} Q{quarter} {product}`, sequence reset every year, placeholders `seq`,
  `yy`, `yyyy`, `quarter`, `half`, `product`, `start`, `end`. `automation/scripts/iteration_name.py`
  renders the name and derives the sequence for seven-day iterations.
- Instance keys `organization.product`, `cadence.iteration_start_day`, `cadence.sprint_close`,
  `cadence.iteration_name_pattern`, `cadence.sequence_resets` — optional; every shipped instance
  sets them. `check_instance` findings `iteration-name-pattern`, `iteration-product`,
  `iteration-start-day`, `sprint-close-day`.
- Transition `ACTIVE → NEW` (return) with the evidence type `RETURN_REASON`; the tag value
  `ceremony`; the ceremony header row *Where the round happened*.

### Changed
- The shipped instances run a **seven-day** iteration — Planning on Monday, the sprint close on
  Friday; the free-text cadence keys say `at sprint close`. The schema still accepts 5 to 30 days.
- Minutes templates are titled by iteration name (`# Planning — <iteration name>`); the
  retrospective minutes carry the cards instead of a free "what went well" list.
- The walkthrough names its iteration (`Sprint 02 26 Q1 Acme Portal`) and closes WI-42 at that
  week's sprint close.
- `core/ceremonies/README.md` no longer says an agent never attends: it attends in writing.
- The orchestrator brief runs the sprint close; the PO assistant knows the cadence and the names.

### Migration (0.3.0 → 0.4.0)
1. Add `organization.product` and the four cadence keys to `instance.yml`, or accept the
   defaults (pattern and reset from the model, Monday and Friday from the kit). `make instance`
   refuses a pattern that uses `{product}` without a product.
2. Name the iterations on your board from the pattern, or set your own pattern.
3. Add `ceremony` to `conventions.tags.process`; create the standing *Delivery process <year>*
   Feature and *Ceremonies <year>* Story under the *Unplanned work* Epic.
4. Re-copy the minutes templates, or run `check_canon.py --fix` on a vendored copy — the
   ceremony header gained a row.
5. Regenerate the prompt pack if you use it (`python3 adapters/prompt-pack/generate.py`).

## [0.3.0] — 2026-09-18

Minor under `0.x`, with a contract change: two state ids became categories. The migration note
below says what an adopter touches; `docs/adopt-and-upgrade.md` says what a minor bump asks in
general.

### Added
- **Lifecycle with categories.** Five fixed categories — `NEW`, `ACTIVE`, `RESOLVED`, `CLOSED`,
  `REMOVED` — and twelve default states, each in one category (`core/05-states.md`,
  `core/model/item-states.yml`). Rules, gates, transitions and tracks read categories; an instance
  runs a subset of states and labels them (`instance.yml` → `lifecycle`), never dropping a
  category. Board columns: one per visible state, eleven; `Removed` hidden.
- **Topologies** (`core/15-topologies.md`; `RULE-TOPOLOGY`, `RULE-TOPOLOGY-COORDINATION`):
  `agent-to-human`, `agent-to-agent`, `independent-agents`, `bot-team`. Required `topology` in the
  instance, cross-checked with the roster. One guide per topology in `docs/scenarios/`.
- **Agent-run onboarding.** `AGENTS.md` at the root, pointer files for four runtimes, the
  interview (`docs/onboarding/interview.md`) and the setup plan (`docs/onboarding/setup-plan.md`);
  `templates/agent-context/AGENTS.md` for the adopter's repository. `make links` checks the entry
  point and its pointers.
- **PO assistant** (`agents/roster.yml` → `po-assistant`, kind `advisor`; brief in
  `agents/briefs/po-assistant.md`): *guide* and *refine* modes; prompt pack regenerated.
- **Writing standard** (`core/16-writing-standard.md`, `RULE-WRITING-STANDARD`) with the ten-icon
  legend as a fragment; `templates/flow/refined-spec.md`; Story cards carry *Given / When / Then*
  scenarios and business rules; `examples/spec/refined-spec-example.md`.
- **Sprint metrics and external references.** Optional fields `EFFORT`, `REMAINING_WORK`,
  `BUSINESS_VALUE`, `EXTERNAL_REF` and the iteration's `ITERATION_CAPACITY`; optional rules
  `track_sprint_metrics` (`RULE-OPT-SPRINT-METRICS`) and `require_external_ref`
  (`RULE-OPT-EXTERNAL-REF`); the tag taxonomy under `conventions.tags`; the standing
  *Unplanned work* Epic (`core/04`). Thirty-five symbols.
- **Spreadsheet track** (`tracks/spreadsheet/`): a hosted spreadsheet as the source of truth,
  a read-only CSV/TSV sync connector, `examples/instance-internal-spreadsheet.yml`.
- `language` in the instance (BCP 47): agents answer and write artifacts in it; the kit stays in
  English.

### Changed
- `ACTIVE` and `RESOLVED` are **categories**, no longer state ids. The default Active state is
  `IN_DEVELOPMENT`; the first Resolved state is `AWAITING_TEST`. The validator normalises a state
  to its category, so a `pact-context` that names a category is still accepted; one that names a
  state the model does not know is refused (`RULE-STATES`).
- `Closed` is allowed from any Resolved-category state; rejection lands on `In development`.
- Board columns `In progress` and `In review` are replaced by one column per state
  (`core/model/board-columns.yml`); every track maps all eleven.
- `topology` is required in `instance.yml`. `check_instance` refuses an `agent-to-agent` instance
  without an agent orchestrator and an `independent-agents` one without a human orchestrator.
- The roster schema accepts `kind: advisor`; the model schema requires a category per state and
  accepts `number` fields marked `optional`.
- `make leaks` also scans `.mdc`, `.csv` and `.tsv` files.

### Migration (0.2.x → 0.3.0)
1. Add `topology` to `instance.yml` (`language` and `lifecycle` are optional); `make instance`
   says what is missing.
2. On the board, rename `Active` → `In development` and `Resolved` → `Awaiting test` — or keep
   your labels and declare them under `lifecycle.labels`. Add the other states you run; drop none
   of the categories.
3. Rename the columns `In progress` → `In development` and `In review` → `Awaiting test`, or add
   the others from the track's `setup.md`.
4. Contexts, queries and filters that say `ACTIVE` or `RESOLVED` keep working — they are
   categories now. Anything that compared a state *name* to `Active` or `Resolved` (a sheet
   formula, a saved query) must compare to the category or to the new state names.
5. A track of your own maps the twelve states, the eleven columns and the four new fields;
   `make mapping` lists what is missing.

## [0.2.0] — 2026-09-17

Minor, not patch: a field and four optional rules enter the contract and one symbol changes
meaning — `docs/adopt-and-upgrade.md` says what a minor bump asks of an adopter.

### Added
- Field `HOMOLOG_LINK` and optional rule `require_homologation_qa`: QA starts the
  homologation environment for the feature branch and links it; the **key user** tests
  there and writes the PO update on the item before `Closed`.

### Changed
- `ISSUE.agent_may_close` is `false`. No type is exempt from `RULE-STATE-RESOLVED-NOT-CLOSED`.
- `RULE-SCOPE` matches the gate: identical globs are forbidden; nested paths are allowed;
  the most-specific glob wins.
- The validator context requires `handoff_scopes`. A `pact-context` block without it fails with
  `RULE-GOLDEN-SCOPE`; it used to default to the claimed scopes. Add the key.

### Fixed
- README, badges and verification prose now match what the gate, the levels and the file
  counts actually are. The copy-ready workflow is a check of the context it is given, not
  of the board. Slack's `sot_eligible: false` is a row on the compatibility matrix.
- Sync `--apply` writes only the local `.state/` snapshot and never calls Slack
  `chat.postMessage`. SoT eligibility is read from `capabilities.yml`.
- The PR validator reads `instance.yml` (or `--instance`) for optional-rule toggles;
  accepts only JSON booleans for flags; allows `Closed` only from `Resolved`; and
  requires Transfer-review acceptance when homologation is on.
- Root `instance.example.yml` matches the internal profile (`require_homologation_qa: false`)
  so the 30-minute quickstart does not skip a gate the instance itself turned on.
- Check reporters print UTF-8 on Windows instead of crashing on arrows; an instance
  may not lower a profile toggle that is already `true`.
- The PR validator applies the defaults of the profile the instance names
  (`profiles/<profile>/profile.yml`). An instance that only sets `organization.profile: agency`
  is gated on client sign-off and homologation, and cannot lower a toggle the profile turned on.
- Instance discovery in the vendored layout looks for `instance.yml` at the adopter's root,
  next to `.pact/` — never inside it.
- Pin `pytest` to 9.0.3 (`CVE-2025-71176` / insecure UNIX tmpdir).
- Epic and Feature cards carry only the trace dates; branch, change and homologation belong to
  the items agents execute.
- The key-user brief's stop condition names next step `review` (Transfer review), as the
  template and `core/14` do.

## [0.1.0]

### Added
- Initial kit: PACT method (`core/`), neutral model (`core/model/`), templates, four tracks
  (Azure DevOps, GitHub Projects, Notion, Slack), agent roster and policies, runtime adapters,
  agency and internal profiles, copy-ready CI, PR validator, parameterised sync, and the
  verification suite that checks all of it.
