# Agency — what differs from the core

You deliver for a customer who is not in your organisation. The method is the same; the
**Approver is outside**, and everything below follows from that one fact.

## Who the approver is

The customer's named representative. The PO (often called the Delivery Lead) is inside the agency
and owns priority *within the contracted scope*; the customer owns acceptance and anything that
changes the contract. `roles.approver.kind` is `human` and `roles.approver.title` says who — a
role, never a person's name.

## What changes at each phase

| Phase | Core | Agency delta |
|---|---|---|
| **Plan** | PO writes the card; DoR closes it | The card carries **in-contract / out-of-contract**. An out-of-contract item is not `Ready` until a [scope change request](templates/scope-change-request.md) is accepted |
| **Act** | Implementer executes in a claimed scope | The human-in-the-loop trigger *external publication* includes **anything sent to the customer** — a preview link, a report. `data-handling-and-access.md` governs what the agent may hold |
| **Check** | Reviewers + risk; receipt | The receipt's *Not verified / not claimed* is **customer-facing**: it is the honest list the customer reads before signing |
| **Transfer** | Approver accepts on the item | QA starts the homologation environment for the feature branch and links it; the **key user** tests there and writes the update for the PO (`RULE-OPT-HOMOLOG-QA`). Acceptance is a **signed artifact** — [`acceptance-signoff.md`](templates/acceptance-signoff.md) — attached to the item (`RULE-OPT-CLIENT-SIGNOFF`). A verbal "looks good" is not `Closed` |

## Added templates

| Template | When |
|---|---|
| [`acceptance-signoff.md`](templates/acceptance-signoff.md) | Every item the customer accepts. The signature is the Transfer evidence |
| [`scope-change-request.md`](templates/scope-change-request.md) | Anything discovered that the contract did not name. Decided by the customer, priced by the agency |
| [`client-status-report.md`](templates/client-status-report.md) | Per iteration, built from the iteration report and the digest — never written from memory |

## Added guides

- [`client-onboarding.md`](guides/client-onboarding.md) — what to agree in week one so that
  `Resolved ≠ Closed` does not surprise anyone on the customer's side.
- [`boundaries-and-billing.md`](guides/boundaries-and-billing.md) — where in-contract ends and
  the scope-change request begins.
- [`data-handling-and-access.md`](guides/data-handling-and-access.md) — what customer data an
  agent may see, hold and send, and what it never may.
