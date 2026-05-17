# Safe Intake Live Browser QA Result

## Status

```text
LIVE BROWSER QA PENDING
```

This file is reserved for the actual observed browser QA result.

Do not mark this file as passed until the prototype has been opened and clicked through in a real browser.

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
| Browser | PENDING |
| Browser version | PENDING |
| Operating system | PENDING |
| Device | PENDING |
| Viewport size | PENDING |
| Local open method | PENDING |
| URL or file path opened | PENDING |
| Console checked? | PENDING |
| Console errors observed? | PENDING |

## Happy-path result table

| Step | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---:|---|---|---|---|---|
| 1 | Open prototype | State is `received`; synthetic fixture visible | PENDING | PENDING |  |
| 2 | Click `Extract text` | State becomes `extracted`; metadata visible | PENDING | PENDING |  |
| 3 | Click `Classify sensitivity` | State becomes `classified`; classification visible | PENDING | PENDING |  |
| 4 | Click `Detect sensitive categories` | State becomes `classified_with_findings`; labels visible | PENDING | PENDING |  |
| 5 | Click `Create redacted copy` | State becomes `redacted`; redacted copy visible | PENDING | PENDING |  |
| 6 | Click `Send to review` | State becomes `needs_review`; reviewer panel visible | PENDING | PENDING |  |
| 7 | Keep or enter decision reason | Reason is present before approval | PENDING | PENDING |  |
| 8 | Click `Approve for AI` | State becomes `approved_for_ai`; approved boundary visible | PENDING | PENDING |  |
| 9 | Click `Generate safe summary` | State becomes `used_or_exported`; safe summary visible | PENDING | PENDING |  |
| 10 | Review audit summary | Audit events show material transitions | PENDING | PENDING |  |

## Blocked-path result table

| Check | Starting state | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|---|---|
| Raw summary blocked | before `approved_for_ai` | Click `Try summarise raw document` | Block message and audit event | PENDING | PENDING |  |
| Query before approval blocked | `needs_review` | Click `Query before approval` | Block message and audit event | PENDING | PENDING |  |
| Export before approval blocked | `needs_review` | Click `Export before approval` | Block message and audit event | PENDING | PENDING |  |
| Missing approval-state blocked | any pre-approved state | Click `Simulate missing approval state`, then attempt summary | Fail-closed message and audit event | PENDING | PENDING |  |
| Raw source export blocked | any state | Click `Try export raw source` | Block message and audit event | PENDING | PENDING |  |
| Raw source still not approved boundary | `approved_for_ai` | Click raw-source negative control | Block message and audit event | PENDING | PENDING |  |

## Approval-gate result table

| Check | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|---|
| Approve with reason | Enter reason and approve | State becomes `approved_for_ai` | PENDING | PENDING |  |
| Missing reason | Clear reason and approve | Approval blocked or warning shown | PENDING | PENDING |  |
| Request changes | Click `Request changes` | State returns to `redacted` | PENDING | PENDING |  |
| Block decision | Click `Block` | State becomes `blocked`; downstream use unavailable | PENDING | PENDING |  |

## Audit-summary result table

| Check | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|
| Normal transitions recorded | Audit shows received, extracted, classified, detection, redaction, review, approval, summary/export events | PENDING | PENDING |  |
| Blocked actions recorded | Blocked attempts appear in audit list | PENDING | PENDING |  |
| Evidence references visible | Events include reason and evidence reference | PENDING | PENDING |  |
| Raw values minimised | Audit does not repeat unnecessary raw fixture values | PENDING | PENDING |  |
| Event order understandable | Most recent or chronological order is clear enough for review | PENDING | PENDING |  |

## Accessibility / usability notes

| Area | Observed result | PASS / WARN / FAIL | Notes / follow-up |
|---|---|---|---|
| Page loads without obvious layout break | PENDING | PENDING |  |
| Buttons are readable and clickable | PENDING | PENDING |  |
| Mobile/narrow layout usable | PENDING | PENDING |  |
| State badge is readable | PENDING | PENDING |  |
| Audit panel is readable | PENDING | PENDING |  |
| Keyboard navigation basic check | PENDING | PENDING |  |
| Colour contrast obvious enough for review | PENDING | PENDING |  |
| Error/block messages noticeable | PENDING | PENDING |  |

## Known limitations visibility

| Limitation | Visible in prototype? | Notes |
|---|---|---|
| Prototype, not production system | PENDING |  |
| Does not prove legal compliance | PENDING |  |
| Does not test real OCR/access/model behaviour | PENDING |  |
| Uses synthetic fixture only | PENDING |  |
| Demonstrates control path, not detection accuracy | PENDING |  |

## Follow-up issue table

| Issue needed? | Title | Reason | Severity | Suggested owner |
|---|---|---|---|---|
| PENDING |  |  | BLOCK / WARN / NICE-TO-HAVE |  |
| PENDING |  |  | BLOCK / WARN / NICE-TO-HAVE |  |
| PENDING |  |  | BLOCK / WARN / NICE-TO-HAVE |  |

## Final demo-readiness judgement

```text
PENDING — LIVE BROWSER QA NOT YET RUN
```

## Final reviewer note

```text
Reviewer:
Date:
Overall result: PENDING
Main evidence:
Main failure or warning:
Follow-up issues created:
Next action: Open the prototype in a real browser and complete this file.
```
