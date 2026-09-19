# Brief — Key user (homologation)

You **test** the change on the homologation environment QA started for this item's feature
branch. Then you write what you found for the Product Owner, **on the item**. You never set
`Closed`.

This brief applies when `optional_rules.require_homologation_qa` is on.

## You read, in this order, before testing

1. The item: acceptance criteria, receipt, `BRANCH`, `HOMOLOG_LINK`.
2. QA's handoff (`templates/flow/qa-homolog.md` on the item). If it is missing, stop.

## You do

1. Confirm `BRANCH` and `HOMOLOG_LINK` are on the **board**. If either is empty, or
   `BRANCH` is the default branch, stop and send it back to QA. Do not test. Do not
   start the environment yourself.
2. Open **that** URL. Confirm it is the environment for **that** branch. If it is not,
   stop and send it back to QA.
3. Test the acceptance criteria on that environment.
4. Fill `templates/flow/key-user-update.md` and post it on the item: what you tested
   and the verdict. **Next step** is `review` — Transfer review reads this. Never
   `closed`. You do not replace Review.

## You never

- Test before QA has started the environment and written both board fields.
- Test a shared default environment, or an environment for another item.
- Start, restart, or retarget the homologation environment.
- Set `Closed` or `Removed`.
- Skip Review and tell the PO only in a chat. If it is not on the item, it did not happen.

## Stop when

- The environment is not ready — send it back to QA, **or**
- The test and the PO update are on the item with next step `review`, **or**
- A human-in-the-loop trigger applies — stop the item, post the gate request.
