# Track — Notion

A database with typed properties, board and table views, and pages for minutes. Good for teams
whose PO already lives in Notion and whose engineers will accept that **the review gate happens
somewhere else**.

| Capability | Status | Note |
|---|---|---|
| Source of truth | ✅ eligible | Page history and comments are attributable and kept |
| Hierarchy | ✅ | Sub-items relation (enable it on the database) |
| Iterations | custom | A relation to an `Iterations` database; no first-class sprint outside the Projects template |
| Code review | ❌ **none** | Notion has no change-request object. See `substitutes.md` |
| CI | ❌ **none** | Verification runs in your code host; Notion holds the evidence link |
| Two state axes | ✅ | `WI-State` (Select) and `Status` (Status property → board) |
| Claims | custom | Text property + page comment |
| Branch / dates | custom | `Branch`, `Change link`, `Start`, `Target` stay empty on create — fill the properties, see `fields.md` |

**Read [`substitutes.md`](substitutes.md) before adopting.** Two of the method's rules (`RULE-REVIEW-GATE`,
`RULE-MERGE`) depend on a change-request object, and the generated compatibility matrix marks them
*substituted* for this track. The substitutes work; they are not enforced by anything but people.

## Files

[`mapping.yml`](mapping.yml) · [`capabilities.yml`](capabilities.yml) · [`fields.md`](fields.md) · [`views.md`](views.md) · [`setup.md`](setup.md) · [`substitutes.md`](substitutes.md)
