# Sync — security

## Tokens

- **Environment variables only.** `AZURE_DEVOPS_TOKEN`, `GITHUB_TOKEN`, `NOTION_TOKEN`,
  `SLACK_BOT_TOKEN`. Never in `config.yml`, never in a fixture, never in a log line.
- `config.yml` is git-ignored. `config.example.yml` holds ids and names, never secrets.
- A connector that finds its variable missing **exits with a clear message and code 2** before
  making any request. It does not fall back to anonymous access.

## Least privilege

| Connector | Minimum scope |
|---|---|
| Azure DevOps | `vso.work` (read) for a mirror; `vso.work_write` only when configured as SoT |
| GitHub | `repo` read + `project` read for a mirror; `project` write only when configured as SoT |
| Notion | The integration shared with the one database; read for a mirror |
| Slack | `chat:write`, `lists:write` if you add a `--post` yourself; this kit's connector only prints |

## What the sync may never do

- Set `CLOSED` or `REMOVED` on a source-of-truth write. `guard_mirror_writes` strips those
  states when `is_sot=True`. Mirrors may *display* a Closed item the SoT already has.
- Write to a track that is not configured as the source of truth, except mirror fields.
- Copy evidence *out of* the SoT into a mirror as if the mirror were the record.
- Log a token, a full PR body, or a comment body. Ids and states only.

## Fixtures

There is no recorded API corpus in this repository. Sync tests are in-memory diffs plus the
no-token refusal. If you add recordings later, put them under `automation/tests/fixtures/api/`,
strip anything a leak rule would catch **before** committing, and run `make leaks`.
