# Track — Slack

Slack is the **coordination layer**: digests, state-change events, human gates in a thread,
notifications. It is **never the source of truth** — the schema rejects an `instance.yml` that says
otherwise — and its threads are not the audit trail. What matters is copied to the SoT.

| Capability | Status | Note |
|---|---|---|
| Source of truth | ❌ **never** | Retention, edits without history, no attributable field changes |
| Hierarchy | ❌ | A `Parent` text field on a List item, mirrored from the SoT |
| Iterations | ❌ | A channel per iteration, or a List field; the dates live in the SoT |
| Code review | ❌ | A reaction in a thread is a *signal*; the verdict lives in the code host |
| CI | ❌ | Notifications only |
| Digest | ✅ **its strength** | A scheduled message is the daily sync (`RULE-DAILY-DIGEST`) |
| Human gate | ✅ | A thread where the Approver answers; the answer is copied to the SoT |

Every instance that uses Slack pairs it with a SoT-eligible track under `source_of_truth:` and
lists Slack under `mirrors:` with `purpose: notifications`.

## Files

[`mapping.yml`](mapping.yml) · [`capabilities.yml`](capabilities.yml) · [`fields.md`](fields.md) · [`channels.md`](channels.md) · [`setup.md`](setup.md) · [`substitutes.md`](substitutes.md) · `event-formats/` ([item event](event-formats/item-event.md), [human gate](event-formats/human-gate.md), [digest](event-formats/digest.md))
