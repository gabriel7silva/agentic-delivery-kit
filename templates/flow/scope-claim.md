# Scope claim

Recorded **on the work item in the source of truth** — as a label, a field, or a comment, whichever
the track supports (see each `tracks/<name>/mapping.yml`, symbol `CLAIM`). Never in a file in the
repository: the anti-conflict mechanism must not itself be something two agents race to edit.

Canon: RULE-CLAIM · RULE-SINGLE-WRITER

## Claim

```markdown
## Claim

| Field | Value |
|---|---|
| Scope | <scope-id from agents/ownership.yml> |
| Holder | <role: implementer> |
| Item | <ITEM-ID> |
| Claimed at | <YYYY-MM-DD HH:MM timezone> |
| Expires at | <claimed at + TTL from agents/concurrency.yml> |
```

## Release

```markdown
## Claim released

| Field | Value |
|---|---|
| Scope | <scope-id> |
| Released at | <YYYY-MM-DD HH:MM timezone> |
| Reason | resolved · rejected · expired · released by holder |
```

## Rules a reader should know

- **One open claim per scope.** A second claim on an open scope is refused; the later item posts an
  `Issue` and waits (`RULE-ARBITRATION`).
- **The handoff names the scopes** the agent may claim. A claim on a scope not in the handoff is out
  of scope, whether or not it is free.
- **Expiry is enforced by the orchestrator**, which posts the release comment itself.
