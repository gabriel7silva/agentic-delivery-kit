# Conclusion comment — WI-42

Posted on the item, after the review gate passed and before the state changed to `Awaiting test`.

```markdown
## Conclusion

| Field | Value |
|---|---|
| Responsible | implementer |
| Date | 2026-01-16 15:40 UTC |
| What was done | Export CSV button on the customer list; export of on-screen rows and columns via the standard library; two tests. |
| Link | https://example.com/acme/delivery/pull/42 |
| Evidence | AC1: customers_3rows.csv · AC2: customers_quoted.csv — both attached to this item |
| Next step | approver |
```

Then, by the implementer: claim on `app` and `tests` released; WI-State
`In development → Awaiting test`; the column follows the state.

## What to notice

*Next step* says `approver`, not `closed`. The implementer's last act is to hand the item to a
human. On the mirror in Slack this appears as:

```
[STORY] WI-42 · Export the customer list as CSV
In development → Awaiting test · by implementer · risk medium
<link>
```
