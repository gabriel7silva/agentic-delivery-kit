# Slack — setup

Slack is set up **after** the source-of-truth track, never instead of it.

## 1. Pair it

In `instance.yml`:

```yaml
source_of_truth:
  track: <azure-devops | github-projects | notion>
mirrors:
  - track: slack
    purpose: notifications
    channel: delivery-updates
```

`make instance` refuses `source_of_truth.track: slack`.

## 2. Channels

Create the channels in `channels.md`. Pin the channel purpose as the first message.

## 3. The List

Create a List `Work items` with the fields in `fields.md`. Set its description to:
*"Mirror of the source of truth. Edits here are overwritten by the sync."*

## 4. Bot or Workflow

Either:

- **Workflow Builder** — a scheduled workflow posts the digest; an incoming webhook receives item
  events from the SoT's automation. No code.
- **The sync connector** — `automation/sync/connectors/slack.py` with a bot token in
  `SLACK_BOT_TOKEN` (see `automation/sync/SECURITY.md`). It updates the List and posts events.

## 5. Digest schedule

Post to `#delivery-digest` at the start of the working day in `cadence.timezone`. Content order is
fixed by `RULE-DAILY-DIGEST`; the template is `event-formats/digest.md`.

## 6. Human gates

The orchestrator opens a thread in `#delivery-gates` per open gate using
`event-formats/human-gate.md`. When the human answers, the orchestrator copies the `DECISION:` line
to the SoT item and closes the thread with a link.

## 7. Verify

Move one item to `Awaiting test` in the SoT and confirm: an event appears in `#delivery-updates`, the
List row updates, and the next digest lists it under *Ready for review*. Then answer a gate thread
and confirm the decision lands on the SoT item. If it stays in Slack, the copy step is missing.
