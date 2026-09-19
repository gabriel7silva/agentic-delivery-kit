# Event format — item state change

Posted to `#delivery-updates` as a top-level message whenever the SoT changes an item's WI-State or
a claim is opened or released. One line of context, one line of what changed, one link. Discussion
goes in the thread.

```
[<TYPE>] <SoT id> · <title>
<from-state> → <to-state> · by <role> · risk <level>
<link to the SoT item>
```

Examples (fictitious):

```
[STORY] WI-42 · Export the list as CSV
In development → Awaiting test · by implementer · risk low
<link>
```

```
[STORY] WI-42 · Export the list as CSV
claim opened · scope reports · by implementer · expires in 4h
<link>
```

```
[STORY] WI-42 · Export the list as CSV
Awaiting test → In development · by approver · REJECTED — AC2: the header row is missing
<link>
```

## Rules

- **Roles, not names.** The message names the role; the SoT knows the account.
- **Never a mention.** Mentions page people; the digest is the pull, this is the log.
- **The `Closed` event is the only one with a celebration emoji**, if you must. `Resolved` is not
  done (`RULE-STATE-RESOLVED-NOT-CLOSED`), and the channel should not feel like it is.
