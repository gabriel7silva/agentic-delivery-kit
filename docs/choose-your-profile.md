# Choose your profile

One question: **is the person who accepts the work inside your organisation?**

| Answer | Profile | Approver | What it turns on |
|---|---|---|---|
| Yes — a colleague, usually the PO | [`internal`](../profiles/internal/delta.md) | Product Owner | changelog entries |
| No — a customer, a client, a sponsor outside | [`agency`](../profiles/agency/delta.md) | Client Approver | client sign-off, homologation QA + key user, iteration report, changelog |

Set it in `instance.yml` → `organization.profile`. Copy the profile's `instance.example.yml` to
start from its defaults.

## What a profile changes

Not the method. A profile is an overlay ([`profiles/_contract.md`](../profiles/_contract.md)):
it sets instance defaults, switches **optional** rules on or off, and adds templates and guides
for its context. It cannot switch off a mandatory rule — the instance check refuses — and it
cannot rewrite a rule — the canon linter refuses.

So `Resolved ≠ Closed`, the single writer, the risk floor and the honest receipt hold in both.
What differs is who signs, what they sign, and which extra artifacts the context needs.

## If you are both

An agency with an internal product, or a product team that also delivers for a partner: **one
instance per context.** They share the kit, the roster and the floors; they differ in `instance.yml`.
Trying to run both under one profile means one of the two approvers is wrong.

## If you are neither yet

Start with `internal`. It has fewer moving parts, and moving to `agency` later is a change to
`instance.yml` plus three templates — not a migration.
