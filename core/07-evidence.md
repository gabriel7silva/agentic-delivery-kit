---
id: RULE-EVIDENCE
canon: true
---

# Evidence and the conclusion comment

Golden rule 5 says every action leaves a trace on the item. This file says what the trace looks
like at the moment that matters most: when an agent claims to be finished.

## The conclusion comment — `RULE-CONCLUSION-COMMENT`

Posted **on the work item** (not in a chat, not in a PR description alone) before any transition to
`Resolved`. Six fields, all mandatory:

| Field | Content |
|---|---|
| **Responsible** | The role that did the work (`implementer`, `reviewer-security`, …) |
| **Date** | When it finished, with timezone |
| **What was done** | Two to five lines. What changed, in the language of the acceptance criteria |
| **Link** | The change, the PR, the artifact — whatever a reader would open first |
| **Evidence** | Test output, screenshots, logs, the receipt. One line per acceptance criterion |
| **Next step** | What the item now waits for: `review`, `test`, `qa`, `key-user`, `release`, `human gate: <trigger>`, `approver`, `nothing` |

The template is `templates/flow/conclusion-comment.md`. It carries the six fields as a fenced
fragment so it can be pasted into any tool.

## The barrier — `RULE-TRANSITION-BARRIER`

**No conclusion comment → no leave from `Active`.** Not to `Resolved`, not to `Closed`. New → Active uses the handoff and the claim, not this block. The six fields
belong **on the work item**. A PR validator that reads the change-request body proves that body,
not the item, unless the same comment was copied there. A track without a validator checks by
hand, but checks.

The barrier is also what makes rejection cheap: an Approver reading a complete conclusion comment
can reject in one line, against one criterion. Without it, rejection means re-deriving what the agent
did.

## Evidence comments during execution

Long-running items post interim evidence comments with the same six fields, `Next step` set to
`continuing`. This is what replaces the standup: the daily digest is built from these comments,
not from asking anyone.

## What evidence is not

- A statement that something works, without the output that shows it.
- A screenshot with no criterion it is attached to.
- A link to a chat.

The rule of thumb: could a reader with no access to the agent reproduce the conclusion from what is
on the item? If not, it is a claim, not evidence — and it goes in *Not verified / not claimed*.

Canon: RULE-EVIDENCE · RULE-CONCLUSION-COMMENT · RULE-TRANSITION-BARRIER
