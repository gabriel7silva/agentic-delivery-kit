# Client onboarding — week one

The things to agree with a new customer **before** the first item is pulled. Each one prevents a
specific argument later.

## 1. `Resolved` is not `Closed` — and what that means for them

Tell the customer, in writing, that they will see items marked *done on our side* that are not
counted as delivered until **they** accept. Show them the board: the Resolved-category columns — `Awaiting test` onwards — are their
queue. Agree who on their side drains it and how often. An Approver who reviews once a month
turns a two-week iteration into a six-week one, and it will look like the agency is slow.

## 2. Who signs

One named role on the customer's side is the Approver. Not a committee. If two people must agree,
one of them signs and the other is a reviewer whose verdict is recorded on the item before
sign-off. Put the title in `instance.yml` → `roles.approver.title`.

## 3. Acceptance criteria are the contract of each item

Walk the customer through one Story and its criteria. The criteria are what they sign against;
*"it should feel finished"* is not a criterion and will not be on a sign-off sheet. Agree that
criteria are written **before** work starts and changed only through Refinement, with them.

## 4. The honest list

Show the customer the *Not verified / not claimed* section of a receipt. Explain that it will
appear on every sign-off sheet, and that its presence is the reason the rest of the receipt can be
trusted. Customers who have been burned by "it works" appreciate this on first sight; the others
learn to.

## 5. Scope changes have a form

Show the scope change request. Agree that discovered work goes through it, that the customer
decides, and that nothing discovered is started before the decision. This is what keeps the
iteration honest and the invoice unsurprising.

## 6. What the agents may see

Go through `data-handling-and-access.md` together. Agree what customer data an agent may hold,
where it lives, and what is never sent anywhere. Write the answer into the customer's
`AGENT-CONTEXT.md` so every agent session starts with it.

## 7. Where the truth lives

Name the source of truth (the board) and the channels that mirror it. Agree that a decision in a
chat is not a decision until it is on the item. The first time a customer says *"but I told you in
Slack"*, this paragraph is what you point to.

## Checklist

- [ ] `Resolved ≠ Closed` explained; their Approver named and cadence agreed
- [ ] One Story's criteria reviewed together
- [ ] Receipt and *Not verified* section shown
- [ ] Scope change request shown and agreed
- [ ] Data handling agreed and written into `AGENT-CONTEXT.md`
- [ ] Source of truth named; "decisions live on the item" agreed
- [ ] `instance.yml` filled with the above
