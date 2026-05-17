# Safe Intake Demo Test Cases

## Purpose

Define manual test cases for the Safe Intake clickable prototype.

These tests verify that the prototype demonstrates the control path:

```text
received
→ extracted
→ classified
→ classified_with_findings
→ redacted
→ needs_review
→ approved_for_ai or blocked
→ used_or_exported
```

The tests are for the first single-page HTML demo. They do not prove production security, legal compliance, model accuracy, or real-world detection performance.

## Test fixture

Use:

```text
03-safe-intake/fixtures/synthetic-artist-onboarding-form.md
```

The fixture is synthetic-only and must not be replaced with real client, artist, or personal data.

## Pass / fail rules

A test passes when:

- the expected state is reached
- the expected visible evidence appears
- blocked actions are visibly blocked
- audit events are recorded for material actions
- raw unapproved content does not move into AI use

A test fails when:

- a state is skipped without evidence
- raw content is used before approval
- a blocked action succeeds
- an audit event is missing
- approval can happen without a review decision

---

# Positive test cases

## P1 — Load synthetic fixture

| Field | Value |
|---|---|
| Starting state | none |
| Action | Open the prototype |
| Expected state | `received` |
| Expected result | Synthetic artist onboarding form is visible |
| Evidence required | document ID placeholder, source type, timestamp placeholder |
| Pass / fail | PASS / FAIL |

## P2 — Extract text

| Field | Value |
|---|---|
| Starting state | `received` |
| Action | Click `Extract text` |
| Expected state | `extracted` |
| Expected result | Extracted text preview and simple metadata appear |
| Evidence required | extraction event, text length placeholder, metadata summary |
| Pass / fail | PASS / FAIL |

## P3 — Classify sensitivity

| Field | Value |
|---|---|
| Starting state | `extracted` |
| Action | Click `Classify sensitivity` |
| Expected state | `classified` |
| Expected result | Sensitivity classification appears |
| Evidence required | classification result, confidence label, reason summary |
| Pass / fail | PASS / FAIL |

## P4 — Detect sensitive categories

| Field | Value |
|---|---|
| Starting state | `classified` |
| Action | Click `Detect sensitive categories` |
| Expected state | `classified_with_findings` |
| Expected result | Expected detection labels appear |
| Evidence required | `[PROJECT_NAME]`, `[PERSON_NAME]`, `[EMAIL]`, `[PHONE]`, `[ADDRESS]`, `[BUSINESS_REFERENCE]`, `[PAYMENT_TERM]`, `[PAYMENT_NOTE]`, `[PRIVATE_NOTE]`, `[SIGNATURE]`, `[DATE]` |
| Pass / fail | PASS / FAIL |

## P5 — Create redacted copy

| Field | Value |
|---|---|
| Starting state | `classified_with_findings` |
| Action | Click `Create redacted copy` |
| Expected state | `redacted` |
| Expected result | Redacted working copy appears |
| Evidence required | redacted copy ID, redaction method, category-labelled redacted text |
| Pass / fail | PASS / FAIL |

## P6 — Send redacted copy to review

| Field | Value |
|---|---|
| Starting state | `redacted` |
| Action | Click `Send to review` |
| Expected state | `needs_review` |
| Expected result | Reviewer decision panel appears |
| Evidence required | reviewer role placeholder, pending decision, redacted copy ID |
| Pass / fail | PASS / FAIL |

## P7 — Approve redacted copy

| Field | Value |
|---|---|
| Starting state | `needs_review` |
| Action | Choose `Approve for AI` with a decision reason |
| Expected state | `approved_for_ai` |
| Expected result | Approved status appears |
| Evidence required | reviewer decision, reason, timestamp placeholder, approved redacted copy ID |
| Pass / fail | PASS / FAIL |

## P8 — Generate safe summary after approval

| Field | Value |
|---|---|
| Starting state | `approved_for_ai` |
| Action | Click `Generate safe summary` |
| Expected state | `used_or_exported` |
| Expected result | Safe summary appears using approved redacted content only |
| Evidence required | summary event, approved redacted copy ID, no unnecessary raw values |
| Pass / fail | PASS / FAIL |

## P9 — Export or view audit summary

| Field | Value |
|---|---|
| Starting state | `approved_for_ai` or `used_or_exported` |
| Action | Click `Export audit summary` or `View audit summary` |
| Expected state | `used_or_exported` |
| Expected result | Audit summary appears |
| Evidence required | event list, state transitions, blocked action log if any, final decision |
| Pass / fail | PASS / FAIL |

---

# Negative / blocking test cases

## N1 — Block raw summary before approval

| Field | Value |
|---|---|
| Starting state | `classified_with_findings` or earlier |
| Attempted action | Click `Try summarise raw document` |
| Expected result | Action is blocked |
| Expected message | `Blocked: only approved redacted content can enter the AI workflow.` |
| Evidence required | blocked action audit event |
| Pass / fail | PASS / FAIL |

## N2 — Block query before approval

| Field | Value |
|---|---|
| Starting state | `needs_review` |
| Attempted action | Click `Query before approval` |
| Expected result | Action is blocked |
| Expected message | `Blocked: only approved redacted content can enter the AI workflow.` |
| Evidence required | blocked action audit event with previous state `needs_review` |
| Pass / fail | PASS / FAIL |

