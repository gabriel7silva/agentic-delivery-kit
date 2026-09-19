# Sync

Mirror work items from the **source of truth** into read-only tracks, and post events to Slack.
One rule above all others: **exactly one track writes; every other track is a projection of it.**
A mirror that writes back is two sources of truth, and two sources of truth is none.

## What it does

```
source of truth ──read──► neutral ITEM records ──write──► mirrors
                                                └──post──► slack events
```

1. A **connector** for the SoT reads items and normalises them to the neutral shape
   (`sync_core.Item`): id, type, WI-State, status, parent, iteration, risk, claim, tags, links.
2. `sync_core` diffs against what each mirror last saw.
3. Each mirror's connector applies the diff. Slack's connector only ever posts; it never holds
   state that anything reads back.

## What it does not do

- Run in the kit's own CI against a live API. Tests cover in-memory diffs, "no token → exit 2",
  and parse sanitised payloads in `automation/tests/fixtures/api/` (GitHub org/user, Azure,
  Notion). Those fixtures are the connector contract, not a live call.
- Store tokens. Every token comes from an environment variable — [`SECURITY.md`](SECURITY.md).
- Send HTTP. `apply()` / `post_events()` / `post_digest()` print. `--apply` writes only the
  local `.state/` snapshot. Treat this as **read + print**, not a production sync.
- Write `Closed`. Even a future write path must not set `CLOSED` / `REMOVED`.

## Running

```bash
cp config.example.yml config.yml        # git-ignored
export GITHUB_TOKEN=…                    # whichever your SoT and mirrors need
python sync_core.py --config config.yml               # dry run: prints the diff, writes nothing
python sync_core.py --config config.yml --apply       # writes only the local .state/ snapshot; connectors still print
```

Default is dry-run. `--apply` is the flag you type on purpose. It does **not** PATCH the tools.

## Connectors

| Connector | Reads | Writes today | Env |
|---|---|---|---|
| `azure_devops.py` | work items via WIQL + REST | prints a PATCH; does not send it | `AZURE_DEVOPS_TOKEN` |
| `github_projects.py` | issues + Project fields via GraphQL | prints a PATCH; does not send it | `GITHUB_TOKEN` |
| `notion.py` | database pages via API | prints a PATCH; does not send it | `NOTION_TOKEN` |
| `slack.py` | nothing | prints the message / List row; does not post | `SLACK_BOT_TOKEN` |
| `spreadsheet.py` | a CSV / TSV export of the Work items sheet | nothing — people edit the sheet | — (no token; `export_path` in the config) |

Each connector is ~100 lines of reference code: enough to run, written to be read and adapted,
not a library. Where the tool's API shape is likely to have moved since this was written, the
connector says so at the call site.
