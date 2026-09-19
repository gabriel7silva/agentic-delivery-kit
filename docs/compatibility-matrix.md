# Compatibility matrix

**Generated** by `automation/scripts/check_mapping.py --write-matrix`. Do not edit by hand —
edit `core/model/rules.yml` (what a rule requires) or `tracks/<name>/capabilities.yml` (what a
tool can do) and regenerate. `make mapping` fails if this file is stale.

| Status | Meaning |
|---|---|
| ✅ supported | every capability the rule requires is native to the tool |
| ⚠️ substituted | a capability is missing and the track declares a substitute in `substitutes.md` — the rule works, with the stated loss |
| ❌ unsupported | a capability is missing and nothing stands in for it |

| Rule | Requires | azure-devops | github-projects | notion | slack | spreadsheet |
|---|---|---|---|---|---|---|
| `RULE-ROLES` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-GOLDEN` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-GOLDEN-EVENTS` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-GOLDEN-HITL` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-GOLDEN-SCOPE` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-GOLDEN-NO-INVENTION` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-GOLDEN-TRACE` | durable_history, comments | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| `RULE-HITL` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-ITEM-MODEL` | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-TWO-AXES` | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-STATES` | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-PACT-PHASES` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-STATE-RESOLVED-NOT-CLOSED` | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-STATE-REJECT` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-STATE-REMOVED` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-STATE-CATEGORIES` | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-DOR-DOD` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-DOR` | attachments | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| `RULE-DOD` | attachments | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| `RULE-EVIDENCE` | comments, attachments | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| `RULE-CONCLUSION-COMMENT` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-TRANSITION-BARRIER` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-REVIEW-RISK` | code_review | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-REVIEW-GATE` | code_review, ci | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-RISK` | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-RISK-GATES` | code_review, comments | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-CONCURRENCY` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-SINGLE-WRITER` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-SCOPE` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CLAIM` | custom_fields, durable_history | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| `RULE-ARBITRATION` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-MERGE` | code_review | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-MERGE-COMMON` | code_review | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-DOCS-IN-CODE` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CONTEXT-VS-TRAIL` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-ANTI-PATTERNS` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-HONESTY` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-TOPOLOGY` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-TOPOLOGY-COORDINATION` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-WRITING-STANDARD` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CEREMONIES` | iteration_native | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-CEREMONY-META` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CEREMONY-PLANNING` | iteration_native | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-CEREMONY-DAILY` | queries | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-DAILY-DIGEST` | queries, automation_hooks | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CEREMONY-REFINEMENT` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-REFINEMENT-DECISIONS` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CEREMONY-REVIEW` | comments, attachments | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| `RULE-CEREMONY-RETRO` | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-RETRO-INPUTS` | queries | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-RETRO-CARDS` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-ITERATION-NAMING` | iteration_native | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-CEREMONY-PARTICIPATION` | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-CEREMONY-SPRINT-CLOSE` | iteration_native, comments, attachments, queries | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-CARRY-OVER` | iteration_native, comments | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-OPT-CLIENT-SIGNOFF` *(optional)* | attachments | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| `RULE-OPT-CHANGELOG` *(optional)* | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-OPT-ITERATION-REPORT` *(optional)* | queries | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-HOMOLOG-QA` *(optional)* | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-HOMOLOG-READY` *(optional)* | custom_fields, comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-KEY-USER-UPDATE` *(optional)* | comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-OPT-HOMOLOG-QA` *(optional)* | custom_fields, comments | ✅ | ✅ | ✅ | ✅ | ✅ |
| `RULE-OPT-SPRINT-METRICS` *(optional)* | custom_fields, iteration_native, queries | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `RULE-OPT-EXTERNAL-REF` *(optional)* | custom_fields | ✅ | ✅ | ✅ | ✅ | ✅ |

## Source of truth

A column of ⚠️ does **not** make a track a source of truth. Slack is never SoT
(`sot_eligible: false`); the instance check rejects it there.

| | azure-devops | github-projects | notion | slack | spreadsheet |
|---|---|---|---|---|---|
| `sot_eligible` | ✅ | ✅ | ✅ | ❌ | ✅ |

## Reading it

A column with many ⚠️ is a track that works with people doing what the tool will not enforce.
A column with any ❌ on a non-optional rule is a track that cannot run PACT alone — pair it with
one that can. Slack has no ❌ in the rule rows above because no rule `requires: [sot_eligible]`;
the eligibility row is the one that says it cannot be the board.
