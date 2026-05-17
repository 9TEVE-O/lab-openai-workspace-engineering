# Approval Gate Spec

## Purpose

Define the review gate that controls when redacted content may enter downstream AI workflows.

## Approval rule

Only material with this state may be used by retrieval, summarisation, export, or model calls:

```text
approval_state == approved_for_ai
```

## Required approval record

- reviewer identity or role
- reviewed item ID
- redacted copy ID
- decision
- decision reason
- timestamp
- expiry or review window, if relevant

## Block conditions

Block downstream AI use when:

- raw content is requested
- approval state is missing
- reviewer decision is incomplete
- redaction is incomplete
- confidence is too low
- document contains excluded sensitive material
- user lacks permission

## Review question

Would a future reviewer understand why this content was approved or blocked?
