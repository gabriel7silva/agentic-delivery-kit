# Examples

Four instance files, one refined specification, one set of sprint-close minutes and one item
walked from intake to `Closed`. Everything is fictitious —
`acme-corp`, `WI-42`, a button that exports a list as CSV — chosen to be understood without any
domain context, so that the **shape** of each artifact is what you notice.

## Instances

| File | Profile | Source of truth | Mirrors |
|---|---|---|---|
| [`instance-internal-github.yml`](instance-internal-github.yml) | internal | GitHub Projects | Slack |
| [`instance-agency-azure-devops.yml`](instance-agency-azure-devops.yml) | agency | Azure DevOps | Slack |
| [`instance-internal-notion-slack.yml`](instance-internal-notion-slack.yml) | internal | Notion | Slack |
| [`instance-internal-spreadsheet.yml`](instance-internal-spreadsheet.yml) | internal | Spreadsheet (hosted) | — |

All four pass `make instance`. The first is also the shape the kit's own CI would use.

## The walkthrough

[`walkthrough/`](walkthrough/README.md) — one Story, seven artifacts in order:

```
00 intake note → 01 refined Story → 02 handoff → 03 PR body (with context) → 04 receipt
→ 05 conclusion comment → 06 closed
```

The PR body in step 03 carries a real ```` ```pact-context ```` block and the receipt and
conclusion from steps 04–05; `make check` runs the PR validator against it. If the kit's own
example does not pass the kit's own gate, the kit is wrong.

## The refined specification

[`spec/refined-spec-example.md`](spec/refined-spec-example.md) — the raw e-mail that produced
Feature WI-40 and, through it, the walkthrough's WI-42: one Feature, four stories with
*Given / When / Then* scenarios, business rules to validate, risks, refinement questions routed
to roles, and the registration tree. What the PO assistant's *refine* mode writes
(`agents/briefs/po-assistant.md`), in the shape of `templates/flow/refined-spec.md`.

## The sprint close

[`ceremonies/sprint-close-example.md`](ceremonies/sprint-close-example.md) — the Friday session of
the week WI-42 shipped, *Sprint 02 26 Q1 Acme Portal*: the ceremony item, the review that accepted
WI-42, retro cards written by a person and by three agents from evidence, the carry-over of the
three items that did not finish, and the next iteration named before Planning. The shape of
`templates/ceremonies/sprint-close-minutes.md` with the fences and placeholders rendered
(`core/ceremonies/sprint-close.md`).
