# GitHub Projects — fields

Issues have few native fields; **Projects** supply the rest. Seven are native; the rest are
Project fields you create once — five of them only when an optional rule is on.

| Method field | GitHub | Native? | Where it lives |
|---|---|---|---|
| `ITEM_ID` | Issue number | ✅ | issue |
| `ITEM_TYPE` | Issue type or `Type` field | custom | org issue types, or Project |
| `WI_STATE` | `WI-State` field | custom | Project — **the** field that makes `Resolved ≠ Closed` visible |
| `STATUS` | `Status` field | ✅ (rename options) | Project |
| `PARENT` | Sub-issue parent | ✅ | issue |
| `ITERATION` | `Iteration` field | ✅ | Project |
| `PRIORITY` | `Priority` field | custom | Project |
| `ROLE` | `Role` field | custom | Project |
| `RISK` | `Risk` field | custom | Project |
| `CLAIM` | `claim:<scope>` label + comment | custom | issue |
| `BRANCH` | Development → branch | ✅ | issue — empty until you create or link the branch **from this issue** |
| `CHANGE_LINK` | Development → pull request | ✅ | issue — empty until a PR is linked or says `Fixes #<n>` |
| `START_DATE` | `Start date` field | custom | Project — type it the day the item becomes `In development` |
| `TARGET_DATE` | `Target date` field | custom | Project — type it in Planning, before Ready |
| `HOMOLOG_LINK` | `Homologation` field | custom | Project text — QA pastes the running env URL for this branch; the key user tests there |
| `TAGS` | Labels | ✅ | issue |
| `RETRO` | `Retro` field | custom, optional | Project |
| `EFFORT` | `Effort` field | custom, optional | Project number — when `track_sprint_metrics` is on |
| `REMAINING_WORK` | `Remaining work` field | custom, optional | Project number, on Tasks |
| `BUSINESS_VALUE` | `Business value` field | custom, optional | Project number, on Epics / Features |
| `EXTERNAL_REF` | `External ref` field | custom, optional | Project text; the title starts with `[<ref>]` when `require_external_ref` is on |

## The open/closed trap

A GitHub issue's own `open` / `closed` is **one bit**. It cannot hold five states, and closing an
issue is what people do by reflex when "done". Rule for this track:

- The issue stays **open** through every state before `Closed` — all of `New`, `Active` and
  `Resolved` categories.
- The issue is **closed** as the last step of `Transfer` (`WI-State: Closed`) — and also for
  `Removed`, with `state_reason: not_planned`.
- A closed issue whose `WI-State` is not `Closed` or `Removed` is a defect the digest reports.

## Development and dates stay empty unless you write them

The issue sidebar's **Development** block is GitHub's native `BRANCH` / `CHANGE_LINK`. It does
not read the issue body. A feature branch that exists in the repo but was not created from this
issue, and a pull request that never mentions `#<n>`, leave that block on *Create a branch*.

`Start date` and `Target date` are ordinary Project fields. They do not default to today or to
the iteration end. An item in an `Active`- or `Resolved`-category state with either date blank is
unfinished trace (`RULE-GOLDEN-TRACE`).

## Labels

`labels.yml` lists the label taxonomy: `type:*` for item types where issue types are unavailable,
`claim:*` per scope, `risk:*` as a visible mirror of the Project field, and the process tags.
