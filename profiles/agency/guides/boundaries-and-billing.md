# Boundaries and billing

Where in-contract work ends and a scope change request begins — decided by rule, not by mood, so
that the agent, the Delivery Lead and the customer reach the same answer.

## The test

An item is **in contract** when all three hold:

1. A Feature named in the agreement is its parent.
2. Its acceptance criteria do not require a capability the agreement does not mention.
3. Delivering it does not change data, integrations or environments the agreement did not name.

Fail any one → it is a **scope change request**, whatever anyone's intent was. The orchestrator
applies this test at Refinement; an item that fails it is not `Ready`.

## What agents do with this

- The handoff's *Out of scope / forbidden* section names the contracted boundary in plain words:
  *"Do not add fields the agreement does not name; raise a scope change request instead."*
- An implementer that discovers out-of-contract work **stops that part**, posts an honest
  placeholder on the item, and the orchestrator raises the request. The implementer does not
  "just do it because it is small" — small is a commercial judgement, not a technical one.
- The human-in-the-loop trigger *money* covers anything that would change what is invoiced.

## Effort language

The method has no estimates. With a customer, effort is expressed as **how many handoffs** an
item fits in. One handoff is a unit the customer can see in the receipts; it is honest in a way
that hours are not. Price per handoff or per iteration; do not price per line of code an agent
wrote.

## Three situations that recur

| Situation | Handling |
|---|---|
| The customer asks in a review for "one small thing" | Write it as an item, apply the test. If in contract, it goes through Refinement like any other. If not, a request — decided before the next iteration, not in the room |
| A Bug turns out to be a missing feature | Re-type it to a Story tagged `gap` (`AP-BUG-FOR-GAPS`), apply the test. A defect in what was agreed is in contract; a feature nobody agreed is not |
| The agent finds a security problem outside the contracted area | Raise it as an Issue with `needs-human`, tell the customer the same day, and let them decide. Fixing it unasked is out of scope; hiding it is worse |
