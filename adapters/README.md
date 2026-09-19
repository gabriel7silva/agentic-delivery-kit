# Adapters

The **only** place in the kit where a runtime is named. An adapter turns the neutral roster
(`agents/roster.yml` + `agents/briefs/`) into whatever one agent runtime expects — a config file,
a directory layout, a prompt per agent — without the roster knowing the runtime exists.

## The contract, in one line

**An adapter is a pure, one-way generator.** It reads `agents/`, writes its own `out/`, and never
edits anything upstream. Full text in [`_contract/adapter-spec.md`](_contract/adapter-spec.md).

## What ships

| Adapter | Target | Why it exists |
|---|---|---|
| [`prompt-pack/`](prompt-pack/README.md) | **Any chat, any model.** One Markdown prompt per agent, nothing else | Proves the roster is neutral: if it works here, it works anywhere. Also the fallback when your runtime has no sub-agent feature |
| [`_template/`](_template/README.md) | A skeleton to copy for a runtime of your own | Contributing a runtime should be one directory, zero changes to the core |

No vendor-specific adapter ships in this repository. That is deliberate: the kit stays honest
about being agnostic, and a runtime adapter belongs with the people who use that runtime day to
day. `_template/` is written so that one takes an afternoon.

## Generated output is committed

Each adapter's `out/` is committed and checked for drift: `make adapters` compares `out/` to a
fresh generation (newlines normalised) and fails if they differ. So a change to a brief that is
not followed by regeneration is a CI failure, not a silent inconsistency.

## What an adapter may not do

- Rewrite a brief. It copies briefs verbatim and may wrap them; it may not paraphrase.
- Claim a guarantee the runtime does not enforce. `mapping.yml` says for each concept whether the
  runtime **enforces** it, **advises** it, or **does not support** it — and what stands in
  (usually the PR validator).
- Read `instance.yml`. Adapters produce role material; instance values are rendered separately if
  wanted (`automation/scripts/render.py`).
