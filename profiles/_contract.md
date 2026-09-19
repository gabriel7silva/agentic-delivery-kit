# Profile contract

A directory under `profiles/` is a profile when it has `profile.yml`, `delta.md`,
`instance.example.yml`, and optionally `templates/` and `guides/`.

## A profile may

1. **Set instance defaults** — `instance.example.yml` pre-filled for its context.
2. **Toggle optional rules** — `profile.yml` → `optional_rules:` may set any rule that carries
   `optional: true` in `core/model/rules.yml`, and only those.
3. **Add** — templates and guides that only make sense in its context.

## A profile may not

- **Redefine canon.** No file under `profiles/` carries `canon: true`, restates a rule table, or
  contradicts a rule. `check_canon.py` refuses the front-matter; `check_links.py` refuses an
  unknown rule id; a human refuses the rest at review.
- **Toggle a mandatory rule.** `check_instance.py` rejects a `profile.yml` whose `optional_rules`
  names a key that no optional rule declares.
- **Name a tool or a runtime.** A profile is about *who you deliver for*, not *what you deliver
  with*. Tools are tracks.

## `profile.yml`

```yaml
version: 1
profile: <name>
optional_rules:
  <instance_key>: true | false
defaults:
  roles:
    approver:
      title: <what the approver is called in this context>
```

## `delta.md`

One page. Sections: **Who the approver is** · **What changes at each PACT phase** · **Added
templates** · **Added guides**. Nothing that is true of both profiles belongs here.
