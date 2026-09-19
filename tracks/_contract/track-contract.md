# Track contract

What a directory under `tracks/` must contain to be a track. Checked by `make mapping` and
`make schemas`; the schema files live in `schemas/`.

## Required files

| File | Validated by | Must |
|---|---|---|
| `README.md` | links | Say in one paragraph what the tool is good at and what it is not, and link to `substitutes.md` if one exists |
| `mapping.yml` | `schemas/mapping.schema.json` + coverage | Map **every** neutral symbol to `native`, `custom` or `unsupported` |
| `capabilities.yml` | `schemas/capabilities.schema.json` | Answer every capability in `core/model/capabilities.yml` with a boolean |
| `fields.md` | links | List which of the method's fields are native, which are custom, which are substituted |
| `setup.md` | links | Get a reader from an empty tool to a working board in numbered steps |
| `substitutes.md` | links | **Required when any capability is `false`.** For each missing capability: the substitute mechanism, the evidence it produces, and what is lost |

Optional: `queries/` (saved queries for the standard views), `labels.yml`, `event-formats/`.

## Mapping semantics

Each symbol maps to exactly one of:

| kind | Meaning | Requires |
|---|---|---|
| `native` | The tool has it out of the box | `as:` — the tool's name for it |
| `custom` | The tool can hold it once you create something | `as:` and `how:` |
| `unsupported` | The tool cannot represent it | `substitute:` with `mechanism`, `evidence`, optionally `loses` |

For select-like symbols (states, columns, types), `values:` maps each neutral value to the tool's
value. A neutral value mapped to `null` means "this value is not represented" and is reported as a
gap by `make mapping`.

## Coverage

`check_mapping.py` builds the symbol set from `core/model/` and refuses a track that omits any
symbol. It also refuses:

- `unsupported` without `substitute`.
- A `capabilities.yml` that says `sot_eligible: true` while `durable_history` or `comments` is `false`.
- A state mapping where `CLOSED` and `RESOLVED` resolve to the same tool value — that would make
  `RULE-STATE-RESOLVED-NOT-CLOSED` unenforceable.

## Substitutes are declarations, not workarounds

A substitute says: *this tool cannot do X; here is what we do instead, and here is what we give up.*
It is read by the compatibility matrix and by the adopter. It is **not** a way to claim a
capability the tool lacks — `capabilities.yml` stays honest; the substitute lives beside it.
