# Safe Intake Operating Invariant

## Core invariant

No raw, unreviewed, or unapproved document content may be embedded, indexed, summarised, queried, exported, or passed to a hosted model.

Downstream AI access requires:

```text
approval_state == approved_for_ai
```

## Why this exists

Safe Intake is not just document upload plus AI summary. It is a controlled intake process where sensitive material is reviewed before AI use.

## Required states

| State | Meaning |
|---|---|
| `received` | Material has entered the system |
| `extracted` | Text/metadata extracted |
| `classified` | Sensitivity classification completed |
| `redacted` | Working redacted copy created |
| `needs_review` | Human review required |
| `approved_for_ai` | Approved redacted content may enter AI workflow |
| `blocked` | Must not enter downstream AI workflow |

## Failure posture

If approval state is missing, ambiguous, stale, or contradicted by evidence, fail closed.
