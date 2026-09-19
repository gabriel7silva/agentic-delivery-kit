# Azure DevOps — fields

Of the twenty-one fields in `core/model/fields.yml`, **fifteen are native**. You add four
required custom fields, one optional (`RETRO`), and `PACT.ExternalRef` when `require_external_ref`
is on.

| Method field | Azure DevOps | Native? | Action |
|---|---|---|---|
| `ITEM_ID` | ID | ✅ | none — optionally add `PACT.Code` (text) for semantic ids |
| `ITEM_TYPE` | Work Item Type | ✅ | none |
| `WI_STATE` | State | ✅ | create the twelve states, each in its Azure category (`setup.md` step 4); Task needs the *Resolved* category added |
| `STATUS` | Board Column | ✅ | configure columns (step 5) |
| `PARENT` | Parent link | ✅ | none |
| `ITERATION` | Iteration Path | ✅ | create iterations with dates (step 3) |
| `PRIORITY` | Priority | ✅ | none |
| `ROLE` | `PACT.Role` | custom | picklist: values from your `instance.yml` roles |
| `RISK` | `PACT.Risk` | custom | picklist: `low` / `medium` / `high` |
| `CLAIM` | `PACT.Claim` | custom | multi-line text |
| `BRANCH` | Development | ✅ | link the repo (step 6); create the branch **from the work item** or the control stays empty |
| `CHANGE_LINK` | Development | ✅ | same — the PR must be linked to the item |
| `START_DATE` | Start Date | ✅ | native on Epic/Feature; add to User Story if wanted; type it when Active |
| `TARGET_DATE` | Target Date | ✅ | type it in Planning, before Ready |
| `HOMOLOG_LINK` | `PACT.Homolog` | custom | QA pastes the running env URL for this branch; the key user tests there |
| `TAGS` | Tags | ✅ | pre-create `needs-human` |
| `RETRO` | `PACT.Retro` | custom, optional | multi-line text |
| `EFFORT` | Story Points / Effort | ✅ optional | show on the card when `track_sprint_metrics` is on |
| `REMAINING_WORK` | Remaining Work | ✅ optional | on Task; the Taskboard reads it |
| `BUSINESS_VALUE` | Business Value | ✅ optional | on Epic / Feature |
| `EXTERNAL_REF` | `PACT.ExternalRef` | custom, optional | single-line text; the title starts with `[<ref>]` when `require_external_ref` is on |

## Process template differences

| Method | Agile | Scrum | Basic |
|---|---|---|---|
| Story | User Story | Product Backlog Item | Issue |
| Issue (impediment) | Issue | Impediment | — (use Issue + tag `impediment`) |
| Resolved on Task | ❌ add it | ❌ add it | ❌ add it |

## Naming the custom fields

Prefix with `PACT.` so they group together in the field picker and are recognisable as the
method's, not the project's. The reference name Azure generates will be `Custom.PACTRole` etc.;
`mapping.yml` uses the display name.
