# Profiles

A profile is an **overlay** for a context. It configures the method for one kind of organisation;
it never rewrites the method. Two ship: [`agency/`](agency/delta.md) (you deliver for an external
customer) and [`internal/`](internal/delta.md) (you build a product with internal stakeholders).

The contract is short and the linter holds it: [`_contract.md`](_contract.md).

| Profile | Approver | What it adds | Optional rules it turns on |
|---|---|---|---|
| **agency** | The customer, external | Client sign-off as gate evidence, scope-change request, status report, data-handling guide | `require_client_signoff`, `require_homologation_qa` |
| **internal** | Usually the PO | Stakeholder update, roadmap alignment, cross-squad dependency guide | — |

Choose in `instance.yml` → `organization.profile`. The instance check refuses a profile that
toggles a rule which is not optional, so a profile cannot quietly switch off `Resolved ≠ Closed`.

## Reading a profile

Each has one page, `delta.md`, that says **only what differs from the core**. If it takes more
than a page, the difference belongs in the core as an optional rule, not in the profile as a
rewrite.
