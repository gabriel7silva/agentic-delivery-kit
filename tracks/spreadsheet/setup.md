# Spreadsheet — setup

From an empty workbook to a working source of truth. About twenty minutes.

## 0. Hosted, with history

Use a spreadsheet that keeps **version history** and **dated, attributable comments** — a
workbook in a shared drive or an online spreadsheet. A file on someone's disk has neither, and
`capabilities.yml` calls this track SoT-eligible only on that condition. Write the workbook's
location in `instance.yml` → `source_of_truth.board`.

## 1. Sheets

Create three sheets: **Work items**, **Iterations**, **Comments**. Freeze the header row of
each.

## 2. Work items — columns

Add the columns in `fields.md`, in that order, and the data validation lists:

- `Type`: Epic · Feature · Story · Task · Bug · Issue
- `WI-State`: the twelve state names from `mapping.yml` — or the subset your instance runs
  (`instance.yml` → `lifecycle`). Add conditional formatting per category: one colour for the
  Resolved states, another for Closed, so the eye reads the category.
- `Status`: the eleven column names.
- `Priority`: P1–P4 · `Risk`: low · medium · high · `Role`: your role ids.
- One checkbox column `Reviewed · <reviewer>` per reviewer in your roster.

## 3. Iterations and Comments

**Iterations**: `Name`, `Start`, `End`, `Goal`, `Capacity`, `Minutes` — one row per iteration;
the `Iteration` column on Work items validates against `Name`. **Comments**: `Item`, `Date`,
`Role`, `Responsible`, `What was done`, `Link`, `Evidence`, `Next step` — the six fields of the
conclusion comment as columns, so that the digest can read them.

## 4. Filter views

A spreadsheet has no board. Filter views are the board and the digest:

| View | Filter | Answers |
|---|---|---|
| One per `Status` value | `Status` = <value> | The column, one view at a time |
| **Gate queue** | `WI-State` in the Resolved states, or `Tags` contains needs-human; sort `Updated` ↑ | The human queue, oldest first |
| **Unreviewed** | `WI-State` in the Resolved states and any `Reviewed · …` unchecked | The review-gate substitute's watchdog |
| **Inconsistent** | `Status` = Done and `WI-State` ≠ Closed | A card in Done without a human |
| **Untraced** | `WI-State` past Awaiting development and (`Start` empty or `Target` empty or `Branch` empty) | Work with no trace on the row |
| **Digest** | four views — Active · Blockers (`Type` = Issue, not Closed) · Needs human · Ready for review | The four sections of `RULE-DAILY-DIGEST` |

## 5. The code host holds the gate

The pull request, the reviewers' verdicts and the verification run live in your code host. The
row holds their URLs (`Change`, `Evidence`) and the mirror of the verdicts (the checkboxes). Wire
the PR validator there (`automation/ci/INSTALL.md`); the sheet cannot enforce anything.

## 6. Rules the sheet cannot enforce — write them on the first row

Put a pinned note on the `WI-State` header: *"Closed is set by <Approver title> only.
Resolved ≠ Closed."* Put one on `Claim`: *"One open claim per scope; the release is a comment."*
People will read a header note; they will not read the kit.

## 7. Protect the sheet

Protect the header row and the `ID` column against edits. Do not protect `WI-State`: a
protection that blocks everyone blocks the Approver too; the rule is people-enforced here.

## 8. Sync (optional)

`automation/sync/connectors/spreadsheet.py` reads a CSV or TSV **export** of the Work items
sheet and mirrors it — to a channel, to another track. It never writes cells; people edit the
sheet. Point `export_path` at the export in the sync config.

## 9. Verify

Add one Story from `templates/work-items/user-story.md` as a row. Move it through the states by
typing them and confirm the **Inconsistent** view lights up when `Status` says Done while
`WI-State` does not say Closed. Leave `Target` empty and confirm **Untraced** shows it. If both
work, the track is honest.
