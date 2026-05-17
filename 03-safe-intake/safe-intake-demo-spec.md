# Safe Intake Demo Specification

## Demo objective

Show the smallest useful Safe Intake workflow: a document enters the system, is checked, redacted, reviewed, approved or blocked, and leaves behind an evidence trail.

The demo is not trying to prove legal compliance, enterprise security, or production readiness. It proves the control shape.

## User story

As a small organisation or creative business operator, I want to use AI on document content without automatically sending raw, unreviewed, or sensitive material into an AI workflow.

I need to see:

- what entered the workflow
- what was detected
- what was redacted
- what required review
- what was approved
- what was blocked
- what evidence remains

## Input document type

Use a synthetic sample document that resembles a real operational document but contains no real client data.

Recommended first demo input:

```text
Sample artist onboarding form or sample music contract excerpt
```

The sample may include placeholder examples of:

- person name
- email address
- phone number
- address
- payment term
- private note
- signature placeholder

## Core invariant

No raw, unreviewed, or unapproved document content may be embedded, indexed, summarised, queried, exported, or passed to a hosted model.

Downstream AI access requires:

```text
approval_state == approved_for_ai
```

If approval state is missing, unclear, stale, or contradicted by the evidence trail, the workflow fails closed.

## Intake stages

| Stage | State | Demo behaviour | Evidence captured |
|---|---|---|---|
| 1 | `received` | User uploads or pastes the synthetic sample document | file name, timestamp, source channel |
| 2 | `extracted` | System extracts visible text and simple metadata | extraction method, text length, metadata |
| 3 | `classified` | System classifies sensitivity level | classification, confidence, reason |
| 4 | `redacted` | System creates a redacted working copy | detected categories, redaction method |
| 5 | `needs_review` | System requires human review before AI use | reviewer role required, review timestamp pending |
| 6 | `approved_for_ai` or `blocked` | Reviewer approves redacted copy or blocks use | reviewer decision, reason, timestamp |
| 7 | `used_or_exported` | Approved redacted content is summarised or exported | approved content ID, query/export record |

## PII/confidential detection behaviour

The demo should identify categories, not expose unnecessary raw values.

Detection categories:

- name
- email
- phone
- address
- signature placeholder
- payment or contract term
- private note

Expected behaviour:

- detected items are highlighted by category
- raw values are not repeated in the audit summary unless necessary
- low-confidence items are sent to review
- unknown sensitive-looking text is flagged as `needs_review`

## Redacted working copy behaviour

The demo creates a separate working copy.

Required behaviour:

- raw source remains outside downstream AI use
- redacted copy replaces detected values with category labels
- redacted copy gets its own ID
- redaction method is recorded
- reviewer sees the redacted copy before approval

Example redaction style:

```text
[PERSON_NAME]
[EMAIL]
[PHONE]
[ADDRESS]
[PAYMENT_TERM]
[PRIVATE_NOTE]
```

## Human approval gate

The reviewer must choose one of three decisions:

| Decision | Meaning |
|---|---|
| Approve for AI | Redacted copy may enter AI workflow |
| Request changes | Redaction is incomplete or unclear |
| Block | Content must not enter AI workflow |

Required approval record:

- reviewer identity or role
- reviewed item ID
- redacted copy ID
- decision
- decision reason
- timestamp

## Blocked actions

The demo must visibly block:

- summarising raw unapproved content
- embedding raw unapproved content
- querying unapproved content
- exporting unreviewed content
- approving without reviewer decision
- using content with missing approval state

Blocked actions should produce a short explanation and an audit event.

## Audit summary

The demo generates a simple audit summary that records control decisions without storing sensitive raw content.

Minimum audit fields:

| Field | Purpose |
|---|---|
| event_id | unique event identifier |
| timestamp | when the event occurred |
| actor | user, reviewer, or system |
| item_id | document or redacted copy affected |
| action | what happened |
| previous_state | state before event |
| new_state | state after event |
| reason | why the event occurred |
| evidence_ref | pointer to relevant evidence |

Required audit events:

- document received
- text extracted
- sensitivity classified
- PII/confidential content detected
- redacted copy created
- human review requested
- approval granted or denied
- approved content used or exported
- blocked action attempted

## What the demo proves

This demo proves:

- document intake can be staged instead of automatic
- sensitive categories can be detected before AI use
- redacted working copies can create a safer downstream boundary
- human approval can control whether content enters AI use
- blocked actions can be made visible
- audit evidence can show what happened and why

## What the demo does not prove

This demo does not prove:

- legal compliance
- production security
- enterprise access control
- perfect PII detection
- full OCR accuracy
- full document-management readiness
- that every edge case has been tested

## Success criterion

A viewer can see what entered, what was detected, what was redacted, what was blocked, what was approved, and what evidence remains.

## Next build decision

Build the demo as a simple clickable or single-page prototype before adding real integrations.

Do not connect real client documents, external storage, or hosted model calls until the approval gate and audit summary are visible in the demo flow.
