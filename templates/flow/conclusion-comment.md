# Conclusion comment

Posted **on the work item** before leaving `Active` (and again if a human later records Transfer). Six fields, all mandatory; the PR validator
checks for them by name. Paste the block below as a comment — it needs nothing else from the repo.

Canon: RULE-CONCLUSION-COMMENT · RULE-TRANSITION-BARRIER

```markdown
## Conclusion

| Field | Value |
|---|---|
| Responsible | <role: implementer · reviewer-… · orchestrator> |
| Date | <YYYY-MM-DD HH:MM timezone> |
| What was done | <two to five lines, in the language of the acceptance criteria> |
| Link | <the change, the PR, the artifact — what a reader opens first> |
| Evidence | AC1: <link> · AC2: <link> · <one entry per criterion> |
| Next step | review · test · qa · key-user · release · human gate: <trigger> · approver · continuing · nothing |
```

## Interim evidence

For long-running items, post the same six fields with **Next step: continuing**. The daily digest
is built from these; nothing else is needed for the sync (`RULE-DAILY-DIGEST`).

## What blocks the transition

- Any field empty.
- **Evidence** that is a sentence instead of a link or an attachment.
- **Next step** that says `closed` — an agent never sets that (`RULE-STATE-RESOLVED-NOT-CLOSED`).
