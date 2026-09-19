# Internal team — what differs from the core

You build a product; your stakeholders are colleagues. The **Approver is usually the PO**, and the
pressures are different: fewer gates about money, more about alignment and dependencies between
teams.

## Who the approver is

By default the Product Owner. When a Feature affects another team's surface — a shared API, a
platform component — that team's owner is a **required reviewer** on the item, recorded as a
verdict, but the PO still accepts. One approver, one signature (`RULE-ROLES`).

## What changes at each phase

| Phase | Core | Internal delta |
|---|---|---|
| **Plan** | PO writes the card; DoR closes it | Intake comes from discovery, support and other teams — [`discovery-and-intake.md`](guides/discovery-and-intake.md) says how a request becomes a card without skipping Refinement |
| **Act** | Implementer executes in a claimed scope | Scopes often cross **team** boundaries. `ownership.yml` names another team's reviewer where a scope is theirs; the claim still belongs to one implementer |
| **Check** | Reviewers + risk; receipt | The *money* and *external publication* triggers rarely fire; **irreversible** and **ambiguity** fire more — a public API change, a metric definition nobody wrote down |
| **Transfer** | Approver accepts on the item | The PO accepts by moving the item, no artifact needed. A [stakeholder update](templates/stakeholder-update.md) goes out per iteration when someone outside the team is waiting on the outcome |

## Added templates

| Template | When |
|---|---|
| [`stakeholder-update.md`](templates/stakeholder-update.md) | Per iteration, for people outside the team who are waiting on something in it |
| [`roadmap-alignment.md`](templates/roadmap-alignment.md) | When an Epic's outcome measures move, or another team's roadmap changes what this one depends on |

## Added guides

- [`discovery-and-intake.md`](guides/discovery-and-intake.md) — from "someone asked" to a card
  that passes the DoR, without agents guessing what was meant.
- [`cross-squad-dependencies.md`](guides/cross-squad-dependencies.md) — how a dependency on
  another team is recorded, watched and unblocked without a meeting.
