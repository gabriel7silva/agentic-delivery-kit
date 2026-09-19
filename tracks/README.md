# Tracks

A track is **translation, not method**. It says how one tool represents every neutral symbol from
`core/model/`, what the tool can and cannot do, and how to set it up. It never restates a rule.
If you find yourself explaining *why* Resolved is not Closed inside a track, stop: that sentence
belongs in `core/05-states.md` and the track links to it.

## The five tracks

| Track | Source of truth? | Code review | CI | Where it shines | Where it needs substitutes |
|---|---|---|---|---|---|
| [`azure-devops/`](azure-devops/) | yes | native | native | The method's vocabulary came from here — most fields are native | almost nothing |
| [`github-projects/`](github-projects/) | yes | native | native | Issues + sub-issues + Projects fields + PRs + Actions in one place | none |
| [`notion/`](notion/) | yes | **no** | **no** | Databases, views, pages for minutes | review gate, verification evidence |
| [`slack/`](slack/) | **never** | no | no | Notifications, digests, human gates in a thread | it is a mirror by design |
| [`spreadsheet/`](spreadsheet/) | yes — hosted, with history | **no** | **no** | Twenty minutes of columns; a first week, a pilot, a team of two | hierarchy, attachments, review gate, verification, iterations |

Pick with [`docs/choose-your-track.md`](../docs/choose-your-track.md). The generated
[`docs/compatibility-matrix.md`](../docs/compatibility-matrix.md) shows, per rule, whether each
track supports it natively, substitutes it, or cannot support it.

## The contract every track satisfies

Defined in [`_contract/track-contract.md`](_contract/track-contract.md). In one breath: a
`mapping.yml` covering **100 %** of the neutral symbols; a `capabilities.yml` answering every
capability question honestly; `README.md`, `fields.md`, `setup.md`; and for every symbol the tool
cannot represent, a `substitute` with the mechanism and the evidence it produces. `make mapping`
tells you what is missing.

## Symbols

The symbol set is the union of the entities listed in `core/model/README.md` and the ids in
`item-types.yml`, `item-states.yml`, `board-columns.yml` and `fields.yml`. Where a field and an
entity share an id (`ITERATION`, `CLAIM`) they are **one** symbol: the field is how the entity
attaches to an item. Thirty-five symbols in total at contract version 1 (the twelve states and eleven columns are
carried inside `WI_STATE` and `STATUS` as `values`, not as separate symbols).

## Adding another track

Copy the directory of the track most like your tool, run `make mapping`, and fix every line it
prints. Then answer `capabilities.yml` honestly — an optimistic `code_review: true` on a tool that
has no change-request object does not make the review gate exist; it makes the matrix lie.
