# Safe Intake Proof Map

## Purpose

Show what the Safe Intake demo proves and what it does not yet prove.

## Proof path

```text
Document received
→ sensitivity classified
→ PII/confidential content detected
→ redacted working copy created
→ human review required
→ approved redacted content allowed
→ audit evidence recorded
```

## Evidence table

| Step | Evidence to preserve |
|---|---|
| Receive | file name, timestamp, source channel |
| Extract | extraction method, text length, metadata |
| Classify | classification result, confidence, reason |
| Detect | detected PII/confidential categories |
| Redact | before/after boundary, redaction method |
| Review | reviewer, decision, timestamp |
| Approve/block | approval state and reason |
| AI use | approved content ID, query/export record |

## Proof limitation

A demo proves the workflow shape and control points. It does not prove enterprise-grade security, regulatory compliance, or production reliability unless those are separately tested.
