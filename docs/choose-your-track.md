# Choose your track

Where your work items live decides how much of the method the tool enforces and how much people
have to. The [compatibility matrix](compatibility-matrix.md) is generated from the data and is
the authority; this page is the reasoning.

## The short answer

| If … | Then | Because |
|---|---|---|
| You are choosing from scratch | **Azure DevOps** | The method's vocabulary *is* its process model; fifteen of twenty-one fields are native; the review gate is a branch policy |
| Your code is on GitHub already | **GitHub Projects** | Issues, sub-issues, Project fields, PRs and Actions in one API; 0 substitutes — about half the method fields are Project custom fields |
| Your PO lives in Notion and engineers accept the gate living in the code host | **Notion** as SoT, with the review gate substituted | Two rules are people-enforced; the *Unreviewed* view catches what the tool cannot |
| You want digests and human gates in chat | **Slack** as a mirror, **never** as SoT | It has no durable history; the instance check rejects it as source of truth |
| You have no tool yet, or a team of two | **Spreadsheet** — hosted, with version history | Twenty minutes of columns; every method field is a column; five capabilities substituted. Leave it the day you need a tree, a board or an enforced gate |

## What each one costs

| | Azure DevOps | GitHub Projects | Notion | Slack | Spreadsheet |
|---|---|---|---|---|---|
| Source of truth | ✅ | ✅ | ✅ | ❌ never | ✅ hosted only |
| Native hierarchy | ✅ | ✅ (sub-issues) | ✅ (sub-items) | ❌ | ❌ (`Parent` column) |
| `Resolved` distinct from `Closed` | native `State` | custom field | plain Select (**not** Status) | mirror | data-validated column |
| Review gate | branch policy | CODEOWNERS + ruleset | **substituted** — checkboxes + comments | in the code host | **substituted** — checkboxes; the PR in the code host |
| Verification | Pipelines | Actions | in the code host | — | in the code host |
| Claims | custom field | `claim:<scope>` label | text property | event only | text column |
| Daily digest | query + dashboard | scheduled Action | linked views | **native** — its strength | filter views |
| Setup time | ~1 h | ~1 h | ~1 h | ~30 min after a SoT | ~20 min |

## The two questions that decide it

**Does the tool have a change-request object?** If not (Notion, Slack), the review gate — the
heart of *Check* — is substituted by people ticking boxes and posting verdicts. It works, and the
kit says exactly what is lost. But if your code host has pull requests, put the *real* gate there
and let the SoT mirror it.

**Does the tool keep attributable history forever?** If not (Slack), it cannot be where
`Resolved ≠ Closed` is recorded. Use it for what it does best — the digest, the gate thread — and
copy every decision to the item.

## Pairing

Most instances pair one SoT with Slack:

```yaml
source_of_truth: { track: github-projects, board: Delivery }
mirrors:
  - { track: slack, purpose: notifications, channel: delivery-updates }
```

Two SoT-eligible tracks at once (say, Azure DevOps and Notion) is possible — one is the SoT, the
other a read-only mirror through `automation/sync/`. Two *writers* is not possible, and the
sync refuses it.

## Then

Open `tracks/<your choice>/setup.md` and follow the numbered steps. Step 9 of every setup is the
same: move one item through every column and confirm the state underneath changes the way
`mapping.yml` says.
