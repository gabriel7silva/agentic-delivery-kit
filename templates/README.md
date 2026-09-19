# Templates

Artifacts that **leave the repository**: a handoff becomes a brief, a receipt becomes a comment on
a work item, minutes become a page in whatever tool holds them. Because they leave, they must be
**self-contained** — a template that only works while it can link back to `core/` is useless pasted
into a card.

That creates a tension with the rule that every fact has one home. Three mechanisms resolve it.

## 1. Rules are cited, never restated

A template carries the line `Canon: RULE-…` where a rule applies. It does not copy the rule. The
reader who needs the rule opens `core/`; the reader who needs the template does not have to.

## 2. Repeated blocks are fenced copies of one fragment

Some blocks must appear inside many templates *and* leave the repo with them: the instance footer,
the ceremony header, the actions table, the retro cards, the trace fields (Epic and Feature carry only the trace dates). Each has **one** source in `_fragments/` and appears
elsewhere as a fenced inline copy:

```markdown
<!-- canon:begin fragment=actions-table -->
| Action | Owner (role) | Due |
|---|---|---|
| | | |
<!-- canon:end -->
```

`make canon` compares every fenced copy byte-for-byte with its fragment. Edit the fragment, run
`make fix-canon` (or paste by hand), and the copies follow. An adopter who never runs anything just
pastes the template — the fences are HTML comments and render as nothing.

## 3. Instance values are readable placeholders

`{{source_of_truth.board}}` is the value at that path in your `instance.yml`. The placeholder is
readable on its own, so a template is usable **unrendered**; `automation/scripts/render.py` fills
them in for people who want that. `make canon` fails on a placeholder whose path does not exist in
`instance.example.yml`.

## Directory map

| Directory | Templates | Made concrete from |
|---|---|---|
| `_fragments/` | The fenced sources. Not used directly | — |
| `work-items/` | [Epic](work-items/epic.md), [Feature](work-items/feature.md), [Story](work-items/user-story.md), [Task](work-items/task.md), [Bug](work-items/bug.md), [Issue](work-items/issue.md) | [`core/04-work-item-model.md`](../core/04-work-item-model.md) |
| `flow/` | **[Handoff](flow/handoff.md)** (DoR made concrete), **[Receipt](flow/receipt.md)** (DoD made concrete), [Conclusion comment](flow/conclusion-comment.md), [Scope claim](flow/scope-claim.md), [QA homolog ready](flow/qa-homolog.md), [Key-user test](flow/key-user-update.md), [Refined spec](flow/refined-spec.md) | [`core/06`](../core/06-ready-and-done.md), [`core/07`](../core/07-evidence.md), [`core/09`](../core/09-concurrency.md), [`core/14`](../core/14-homologation.md) |
| `ceremonies/` | Minutes for [Planning](ceremonies/planning-minutes.md) and the **[Sprint close](ceremonies/sprint-close-minutes.md)** (review → retrospective → refinement, one session, with the retro cards and the carry-over table); [Refinement](ceremonies/refinement-minutes.md), [Review](ceremonies/review-minutes.md), [Retrospective](ceremonies/retrospective-minutes.md) for teams that hold them apart | [`core/ceremonies/`](../core/ceremonies/README.md) |
| `agent-context/` | [`AGENTS.md`](agent-context/AGENTS.md) (the adopter's entry file), [`AGENT-CONTEXT.md`](agent-context/AGENT-CONTEXT.md) (stable), [`CURRENT-FOCUS.md`](agent-context/CURRENT-FOCUS.md) (volatile) | [`core/11-docs-in-the-code.md`](../core/11-docs-in-the-code.md) |

## The one convention that matters

Every template ends with the instance footer fragment. It is the line that tells a reader six months
from now which board, which cadence and which roles this artifact belonged to — without naming a
single person.
