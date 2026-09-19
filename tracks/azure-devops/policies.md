# Azure DevOps — branch policies as the review gate

Everything `RULE-REVIEW-GATE` needs is a branch policy on the default branch. No script required
for the gate itself; `automation/ci/azure-pipelines/` adds the PR validator on top.

Repos → Branches → default branch → **Branch policies**:

| Policy | Setting | Implements |
|---|---|---|
| **Require a minimum number of reviewers** | 1 for `low`; use *Automatically include reviewers* below for `medium`/`high` | `RULE-RISK-GATES` |
| **Automatically include reviewers** | One entry per scope in `agents/ownership.yml`: path filter = the scope's globs, reviewers = the scope's required reviewers, **Required** | `RULE-SCOPE` reviewers |
| **Check for linked work items** | Required | `RULE-MERGE-COMMON` — the change is linked from the item |
| **Check for comment resolution** | Required | No blocking finding left open |
| **Build validation** | The pipeline from `automation/ci/azure-pipelines/azure-pipelines.yml`, required, expires after 12 h | `VERIFICATION` gate + PR validator |
| **Limit merge types** | Squash or merge commit — your convention | — |

## Human gate for `high`

Branch policies cannot read the item's `PACT.Risk`. Two options:

1. **Path-based** — add the scope's paths with floor `high` to a second *Automatically include
   reviewers* entry whose reviewer is the **Approver's** account, Required. Any change under a
   `high` path then needs the human before merge.
2. **Validator-based** — the PR validator reads `PACT.Risk` via the API and fails the build
   validation until a comment from the approver exists. Stricter, needs a token.

Option 1 is enough for most instances and needs nothing but the policy screen.

## Claims

Branch policies cannot see claims. The validator (`validate_pr.py`) checks that the PR's touched
paths fall inside a scope whose `PACT.Claim` field on the linked item names this branch, and that
no other open item holds a claim on the same scope.
