# Adapter specification

What a directory under `adapters/` must be to be an adapter.

## Files

| File | Required | Purpose |
|---|---|---|
| `README.md` | yes | What runtime; where the adopter copies `out/`; what the runtime enforces vs advises |
| `mapping.yml` | yes | Roster concept → runtime concept, with an `enforcement` per concept |
| `generate.py` | yes | The generator. `python generate.py` writes `out/`; `python generate.py --check` exits 1 on drift |
| `out/` | yes, committed | The generated material |

## `mapping.yml` shape

```yaml
version: 1
runtime: <name>                 # the only place this name appears in the kit
concepts:
  agent:
    as: <what the runtime calls an agent definition>
    enforcement: enforces | advises | unsupported
  read_only_reviewer:
    as: …
    enforcement: …
    stands_in: <what covers it when unsupported — usually "PR validator">
  parallel_review: …
  single_writer: …
  claim: …
  human_gate: …
```

`enforcement` is a promise about the **runtime**, not about the method. The method's guarantees
come from the PR validator either way (`agents/README.md`); this field tells the adopter how much
the runtime adds on top.

## `generate.py` behaviour

1. Load `agents/roster.yml` and every brief it references, through `adapters/_contract/base.py`.
2. For each agent, produce the runtime's artifact. **The brief text is included verbatim.** Wrap
   it with headers, front-matter, tool declarations — never rewrite a sentence of it.
3. Write to `out/`, deterministically: same inputs, byte-identical output. No timestamps.
4. `--check`: generate in memory, compare with the committed `out/` (newlines normalised so
   Windows CRLF still matches), exit 1 and list differing files on drift.

`base.py` gives you `load_roster()`, `brief_text(agent)`, `verdict_shape()`, `write_tree()` and
`check_drift()`. A new adapter is usually under a hundred lines.

## What the generator never does

- Import anything from `tracks/`, `profiles/` or `instance.yml`.
- Write outside its own `out/`.
- Depend on network access or an installed runtime to *generate*. Generation is text in, text out.

## Conformance

An adapter is accepted when `make adapters` passes (no drift), `make leaks` passes on its `out/`,
and its README states plainly what the runtime does **not** enforce.
