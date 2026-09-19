# Track — GitHub Projects

Issues for items, **sub-issues** for hierarchy, a **Projects (v2)** board with custom fields for the
two state axes, pull requests for the review gate, Actions for verification. Zero substitutes;
about half the method fields are Project custom fields, and Bug-as-native depends on issue types.
Everything in one place, all of it scriptable through one API.

| Capability | Status | Note |
|---|---|---|
| Source of truth | ✅ eligible | Issues + Project fields; full history on every issue |
| Hierarchy | ✅ native | Sub-issues (parent/child); the Project shows it as a tree view |
| Iterations | ✅ native | Project **Iteration** field with dates, or Milestones |
| Code review | ✅ native | Pull requests, `CODEOWNERS`, required reviews, rulesets |
| CI | ✅ native | Actions; `automation/ci/github-actions/` is copy-ready |
| Two state axes | custom | Two single-select Project fields: `WI-State` and `Status` |
| Claims | custom | A label per scope (`claim:<scope>`) or a text field — see `fields.md` |

## What to know

- An issue's built-in open/closed is **not** WI-State. Keep issues open until `Closed`; the
  Project field carries the real state. Closing the GitHub issue is the last step of `Transfer`.
- Project fields live on the **Project**, not on the issue. An issue in two Projects has two sets.
  One Project per instance.
- `CODEOWNERS` implements per-scope required reviewers with no script — one line per scope.
- **Development** (branch + PR) and the `Start date` / `Target date` Project fields stay empty
  unless you write them. Creating the issue is not enough — see `setup.md` step 8.

## Files

[`mapping.yml`](mapping.yml) · [`capabilities.yml`](capabilities.yml) · [`fields.md`](fields.md) · [`setup.md`](setup.md) · [`labels.yml`](labels.yml) · `queries/` ([digest](queries/digest.graphql))
