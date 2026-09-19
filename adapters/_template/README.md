# Adapter — `<runtime name>`

Copy this directory to `adapters/<runtime-name>/`, replace every `<…>`, delete this paragraph.

## What it produces

One `<artifact the runtime expects>` per agent in `agents/roster.yml`, under `out/`. Copy `out/`
to `<where the runtime looks — a directory, a config path>` in the adopting repository.

## What this runtime enforces

Be exact. Each row is a promise the adopter will rely on.

| Concept | Here | Enforced by the runtime? | Stands in |
|---|---|---|---|
| Read-only reviewer | `<e.g. a tool allowlist with no write tool>` | enforces · advises · unsupported | PR validator |
| Parallel review | `<e.g. native sub-agents>` | | |
| Single writer per scope | `<e.g. file locks, or nothing>` | | PR validator |
| Claims | `<…>` | | PR validator |
| Human gate | `<…>` | | PR validator refuses Closed by an agent |

## Regenerate

```bash
python adapters/<runtime-name>/generate.py          # writes out/
python adapters/<runtime-name>/generate.py --check  # drift check, add to CI
```

## Conformance

`make adapters` and `make leaks` pass; the table above is truthful. See
`adapters/_contract/adapter-spec.md`.
