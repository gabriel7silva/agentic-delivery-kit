# Slack — fields (List schema)

One Slack **List**, `Work items`, mirroring the SoT. Every field below is written by the sync
(`automation/sync/connectors/slack.py`) and read by people. Editing a mirrored field by hand does
nothing to the SoT and is overwritten on the next sync — say so in the List's description.

| Method field | List field | Type | Mirrored from SoT? |
|---|---|---|---|
| `ITEM_ID` | `SoT id` | Text | ✅ |
| `ITEM_TYPE` | `Type` | Select | ✅ |
| `WI_STATE` | `WI-State` | Select | ✅ |
| `STATUS` | `Status` | Select | ✅ |
| `PARENT` | `Parent` | Text (SoT id) | ✅ — no hierarchy |
| `ITERATION` | `Iteration` | Select | ✅ — no dates |
| `PRIORITY` | `Priority` | Select | ✅ |
| `ROLE` | `Role` | Select | ✅ |
| `RISK` | `Risk` | Select | ✅ |
| `CLAIM` | — | — | lives in the SoT; Slack shows the event |
| `BRANCH` | `Branch` | Text | ✅ |
| `CHANGE_LINK` | `Change` | Link | ✅ |
| `START_DATE` | `Start` | Date | ✅ |
| `TARGET_DATE` | `Target` | Date | ✅ |
| `HOMOLOG_LINK` | `Homologation` | Link | ✅ |
| `TAGS` | `Tags` | Multi-select | ✅ |
| `RETRO` | — | — | SoT only |
| `EFFORT` · `REMAINING_WORK` · `BUSINESS_VALUE` | `Effort` · `Remaining` · `Value` | Number | ✅ when the instance tracks them |
| `EXTERNAL_REF` | `External ref` | Text | ✅ |
| — | `Thread` | Link | the item's announcement thread |

## Why a List at all

Because a channel scrolls. A List gives the PO a **filterable** view of the mirror — *Resolved,
oldest first* — without opening the SoT, which is what makes the Slack-first morning routine work.
It is a convenience, not a record.
