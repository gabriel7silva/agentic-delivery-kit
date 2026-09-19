# 🔹 <Feature title> — refined specification

What the PO assistant's *refine* mode, or a Refinement session, produces from a raw request: a
Feature and one story per independent deliverable, each with testable scenarios, the rules still
to confirm, the risks, the questions, and how to register it. Posted on the Feature; each story
then becomes its own card from `templates/work-items/user-story.md`.

Canon: RULE-DOR · RULE-CEREMONY-REFINEMENT · RULE-WRITING-STANDARD

## 🔹 Suggested Feature

| Field | Value |
|---|---|
| Feature | <title — a capability, a few iterations> |
| Parent Epic | <EPIC-ID> — <title> |
| Business objective | <one paragraph: what changes for whom, and why now> |
| Requesting area | <area or unit — never a person> |
| Requester (role) | <role> |
| Impacted users | <who works differently after this> |

## 📊 Expected benefits

- <benefit, measurable where possible>
- <benefit>

---

## US 1 — <title>

**User story** — As <persona>, I want <goal>, so that <benefit>.

**Context** — <what is hard today, in two lines; what the request said, not what we assume>

**Acceptance criteria — scenarios**

*Scenario 1 — <name>*
- Given <context>
- When <action>
- Then <observable result>

*Scenario 2 — <name>*
- Given <context>
- When <action>
- Then <observable result>

**Business rules to validate**

- <a rule the story depends on that nobody has written down> → <who confirms it>

📊 **Suggested metrics** *(when the story changes what is measured)*

- <metric>

⚠️ **Risks and controls** *(when the story touches money, data, permissions or something irreversible)*

- <risk> → <control>

📌 **Recommended rule** *(when one sentence settles a recurring doubt)*

> <the rule>

---

## US 2 — <title>

<same shape>

---

## 🧠 Refinement questions

Grouped by theme; each one is answered by a role before the story is *Awaiting development*.

### <theme>
- <question> → <role>

### <theme>
- <question> → <role>

## ✅ Recommended registration

```
Epic <EPIC-ID> — <title>
└── Feature — <title>
    ├── US 1 — <title>
    ├── US 2 — <title>
    └── US n — <title>
```

> ⚠️ **Main rule:** the original request is not one User Story. It holds <n> independent
> deliverables, each with its own rules, risks and criteria. One Feature, separate stories —
> prioritised, estimated, developed and homologated one by one.

## 🔁 What changed from the original request

| Improvement | What was done |
|---|---|
| Clarity | <terms corrected; pains separated by objective> |
| Structure | <report → Feature, stories, scenarios> |
| Scope | <what was split apart and why> |
| Testability | <scenarios added for later homologation> |
| Prioritisation | <the pain the request named as the main one> |
| Governance | <permissions, audit, pending points, questions> |

<!-- canon:begin fragment=honest-placeholder -->
- [ ] unknown — <what is not known> → <who decides>
<!-- canon:end -->

<!-- canon:begin fragment=instance-footer -->
---
Source of truth: {{source_of_truth.track}} · Board: {{source_of_truth.board}} · Iteration: {{cadence.iteration_length_days}} days · Timezone: {{cadence.timezone}}
Roles: PO = {{roles.product_owner.title}} · Orchestrator = {{roles.orchestrator.title}} · Implementer = {{roles.implementer.title}} · Approver = {{roles.approver.title}}
Method: PACT — Plan · Act · Check · Transfer. Resolved ≠ Closed. Canon: RULE-STATE-RESOLVED-NOT-CLOSED
<!-- canon:end -->
