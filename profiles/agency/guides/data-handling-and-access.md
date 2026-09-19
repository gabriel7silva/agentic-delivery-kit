# Data handling and access

What an agent working on a customer's delivery may see, hold and send. Agreed with the customer
in week one and written into their `AGENT-CONTEXT.md`, so it is context every session starts
with — not a policy in a drawer.

## Three classes

| Class | Examples | Agents may |
|---|---|---|
| **Public** | Docs, marketing copy, open-source code | Read, hold, send |
| **Internal** | Source code, tickets, test data, architecture | Read and hold **inside the delivery environment**; never send outside it |
| **Restricted** | Production data, credentials, personal data, anything under a regulation | **Never see.** Work uses synthetic or masked data; a task that would require real data hits the *access* human-in-the-loop trigger |

The customer classifies. When they have not, everything they gave you is *Internal* and anything
that looks like a person's data is *Restricted* until they say otherwise.

## Rules that follow

- **No production credentials in any agent's reach.** Not in a repository, not in an environment
  the agent runs in, not pasted into a prompt. An implementer that needs to exercise an
  integration gets a sandbox credential the customer issued for that purpose, or the item waits.
- **Evidence is minimised.** A screenshot for a receipt shows the feature, not the customer's
  real records. Test fixtures are synthetic. If a log line would carry restricted data, the log
  line is redacted before it becomes evidence.
- **Sending is publication.** Anything that leaves the delivery environment towards the customer
  or a third party triggers the *external publication* gate. A preview link counts.
- **The security reviewer reads for this.** Its brief already looks for credentials, user data and
  irreversible actions; in an agency context it also checks that nothing in the diff or the
  receipt carries *Restricted* data.

## Write it down

The customer's `AGENT-CONTEXT.md` gets a section:

```markdown
## Data you may see
- Public: <list or "as classified in <link>">
- Internal: <list> — stays inside <environment>
- Restricted: <list> — you never see this; ask for synthetic data via an Issue
```

An agent reading that section every session is the control. A policy nobody reads is not.
