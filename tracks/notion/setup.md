# Notion — setup

From an empty workspace to a working board. About an hour, most of it creating properties.

## 0. Plan and page history

`capabilities.yml` marks this track `sot_eligible` because comments are attributable. **Property
change history** is a paid page-history feature. Confirm it on your workspace before you treat
Notion as the source of truth. If history is not on, keep a SoT that has it.

## 1. Databases

Create three full-page databases: **Work items**, **Iterations**, **Minutes**.

## 2. Work items — properties

Follow the table in `fields.md` exactly. Order matters for nobody but you; naming matters for the
sync scripts, which look up properties by name.

- Set the `ID` property's prefix.
- `WI-State`: **Select** with the twelve options from `mapping.yml` (or your instance's subset,
  `instance.yml` → `lifecycle`). Not Status.
- `Status`: the Status property with the eleven columns placed in the three groups as
  `mapping.yml` says.
- Enable **Sub-items** (⋯ → Sub-items). Rename the relation to `Parent item` if Notion names it
  differently.
- Add one **Checkbox** per reviewer in your roster: `Reviewed · correctness`, `Reviewed · security`,
  …
- `Branch`, `Change link`, `Start` and `Target` are ordinary properties. Creating a page leaves
  them empty. Fill `Target` in Planning (required before Ready). Fill `Start` the day
  `WI-State` becomes `In development`. Fill `Branch` with the **feature branch** of this item, never
  `main`. Fill `Change link` with the pull-request URL the moment it exists. Fill
  `Homologation` with the running environment URL after QA starts it for that branch — the
  **key user** tests there. A filled table in the page body does not update these properties.

## 3. Iterations — properties

`Name` (title), `Start` (date), `End` (date), `Goal` (text). Then on Work items add the relation
`Iteration` → Iterations.

## 4. Minutes — properties

`Name` (title), `Ceremony` (Select: Planning · Refinement · Review · Retrospective), `Date`,
`Iteration` (relation). Each page's body is the corresponding template from
`templates/ceremonies/`.

## 5. Views

Create the views in `views.md`. The **Inconsistent** and **Unreviewed** views are the ones that
catch what Notion cannot enforce; do not skip them.

## 6. Templates

On Work items, create one database template per type from `templates/work-items/`. On Minutes,
one per ceremony.

## 7. The review gate substitute

Read `substitutes.md`. Decide, and write in your `instance.yml` notes, **who** ticks each
`Reviewed · …` box and where the verdict comment goes. This is a people process in Notion; make it
explicit or it will not happen.

## 8. Automation (optional)

Notion automations can: set `Status` when `WI-State` changes (one-way, State → Column only — never
the reverse); notify a channel when `WI-State` enters a Resolved-category state. `automation/sync/connectors/notion.py`
can mirror to or from another track once you provide a token.

## 9. Verify

Create one Story from its template, tick nothing, move it to `Awaiting test`, and confirm it
appears in **Unreviewed** and in **Gate queue**. Then set `Status` to Done with `WI-State` still
`Awaiting test` and confirm it appears in **Inconsistent**. If both views light up, the track is
honest.

Then leave `Target` and `Branch` empty and confirm the Story appears in **Untraced**. Fill
`Target`, set `Start` to today, set `Branch` to the feature branch (not `main`), paste the PR
URL into `Change link`, and confirm it leaves that view.