## N3 — Block export before approval

| Field | Value |
|---|---|
| Starting state | `needs_review` |
| Attempted action | Click `Export before approval` |
| Expected result | Action is blocked |
| Expected message | `Blocked: only approved redacted content can enter the AI workflow.` |
| Evidence required | blocked action audit event |
| Pass / fail | PASS / FAIL |

## N4 — Block approval without decision reason

| Field | Value |
|---|---|
| Starting state | `needs_review` |
| Attempted action | Choose `Approve for AI` without a reason |
| Expected result | Approval is blocked or warning shown |
| Expected message | Reviewer decision reason required |
| Evidence required | no transition to `approved_for_ai` until reason is supplied |
| Pass / fail | PASS / FAIL |

## N5 — Block use when approval state is missing

| Field | Value |
|---|---|
| Starting state | ambiguous / reset / state missing |
| Attempted action | Generate safe summary |
| Expected result | Action is blocked |
| Expected message | Missing approval state. Workflow fails closed. |
| Evidence required | blocked action event |
| Pass / fail | PASS / FAIL |

## N6 — Block raw source export

| Field | Value |
|---|---|
| Starting state | any state before `approved_for_ai` |
| Attempted action | Export source document |
| Expected result | Action is blocked |
| Expected message | Raw source document cannot be exported from this demo path before approval |
| Evidence required | blocked action event, source document not exported |
| Pass / fail | PASS / FAIL |

---

# Approval-gate tests

## A1 — Request changes returns to redaction stage

| Field | Value |
|---|---|
| Starting state | `needs_review` |
| Action | Choose `Request changes` |
| Expected state | `redacted` |
| Expected result | Reviewer sends item back for redaction change |
| Evidence required | reviewer decision, reason, transition from `needs_review` to `redacted` |
| Pass / fail | PASS / FAIL |

## A2 — Block decision prevents AI use

| Field | Value |
|---|---|
| Starting state | `needs_review` |
| Action | Choose `Block` |
| Expected state | `blocked` |
| Expected result | Downstream AI actions are unavailable or blocked |
| Evidence required | reviewer decision, block reason, timestamp placeholder |
| Pass / fail | PASS / FAIL |

## A3 — Approval allows safe summary only

| Field | Value |
|---|---|
| Starting state | `approved_for_ai` |
| Action | Generate safe summary |
| Expected result | Summary uses approved redacted content only |
| Evidence required | approved redacted copy ID; no raw fixture values in safe summary |
| Pass / fail | PASS / FAIL |

---

# Audit-summary tests

## AU1 — Audit records normal state transitions

| Field | Value |
|---|---|
| Action | Complete happy path from `received` to `used_or_exported` |
| Expected result | Audit summary shows each major transition |
| Required events | received, extracted, classified, categories detected, redacted copy created, review requested, approval granted, safe summary generated |
| Pass / fail | PASS / FAIL |

## AU2 — Audit records blocked actions

| Field | Value |
|---|---|
| Action | Attempt raw summary before approval |
| Expected result | Audit summary includes blocked action event |
| Required fields | event_id, timestamp, actor, item_id, action, previous_state, new_state, reason, evidence_ref |
| Pass / fail | PASS / FAIL |

## AU3 — Audit does not expose unnecessary raw values

| Field | Value |
|---|---|
| Action | View audit summary after detection and redaction |
| Expected result | Audit uses labels and evidence references, not unnecessary raw fixture values |
| Required evidence | category labels visible; raw values not repeated unless part of document preview |
| Pass / fail | PASS / FAIL |

---

# Raw-content blocked-path tests

## R1 — Raw content cannot enter safe summary path

| Field | Value |
|---|---|
| Starting state | before `approved_for_ai` |
| Attempted action | Generate summary from raw source |
| Expected result | Blocked |
| Evidence required | blocked action event; no summary generated |
| Pass / fail | PASS / FAIL |

## R2 — Raw content cannot enter export path

| Field | Value |
|---|---|
| Starting state | before `approved_for_ai` |
| Attempted action | Export raw content |
| Expected result | Blocked |
| Evidence required | blocked action event; raw export unavailable |
| Pass / fail | PASS / FAIL |

## R3 — Redacted content boundary is visible after approval

| Field | Value |
|---|---|
| Starting state | `approved_for_ai` |
| Action | View approved content boundary |
| Expected result | Prototype shows approved redacted copy ID and category-labelled text |
| Evidence required | raw source and approved redacted copy are visibly separate |
| Pass / fail | PASS / FAIL |

---

# Manual run checklist

Before considering the prototype demo-ready:

- [ ] Run all positive tests.
- [ ] Run all negative/blocking tests.
- [ ] Run all approval-gate tests.
- [ ] Run all audit-summary tests.
- [ ] Run all raw-content blocked-path tests.
- [ ] Record failed tests as issues.
- [ ] Do not use real documents while testing.
- [ ] Do not claim production readiness from these tests.

## Demo-ready threshold

The first prototype is demo-ready when:

```text
All positive tests pass.
All negative/blocking tests pass.
Approval gate tests pass.
Audit summary tests pass.
Raw-content blocked-path tests pass.
Known limitations remain visible in the demo.
```

## Next file

After these tests are added, build:

```text
demos/safe-intake-clickable-prototype.html
```
