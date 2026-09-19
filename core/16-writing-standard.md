---
id: RULE-WRITING-STANDARD
canon: true
---

# The writing standard

Everything an agent writes for someone to read — an answer, a specification, a handoff, a status
report, a digest, minutes, a comment on an item — has one shape, so that a reader scans it the same
way every time and a symbol means the same thing in every document. The standard applies in every
direction: agent → human, human → agent, agent → agent. It looks like professional documentation,
and it is easy to scan on a phone. The only thing it never touches is a field a machine parses.

## Hierarchy — `RULE-WRITING-STANDARD`

- `#` for the title, with one semantic icon and the name of the concept; `##` for sections; `###`
  for subsections.
- `---` between sections; white space between blocks.
- Short sentences. Lists and themed blocks rather than long paragraphs.
- **Bold** on rules, names and the differences that matter.
- Bullets for related items; numbers only when the order matters.
- A **table** whenever two or more things are compared — states, roles, options, criteria — never
  side-by-side prose.
- A `>` block for the main rule, an alert, a summary or a critical note.
- The same alignment, spacing, titles and symbols from the first line to the last.

## Icons with meaning

Ten icons, each with one meaning, kept for the whole document. Never as decoration; never a
symbol switched half-way.

<!-- canon:begin fragment=icon-legend -->
| Icon | Means | Use it for |
|---|---|---|
| 🔹 | Definition | The main section, or the concept being defined |
| ✅ | Correct | A valid behaviour, characteristic or recommendation |
| ❌ | Incorrect | A wrong behaviour, an exclusion, something that does not apply |
| 🗑️ | Removed | A discarded, cancelled or removed item |
| 🔁 | Comparison | A transition, or a difference between states or options |
| 🧠 | Tip | Guidance for the team |
| 📌 | Rule | The main rule, a summary, a flow |
| ⚠️ | Alert | A risk, an exception, a mandatory point |
| 👉 | Example | A practical example |
| 📊 | Metric | A measure or an analytical impact |
<!-- canon:end -->

## The nine parts

Adapt the sequence to the content; omit only a part that adds nothing.

1. **Title** — one icon, the concept's name.
2. **Definition** — one or two direct sentences.
3. **What it is** — positive, objective items.
4. **What it is not** — when a misreading is a real risk.
5. **Examples** — in the reader's own context.
6. **Comparison table** — when states, options or roles resemble each other, with the columns
   *Concept · When to use · What it represents · Impact*.
7. **Impacts or tips** — for the process, the metrics, the decision.
8. **Flow** — in a monospace block when there is a sequence of states: arrows, and the branches
   that matter kept in.
9. **Main rule** — in a box, to close.

## Comparisons and flows

- Columns: *Concept · When to use · What it represents · Impact*.
- Make the essential contrast visible: `Closed` = delivered **and accepted** versus `Removed` =
  cancelled or discarded (`RULE-STATE-REMOVED`).
- Flows use arrows and keep their branches. A state sequence written as prose is a defect.

## Closing model

When it helps, end with the two lines that settle most confusion:

> 🟢 **Closed** → "Delivered and accepted."
> 🗑️ **Removed** → "Will not happen."

## Language

Prose in the instance language (`instance.yml` → `language`). Keys, ids, rule ids, state ids and
code stay in English, so that a document written in one language still says
`RULE-STATE-RESOLVED-NOT-CLOSED` and `AWAITING_TEST` the way the kit does.

## Parse-safety — what the standard never touches

The PR validator and the sync read a few things by exact text. Those keep it, with the icon
beside them, never inside them:

| Machine-read | Exact text that must stay |
|---|---|
| The conclusion comment | The six field names — *Responsible, Date, What was done, Link, Evidence, Next step* — in a `\| Field \| Value \|` table under `## Conclusion` |
| The receipt | `## Receipt`; the rows `\| AC1 \| pass \| …`; the heading *Not verified / not claimed* |
| The context block | The fenced ```` ```pact-context ```` JSON |
| Board fields | State names as the track maps them; a label is on the board, not in a comment |

An icon inside a field name is not a nicer document; it is a gate failure.

## When the reader is an agent

The same shape. Agents read tables and lists better than prose too. The handoff, the receipt and
the conclusion comment already *are* this standard with a few machine-read fields; a message from
one agent to another, recorded on the item (`RULE-TOPOLOGY-COORDINATION`), follows it as well.

Canon: RULE-WRITING-STANDARD
