---
name: Bug
about: Proven defect. A product gap is a Story tagged gap, not a Bug.
title: "[Bug] "
labels: ["bug"]
---

## What is wrong (one line)

<!-- WI-State starts at New. Agents stop at Resolved. Only a human sets Closed. -->

- **Related to:** <!-- STORY-ID or FEATURE-ID, if any -->
- **Severity:** blocking · major · minor
- **External ref:** <!-- [ticket] if this answers another system -->

### Reproduction

1. Given
2. When
3. Then — expected:

**Evidence of the defect:** <!-- log, screenshot, failing test -->

### Acceptance criteria

- [ ] AC1 — The reproduction no longer produces the defect. Evidence:
- [ ] AC2 — A regression test exists and fails on the previous version. Evidence:
- [ ] unknown — <what> → <who decides>

### Forbidden

- Do not fix adjacent problems in the same change — file them.

### Trace

| Field | Value |
|---|---|
| Branch | <!-- never main --> |
| Change / PR | |
| Start date | |
| Target date | |

PACT · Resolved ≠ Closed
