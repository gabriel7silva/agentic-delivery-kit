## WI-42 — Export the customer list as CSV

Adds an **Export CSV** button to the customer list screen. The export uses the rows and columns
currently on screen and writes them with the standard library's CSV writer, so quoting is handled
for commas and quotes in names.

Files: `src/customers/list.py`, `src/customers/export.py` (new), `tests/customers/test_export.py`
(new), `tests/fixtures/customers_3rows.json` (new).

```pact-context
{
  "item": {"id": "WI-42", "type": "STORY", "wi_state": "IN_DEVELOPMENT", "risk": "medium"},
  "actor_role": "implementer",
  "target_state": "AWAITING_TEST",
  "handoff_scopes": ["app", "tests"],
  "claims": {"this_item": ["app", "tests"], "open_elsewhere": {}},
  "verification": {"passed": true},
  "verdicts": [
    {"reviewer": "reviewer-correctness", "verdict": "pass-with-findings", "risk": "low",
     "findings": [{"severity": "non-blocking", "where": "src/customers/export.py:18",
                   "what": "the header row uses column keys, not display labels; fine for AC1, note it in the receipt"}]},
    {"reviewer": "reviewer-delivery-compliance", "verdict": "pass", "risk": "low", "findings": []}
  ],
  "human_review": {"present": false, "by": null}
}
```

## Receipt

### Summary

The customer list screen gains an Export CSV button. Clicking it downloads `customers.csv` with
the filtered rows and visible columns in on-screen order. Names containing commas or quotes are
quoted by the CSV writer.

### Where

| Field | Value |
|---|---|
| Branch | `story/WI-42-export-csv` |
| Change / pull request | https://example.com/acme/delivery/pull/42 |
| Merge reference | not merged |
| Scopes claimed | `app`, `tests` |

### Commands run

```
make lint   → exit 0
make test   → exit 0   (14 passed, 2 new)
```

### Acceptance, criterion by criterion

| AC | Result | Evidence |
|---|---|---|
| AC1 | pass | https://example.com/acme/delivery/pull/42/files#customers_3rows.csv — 1 header + 3 rows |
| AC2 | pass | https://example.com/acme/delivery/pull/42/files#customers_quoted.csv — `"Doe, Jane"` intact |

### Not verified / not claimed

- Not opened in a spreadsheet application; only the raw file bytes were inspected. The requester
  should open one export in their tool before sign-off.
- Not tested with more than 200 rows; no statement about performance on large lists.
- The header row uses column keys (`first_name`) rather than on-screen labels (`First name`) —
  reviewer finding, left as is; raise a follow-up if labels are wanted.

### Risks and follow-ups

- Header labels vs keys → WI-45 (Story, tagged `improvement`).

### Review gate

| Reviewer (role) | Verdict | Risk | Blocking findings |
|---|---|---|---|
| reviewer-correctness | pass-with-findings | low | 0 |
| reviewer-delivery-compliance | pass | low | 0 |

**Risk of this change:** `MAX(verdicts, floors)` = medium (floor of `src/**`)

## Conclusion

| Field | Value |
|---|---|
| Responsible | implementer |
| Date | 2026-01-16 15:40 UTC |
| What was done | Export CSV button on the customer list; export of on-screen rows and columns via the standard library; two tests. |
| Link | https://example.com/acme/delivery/pull/42 |
| Evidence | AC1: https://example.com/acme/delivery/pull/42/files#customers_3rows.csv · AC2: https://example.com/acme/delivery/pull/42/files#customers_quoted.csv |
| Next step | review |
