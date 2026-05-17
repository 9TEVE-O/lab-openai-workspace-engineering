# Safe Intake Demo Proof Pack

## Plain-English summary

This proof pack shows a controlled document-intake demo. A sample document enters the workflow, is checked, redacted, reviewed, approved or blocked, and leaves behind an evidence trail.

The point is not to prove that AI can read a document. The point is to show that document content can be controlled before AI use.

## Workflow map

```text
Synthetic sample document
→ text and metadata extracted
→ sensitivity checked
→ PII/confidential categories identified
→ redacted working copy prepared
→ human review required
→ approved redacted content allowed
→ audit summary generated
```

## Evidence table

| Claim | Evidence | Status |
|---|---|---|
| The workflow has staged intake | Demo spec lists received, extracted, classified, redacted, review, approval, and use states | FACT |
| Raw content is not the downstream boundary | Demo invariant requires `approval_state == approved_for_ai` before AI use | FACT |
| The system records review evidence | Audit summary includes event, actor, state, reason, and evidence reference fields | FACT |
| Production compliance is proven | Not demonstrated by this demo | GAP |

## What was tested

- synthetic document intake
- text extraction stage
- sensitivity classification stage
- PII/confidential category detection
- redacted working copy boundary
- approval gate
- blocked raw-content path
- audit summary shape

## What was blocked

- raw unapproved content moving into AI use
- missing approval state
- export or summary before review
- unsupported compliance claims

## Human review points

- reviewer checks the redacted working copy
- reviewer approves, requests changes, or blocks
- reviewer decision and reason are recorded

## Known limitations

- This proof uses synthetic sample content, not real client material.
- It does not prove production security.
- It does not prove legal compliance.
- It does not prove perfect detection accuracy.
- It does not include real external integrations.

## Next decision

Build a clickable single-page prototype using the same states and evidence trail before adding real integrations or client documents.
