# Receipt — WI-42 Export the customer list as CSV

The receipt as posted on the item. Identical to the `## Receipt` section of [`03-pr-body.md`](03-pr-body.md);
it lives in both places because the PR is where reviewers read and the item is where the record
is. The validator reads it from the PR body.

## Summary

The customer list screen gains an Export CSV button. Clicking it downloads `customers.csv` with
the filtered rows and visible columns in on-screen order. Names containing commas or quotes are
quoted by the CSV writer.

## Where

| Field | Value |
|---|---|
| Branch | `story/WI-42-export-csv` |
| Change / pull request | https://example.com/acme/delivery/pull/42 |
| Merge reference | not merged |
| Scopes claimed | `app`, `tests` |

## Commands run

```
make lint   → exit 0
make test   → exit 0   (14 passed, 2 new)
```

## Acceptance, criterion by criterion

| AC | Result | Evidence |
|---|---|---|
| AC1 | pass | customers_3rows.csv — 1 header + 3 rows |
| AC2 | pass | customers_quoted.csv — `"Doe, Jane"` intact |

## Not verified / not claimed

- Not opened in a spreadsheet application; only the raw file bytes were inspected.
- Not tested with more than 200 rows.
- Header row uses column keys, not on-screen labels — left as is; follow-up WI-45.

## What to notice

Three things are not claimed, and one of them (header labels) came from a reviewer's non-blocking
finding. The implementer did not fix it — that would have widened the change — and did not hide
it. It became a follow-up item with an id, which is the only acceptable place for a "later".
