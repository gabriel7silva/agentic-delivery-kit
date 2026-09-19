# Event format — human gate

Posted to `#delivery-gates` as a top-level message when an item stops on a human-in-the-loop trigger
(`RULE-HITL`) or reaches risk `high`. The human answers **in the thread**; the orchestrator copies
the decision to the SoT item.

```
GATE · <SoT id> · <title>
trigger: <money | access | publication | irreversible | ambiguity | risk-high>
needs: <one sentence — what decision, from whom (role)>
context: <one sentence, or a link to the receipt section>
<link to the SoT item>
```

Example (fictitious):

```
GATE · WI-42 · Export the list as CSV
trigger: ambiguity
needs: PO — should the export include archived rows? AC1 says "all rows", the list view hides archived ones
context: receipt § Not verified
<link>
```

## Closing the thread

The last reply, by the human, starts with `DECISION:` and is one or two lines:

```
DECISION: exclude archived rows. AC1 amended on the item.
```

The orchestrator replies once more with the link to the SoT comment where the decision now lives,
and the thread is done. A gate thread with no `DECISION:` reply is still open, whatever reactions
it has.
