---
id: RULE-GOLDEN
canon: true
---

# The five golden rules

Everything else in this method is a consequence of these five. When two rules elsewhere seem to
conflict, come back here — the one that better serves a golden rule wins.

## 1. An agent is not a person in a standup — `RULE-GOLDEN-EVENTS`

Agents report state by **event and log**, not by oral status. The daily sync is a digest and an
impediment queue, not a meeting. Anything that asks an agent "what did you do yesterday" is asking
the wrong question of the wrong entity: read the work item. A ceremony is no exception: an agent
takes part by writing on the ceremony item within the session's window
(`RULE-CEREMONY-PARTICIPATION`) — never by speaking in a room.

## 2. A human is in the loop wherever there is … — `RULE-GOLDEN-HITL`

… money, access, external publication, an irreversible product decision, or business ambiguity.
These are the only reasons an agent must stop and wait; they are also the reasons an agent must
**always** stop and wait. The full trigger list is `RULE-HITL`.

## 3. Scope is closed per card — `RULE-GOLDEN-SCOPE`

Every agent receives an objective, acceptance criteria, evidence and **limits** — what it must not
do. A card without a "forbidden" section is not ready. Scope creep by an agent is a defect of the
card, not initiative.

## 4. Nothing invented — `RULE-GOLDEN-NO-INVENTION`

Agents state only what a source or a tool supports. Everything else is written as `unknown` or as a
question to the PO. The written form of this rule is the *honest placeholder*: `- [ ] unknown — …`.
A confident sentence with no evidence behind it is a bug.

## 5. Idempotence and traceability — `RULE-GOLDEN-TRACE`

Every relevant action leaves a trace **on the work item**: a comment, an attachment, a link to a
change or an artifact. Running the same step twice produces the same result and the same trace.
If it happened in a chat and not on the item, it did not happen.

The trace includes the board fields the track maps to `BRANCH`, `CHANGE_LINK`, `START_DATE` and
`TARGET_DATE`. A comment or a template table that names them while those fields stay empty is not
a trace — the next reader of the board will not see them.

---

## Why these five

They are the difference between *delegating* to agents and *hoping*. Rules 1 and 5 make the work
observable without interrupting it. Rules 2 and 3 keep the blast radius bounded. Rule 4 keeps the
observations trustworthy. Remove any one and the other four stop being enough.

Canon: RULE-GOLDEN
