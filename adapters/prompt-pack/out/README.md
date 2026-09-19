# Prompt pack — index

Generated from `agents/roster.yml` and `agents/briefs/`. Do not edit here; edit the brief and
regenerate (`python adapters/prompt-pack/generate.py`).

| File | Kind | Purpose |
|---|---|---|
| [`orchestrator.md`](orchestrator.md) | orchestrator | Pull Ready items, issue handoffs, track claims and their expiry, build the daily digest, escalate human gates, arbitrate scope collisions. |
| [`implementer.md`](implementer.md) | implementer | Execute one item inside one claimed scope, produce the change, the receipt and the conclusion comment, and stop at Resolved. |
| [`reviewer-correctness.md`](reviewer-correctness.md) | reviewer | Does the change do what the acceptance criteria say, and nothing else? Logic, edge cases, tests that prove the criteria, behaviour outside the stated scope. |
| [`reviewer-security.md`](reviewer-security.md) | reviewer | Trust boundaries — user data on disk or over the network, credentials, permissions, injection, paths that escape their root, anything irreversible. |
| [`reviewer-docs.md`](reviewer-docs.md) | reviewer | Is what a future reader needs written down next to the change — agent context updated, decision recorded, changelog line when the instance requires it, no stale document contradicted by the diff?. |
| [`reviewer-delivery-compliance.md`](reviewer-delivery-compliance.md) | reviewer | Did the process happen? Claim inside the handoff's scopes, receipt complete with "Not verified / not claimed", conclusion comment with six fields, every AC evidenced or explicitly out of scope, no transition an agent may not make. |
| [`po-assistant.md`](po-assistant.md) | advisor | Guide Product Owners and teams — people or agents — on ceremonies, the PO's role, work items and states, in the instance's language and tool; and turn a raw request into a refined specification (Feature, stories, scenarios, questions, registration tree). |

## Order for one item

1. **orchestrator** — confirms the Definition of Ready, writes the handoff, records the claim.
2. **implementer** — one conversation, given the handoff. Produces the change, the receipt, the
   conclusion comment.
3. **Every required reviewer for the touched scopes** — one conversation *each*, in parallel,
   given the diff and the item. Each returns a verdict block.
4. Run the PR validator (`automation/scripts/validate_pr.py`) with the verdicts. It is the gate;
   the prompts are the preparation.
5. A human accepts. The item moves to Closed by that human's hand, not by any prompt above.

**po-assistant** sits outside that chain. Paste it when a person needs the method explained in
their own language and context, or a raw request turned into a Feature with stories before
Refinement. It recommends; it never sets a state.

When `require_homologation_qa` is on, two **human** briefs apply and are not generated here:
[`agents/briefs/qa.md`](../../../agents/briefs/qa.md) and
[`agents/briefs/key-user.md`](../../../agents/briefs/key-user.md).
