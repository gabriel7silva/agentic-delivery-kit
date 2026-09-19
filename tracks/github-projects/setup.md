# GitHub Projects — setup

From an empty repository to a board that runs PACT. About an hour.

## 1. Project

Create a **Project (v2)** at the organization or user level. One per instance.

## 2. Fields

Project → Settings → Fields. Create:

| Field | Type | Options |
|---|---|---|
| `Status` (rename the built-in) | single select | `Backlog`, `In analysis`, `Ready`, `Blocked`, `In development`, `Awaiting test`, `Prepare homologation`, `Key-user homologation`, `Prepare release`, `Integration test`, `Done` — or your instance's subset |
| `WI-State` | single select | the twelve states in `mapping.yml`, in order — or the subset in `instance.yml` → `lifecycle` |
| `Type` | single select | `Epic`, `Feature`, `Story`, `Task`, `Bug`, `Issue` — skip if you use org issue types |
| `Priority` | single select | `P1`, `P2`, `P3`, `P4` |
| `Role` | single select | your `instance.yml` role ids |
| `Risk` | single select | `low`, `medium`, `high` |
| `Iteration` | iteration | length from `cadence.iteration_length_days` |
| `Start date`, `Target date` | date | |
| `Homologation` | text | the running environment URL for this item's feature branch |
| `WI-ID` (optional) | text | semantic ids |
| `Retro` (optional) | text | |
| `Effort`, `Remaining work`, `Business value` (when `track_sprint_metrics` is on) | number | |
| `External ref` (when `require_external_ref` is on) | text | the request's id in the external system; the title starts with `[<ref>]` |

## 3. Views

| View | Layout | Group / filter |
|---|---|---|
| Board | board | group by `Status`; visible fields include `Start date` and `Target date` |
| WI-State | board | group by `WI-State` — the honest one |
| Hierarchy | table | tree by sub-issue |
| Gate queue | table | `WI-State` in a Resolved-category state (`Awaiting test` … `Integration test`) OR label `needs-human`, sort by updated ascending |
| Iteration | roadmap | by `Iteration` |
| Trace | table | columns: Title, WI-State, `Start date`, `Target date`, Linked pull requests |
| Untraced | table | `WI-State` past Awaiting development, and (`Start date` empty OR `Target date` empty OR no linked branch) |
| Roadmap | roadmap | by `Target date`, grouped by parent — the Epic and Feature timeline |

## 4. Labels

Apply `labels.yml`. Generate one `claim:<scope>` label per scope in `agents/ownership.yml`.

## 5. Sub-issues

Enable sub-issues on the repository (Settings → Features). Create the hierarchy by adding sub-issues
from the parent: Epic → Feature → Story → Task.

## 6. Review gate

- `CODEOWNERS` at the repository root: one line per scope, paths from `agents/ownership.yml`,
  owners = the required reviewers' accounts or a team.
- Ruleset on the default branch: require a pull request, require review from Code Owners,
  require status checks (`delivery-guard` from `automation/ci/github-actions/`), dismiss stale
  approvals.

## 7. Actions

Copy `automation/ci/github-actions/delivery-guard.yml` and `docs-lint.yml` into
`.github/workflows/`. The guard reads the linked issue's Project fields; give it a token with
`project: read` and `issues: write`.

## 8. Branch, pull request and dates

`BRANCH` and `CHANGE_LINK` are **not** Project fields. They appear only when GitHub links a
branch or a pull request to the issue (the **Development** section). Creating the branch in the
repo without that link leaves Development empty — the item then has no trace.

- Create the branch **from the issue**: Development → *Create a branch*, or
  `gh issue develop <n> --name <branch>`.
- Open the pull request with `Fixes #<n>` / `Closes #<n>` in the body, or Development →
  *Link a pull request*.
- A branch created on its own, or a PR that never mentions the issue, does not fill the fields.

`START_DATE` and `TARGET_DATE` **are** Project fields (step 2). They stay empty unless someone
types them:

- `Target date` — Planning, before the item may become Ready.
- `Start date` — the day `WI-State` becomes `In development`.

Writing the names only in the issue body is not enough. The next reader opens the sidebar.

## 9. Digest

A scheduled Action runs `queries/digest.graphql` and comments on a pinned issue titled
**Daily digest**. The four sections come from `core/ceremonies/daily.md`.

## 10. Verify

Create one issue from `templates/work-items/user-story.md`, add it to the Project, and move it
through every `Status`. Confirm `WI-State` is changed **by you** underneath — the two are separate
fields on purpose, and nothing should auto-sync `Status: Done` to `WI-State: Closed`.

Then: set `Target date`, move to `In development` and set `Start date`, create the branch from
Development, open a PR that mentions the issue. Confirm the sidebar shows both dates and the
Development section is no longer "Create a branch". If either is missing, step 8 was skipped.
