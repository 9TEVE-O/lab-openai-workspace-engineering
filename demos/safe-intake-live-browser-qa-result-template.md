# Safe Intake Live Browser QA Result Template

## Purpose

Use this template to record an actual live browser QA run of the Safe Intake clickable prototype.

This is for observed browser behaviour only. Do not use this template for source-only or logic-only review.

## Prototype under test

```text
Prototype file: demos/safe-intake-clickable-prototype.html
Prototype commit reviewed:
Prototype file SHA, if available:
QA run date:
Reviewer:
```

## Browser / device environment

| Field | Value |
|---|---|
| Browser |  |
| Browser version |  |
| Operating system |  |
| Device |  |
| Viewport size |  |
| Local open method | direct file / local server |
| URL or file path opened |  |
| Console checked? | YES / NO |
| Console errors observed? | YES / NO / N/A |

## QA scope

This live browser QA checks:

- visible page load
- clickable button behaviour
- state transitions
- blocked-path behaviour
- approval-gate behaviour
- audit-summary updates
- known limitations visibility
- basic usability and layout issues

This live browser QA does not prove:

- legal compliance
- production security
- real OCR performance
- real model behaviour
- real access control
- detection accuracy on real documents

## Happy-path result table

| Step | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---:|---|---|---|---|---|
| 1 | Open prototype | State is `received`; synthetic fixture visible |  |  |  |
| 2 | Click `Extract text` | State becomes `extracted`; metadata visible |  |  |  |
| 3 | Click `Classify sensitivity` | State becomes `classified`; classification visible |  |  |  |
| 4 | Click `Detect sensitive categories` | State becomes `classified_with_findings`; labels visible |  |  |  |
| 5 | Click `Create redacted copy` | State becomes `redacted`; redacted copy visible |  |  |  |
| 6 | Click `Send to review` | State becomes `needs_review`; reviewer panel visible |  |  |  |
| 7 | Keep or enter decision reason | Reason is present before approval |  |  |  |
| 8 | Click `Approve for AI` | State becomes `approved_for_ai`; approved boundary visible |  |  |  |
| 9 | Click `Generate safe summary` | State becomes `used_or_exported`; safe summary visible |  |  |  |
| 10 | Review audit summary | Audit events show material transitions |  |  |  |

## Blocked-path result table

| Check | Starting state | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|---|---|
| Raw summary blocked | before `approved_for_ai` | Click `Try summarise raw document` | Block message and audit event |  |  |  |
| Query before approval blocked | `needs_review` | Click `Query before approval` | Block message and audit event |  |  |  |
| Export before approval blocked | `needs_review` | Click `Export before approval` | Block message and audit event |  |  |  |
| Missing approval-state blocked | any pre-approved state | Click `Simulate missing approval state`, then attempt summary | Fail-closed message and audit event |  |  |  |
| Raw source export blocked | any state | Click `Try export raw source` | Block message and audit event |  |  |  |
| Raw source still not approved boundary | `approved_for_ai` | Click raw-source negative control | Block message and audit event |  |  |  |

## Approval-gate result table

| Check | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|---|
| Approve with reason | Enter reason and approve | State becomes `approved_for_ai` |  |  |  |
| Missing reason | Clear reason and approve | Approval blocked or warning shown |  |  |  |
| Request changes | Click `Request changes` | State returns to `redacted` |  |  |  |
| Block decision | Click `Block` | State becomes `blocked`; downstream use unavailable |  |  |  |

## Audit-summary result table

| Check | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|
| Normal transitions recorded | Audit shows received, extracted, classified, detection, redaction, review, approval, summary/export events |  |  |  |
| Blocked actions recorded | Blocked attempts appear in audit list |  |  |  |
| Evidence references visible | Events include reason and evidence reference |  |  |  |
| Raw values minimised | Audit does not repeat unnecessary raw fixture values |  |  |  |
| Event order understandable | Most recent or chronological order is clear enough for review |  |  |  |

## Accessibility / usability notes

| Area | Observed result | PASS / WARN / FAIL | Notes / follow-up |
|---|---|---|---|
| Page loads without obvious layout break |  |  |  |
| Buttons are readable and clickable |  |  |  |
| Mobile/narrow layout usable |  |  |  |
| State badge is readable |  |  |  |
| Audit panel is readable |  |  |  |
| Keyboard navigation basic check |  |  |  |
| Colour contrast obvious enough for review |  |  |  |
| Error/block messages noticeable |  |  |  |

## Known limitations visibility

| Limitation | Visible in prototype? | Notes |
|---|---|---|
| Prototype, not production system | YES / NO |  |
| Does not prove legal compliance | YES / NO |  |
| Does not test real OCR/access/model behaviour | YES / NO |  |
| Uses synthetic fixture only | YES / NO |  |
| Demonstrates control path, not detection accuracy | YES / NO |  |

## Follow-up issue table

| Issue needed? | Title | Reason | Severity | Suggested owner |
|---|---|---|---|---|
| YES / NO |  |  | BLOCK / WARN / NICE-TO-HAVE |  |
| YES / NO |  |  | BLOCK / WARN / NICE-TO-HAVE |  |
| YES / NO |  |  | BLOCK / WARN / NICE-TO-HAVE |  |

## Final demo-readiness judgement

Choose one:

```text
DEMO READY
NOT DEMO READY
DEMO READY WITH WARNINGS
INCONCLUSIVE — REQUIRES RE-RUN
```

## Final reviewer note

```text
Reviewer:
Date:
Overall result:
Main evidence:
Main failure or warning:
Follow-up issues created:
Next action:
```
