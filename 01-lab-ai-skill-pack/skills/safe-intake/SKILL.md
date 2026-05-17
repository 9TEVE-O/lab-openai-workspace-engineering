# Safe Intake Skill

## Purpose

Design, review, or explain Safe Intake workflows where documents are classified, redacted, reviewed, approved, and only then made available to AI systems.

## Core invariant

No raw, unreviewed, or unapproved document content may be embedded, indexed, summarised, queried, exported, or passed to a hosted model.

Downstream AI access requires:

```text
approval_state == approved_for_ai
```

## Workflow

1. Receive file or text input
2. Extract text and metadata
3. Classify sensitivity
4. Detect PII and confidential content
5. Create redacted working copy
6. Require human review
7. Approve or block AI use
8. Allow only approved redacted content into retrieval, summarisation, or export
9. Record audit evidence

## Required gates

- Raw content gate
- PII/confidentiality gate
- Human review gate
- Approval-state gate
- Export/reporting gate

## Output contract

Return:

- intake stage
- detected risks
- required review action
- approved content boundary
- audit evidence required
- blocked actions, if any
