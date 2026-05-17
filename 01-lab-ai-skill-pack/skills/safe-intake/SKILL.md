# Safe Intake Skill

## Purpose

Design, review, or explain Safe Intake workflows where documents are classified, redacted, reviewed, approved, and only then made available to AI systems.

The skill protects the central Safe Intake invariant: raw, unreviewed, or unapproved content must not enter downstream AI use.

## Trigger phrases / when to use

Use this skill when the user asks about:

- Safe Intake
- document upload, document intake, or AI ingestion
- PII/confidential detection
- redaction before AI use
- human approval gates
- audit logs for AI workflows
- document intelligence with compliance or privacy risk
- what should be blocked before model use

## Inputs required

Ask for or infer:

- document type or sample content category
- source channel, if relevant
- intended downstream AI use
- sensitivity concerns
- required reviewer or approval role
- desired output: spec, workflow, audit note, proof map, or demo step
- whether raw content has already been reviewed

If raw sensitive content is provided, do not reproduce it unnecessarily. Work from categories, summaries, or redacted snippets where possible.

## Core invariant

No raw, unreviewed, or unapproved document content may be embedded, indexed, summarised, queried, exported, or passed to a hosted model.

Downstream AI access requires:

```text
approval_state == approved_for_ai
```

## Workflow

1. Receive file or text input.
2. Extract text and metadata.
3. Classify sensitivity.
4. Detect PII and confidential content.
5. Create a redacted working copy.
6. Require human review.
7. Approve or block AI use.
8. Allow only approved redacted content into retrieval, summarisation, querying, or export.
9. Record audit evidence.
10. State what the workflow proves and does not prove.

## Required gates

- Raw content gate
- PII/confidentiality gate
- Human review gate
- Approval-state gate
- Export/reporting gate

## Output contract

Return:

```text
Intake stage:
Detected risks:
Required review action:
Approved content boundary:
Blocked actions:
Audit evidence required:
Known limitations:
Next decision:
```

## Safety rules

- Fail closed when approval state is missing, ambiguous, stale, or contradicted.
- Do not send raw unapproved content to AI, retrieval, embeddings, summaries, or exports.
- Do not claim legal compliance from a workflow sketch or demo.
- Preserve enough evidence for later review without storing unnecessary sensitive content.
- Keep human approval explicit where confidence, permissions, or sensitivity require it.

## Failure modes

- Treating upload as permission for AI ingestion.
- Redacting visually but retaining raw text in downstream indexes.
- Summarising raw content before approval.
- Skipping human review because the model seems confident.
- Producing client-facing claims stronger than the evidence supports.
- Recording audit logs that contain the sensitive content they were meant to control.

## Example request

```text
Design the Safe Intake flow for a music contract before it goes into an AI knowledge base.
```

## Example output

```text
Intake stage: needs_review
Detected risks: names, signatures, payment terms, private contract clauses
Required review action: human reviewer must inspect redacted working copy
Approved content boundary: only the approved redacted copy may enter retrieval
Blocked actions: embedding raw contract, summarising raw text, exporting unreviewed clauses
Audit evidence required: document ID, classification result, redaction record, reviewer decision, approval timestamp
Known limitations: this proves workflow control, not legal compliance
Next decision: approve the redacted copy, request further redaction, or block AI use
```
