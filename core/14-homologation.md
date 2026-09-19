---
id: RULE-HOMOLOG-QA
canon: true
---

# Homologation before the PO sees it

An optional rule (`RULE-OPT-HOMOLOG-QA`, instance key `require_homologation_qa`). The companion
ids `RULE-HOMOLOG-QA`, `RULE-HOMOLOG-READY` and `RULE-KEY-USER-UPDATE` share that key — they
are not always-on. When the toggle is off, this file does
not apply. When it is on, **no key-user test starts** and **no item reaches `Closed`** until
the change is running on the homologation environment that belongs to **this item's feature
branch**, a key user has tested **there**, and **Review** has accepted that evidence.

The instance names the environment (`conventions.homologation_environment`). The method does
not start it — QA does — and does not invent its URL. On the default lifecycle these two steps
are the states `Prepare homologation` (QA) and `Key-user homologation` (the key user), both in
the `Resolved` category (`core/05-states.md`).

## Who

QA and key user are **instance hats**, not new method roles. **Review** is already in the
method — twice. Neither hat, and no reviewer, may set `Closed`.

| Who | Phase | Owns | Never does |
|---|---|---|---|
| **Reviewer** | Check — `RULE-REVIEW-GATE` | Verdict and risk on the **diff and the receipt**. This review must **pass** before QA starts the environment | Tests on homologation; starts the environment; sets `Closed` |
| **QA** | after Check | Starts the homologation environment for this branch; writes `BRANCH` and `HOMOLOG_LINK`; hands the running environment to the key user | Starts the environment while the item is still `Active`; tests the product; sets `Closed` |
| **Key user** | after QA | **Tests** on the environment QA linked; writes the result on the item for Review | Starts the environment; tests before both links exist; tests the default branch; sets `Closed`; skips Review and talks only to the PO in a chat |
| **Review (Transfer)** | Transfer — `RULE-CEREMONY-REVIEW` | Reads the receipt **and** the key-user test on `HOMOLOG_LINK`; accepts or rejects. The Approver then may set `Closed` | Accepts from a summary or a chat; accepts before the key-user test exists |

Review of the change (Check) and Review of the value (Transfer) are not the same pass.
Skipping either is a defect of the card.

## Review first — `RULE-REVIEW-GATE`

QA does not start the homologation environment until:

- deterministic verification has passed,
- every required reviewer has returned a verdict,
- no blocking finding is open,
- the item is `Resolved`.

An environment started from an `Active` item, or from a branch that has not been through
the review gate, is anti-pattern `AP-HOMOLOG-BEFORE-REVIEW`. Stop, wait for Review, then start.

## Before the key user may test — `RULE-HOMOLOG-READY`

QA does this after Check. All four, on the **board fields**, not only in a comment:

1. `BRANCH` is this item's feature branch — never the default branch.
2. The homologation environment for **that** branch is **started**.
3. `HOMOLOG_LINK` is the URL of that running environment.
4. The two refer to each other: the environment was started from `BRANCH`; `BRANCH` was not
   swapped after the environment came up.

Then QA posts `templates/flow/qa-homolog.md` on the item. **Next step** is `key-user`. The
item stays `Resolved`. QA does not set `Closed`.

A shared default environment, or one left running from another item, is not this rule. Stop,
start the right one, write the new URL, then hand it over.

## Key user tests — `RULE-KEY-USER-UPDATE`

The key user opens `HOMOLOG_LINK` (the same URL QA wrote) and tests the acceptance criteria
**on that environment**. If either board field is empty, or the environment is not this
branch, they stop and send it back to QA. They do not start the environment themselves.

When the test is done they post `templates/flow/key-user-update.md` **on the item**. **Next
step** is `review` — the Transfer review, not another code review. A message that never
lands on the item did not happen (`RULE-GOLDEN-TRACE`).

## Review again — `RULE-CEREMONY-REVIEW`

Review (Transfer) opens the same `HOMOLOG_LINK`, reads the key-user verdict against each
acceptance criterion and the receipt's *Not verified / not claimed*, and accepts or rejects
on the item (`RULE-STATE-REJECT` if it goes back). Only after that pass may the Approver
move the item to `Closed`.

The key user does not replace this review. They produce the evidence Review reads.

## Order

```
Act (implementer) — feature branch, change, receipt
  → Review (Check) — reviewers on the diff; item → Resolved
  → QA starts the environment for BRANCH
  → QA writes BRANCH + HOMOLOG_LINK
  → QA hands over (next step: key-user) — QA does not test the product
  → Key user tests on that environment
  → Key user writes the result on the item (next step: review)
  → Review (Transfer) — receipt + key-user evidence on HOMOLOG_LINK
  → Approver / PO → Closed
```

Skipping Check review, the start, the links, the key-user test, or Transfer review — or
sending the PO a chat message instead of the item — is `AP-HOMOLOG-SKIP` or
`AP-HOMOLOG-BEFORE-REVIEW`.

Canon: RULE-HOMOLOG-QA · RULE-HOMOLOG-READY · RULE-KEY-USER-UPDATE · RULE-OPT-HOMOLOG-QA · RULE-REVIEW-GATE · RULE-CEREMONY-REVIEW
