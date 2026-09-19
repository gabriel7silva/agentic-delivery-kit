# Event format — daily digest

Posted to `#delivery-digest` once per working day, at the start of the day in `cadence.timezone`.
Four sections in the order `RULE-DAILY-DIGEST` fixes. Built from the SoT by the sync or a workflow;
never written by hand. Empty sections say `none` — an absent section looks like a broken digest.

```
Daily digest · <date> · <iteration name> — goal: <one sentence>

1 · Active (<count>)
  <SoT id> <title> — <latest evidence: one line> — <role>
  …

2 · Blockers (<count>)
  <SoT id> <title> — blocks <ids> — needs <role>
  …

3 · Decisions needed from a human (<count>)
  <SoT id> <title> — <trigger> — waiting on <role> since <date> — <gate thread link>
  …

4 · Ready for review (<count>, oldest first)
  <SoT id> <title> — risk <level> — Resolved since <date> — <link>
  …

Inconsistencies (<count>)
  <SoT id> — <e.g. Status Done but WI-State Resolved>
```

## What the PO does with it

Reads sections 3 and 4 first — they are the queue that only a human can drain. Section 1 is for
curiosity; section 2 is for whoever can unblock. If section 4 grows day over day, the Approver is
the bottleneck (`core/ceremonies/retrospective.md`), not the agents.
