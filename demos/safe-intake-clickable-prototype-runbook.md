# Safe Intake Clickable Prototype QA Runbook

## Purpose

This runbook explains how to manually review the Safe Intake clickable prototype against the demo test cases.

This is manual QA, not automated testing.

## Prototype under review

```text
demos/safe-intake-clickable-prototype.html
```

## Related files

```text
03-safe-intake/safe-intake-clickable-prototype-plan.md
03-safe-intake/fixtures/synthetic-artist-onboarding-form.md
03-safe-intake/safe-intake-demo-test-cases.md
```

## How to open the prototype locally

Option 1: open directly from the file system.

```text
Open demos/safe-intake-clickable-prototype.html in a browser.
```

Option 2: serve the repo locally from the repository root.

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/demos/safe-intake-clickable-prototype.html
```

Do not add real documents, credentials, API keys, external storage, or hosted model calls while reviewing this prototype.

## Review scope

The review checks whether the prototype visibly demonstrates:

- synthetic fixture intake
- state transitions
- sensitive-category detection labels
- redacted working copy
- human approval gate
- blocked raw-content actions
- safe summary after approval
- audit summary
- known limitations

The review does not check:

- production security
- legal compliance
- real OCR
- real model behaviour
- real access control
- detection accuracy on real documents

## Happy-path click sequence

Run this path first.

| Step | Action | Expected result | Pass / Fail | Notes |
|---:|---|---|---|---|
| 1 | Open the prototype | State is `received`; synthetic fixture appears |  |  |
| 2 | Click `Extract text` | State becomes `extracted`; metadata appears |  |  |
| 3 | Click `Classify sensitivity` | State becomes `classified`; classification appears |  |  |
| 4 | Click `Detect sensitive categories` | State becomes `classified_with_findings`; labels appear |  |  |
| 5 | Click `Create redacted copy` | State becomes `redacted`; redacted copy appears |  |  |
| 6 | Click `Send to review` | State becomes `needs_review`; reviewer panel appears |  |  |
| 7 | Enter or keep decision reason | Reason is present before approval |  |  |
| 8 | Click `Approve for AI` | State becomes `approved_for_ai`; approved boundary appears |  |  |
| 9 | Click `Generate safe summary` | State becomes `used_or_exported`; safe summary appears |  |  |
| 10 | Review audit summary | Audit events show material transitions |  |  |

## Blocked-path checks

Run these after reset or at the correct state.

| Check | Starting state | Action | Expected result | Pass / Fail | Notes |
|---|---|---|---|---|---|
| Raw summary blocked | `received`, `extracted`, `classified`, or `classified_with_findings` | Click `Try summarise raw document` | Block message appears; audit event recorded |  |  |
| Query before approval blocked | `needs_review` | Click `Query before approval` | Block message appears; audit event recorded |  |  |
| Export before approval blocked | `needs_review` | Click `Export before approval` | Block message appears; audit event recorded |  |  |
| Raw source still not boundary | `approved_for_ai` | Click `Try raw source anyway` | Block message appears; audit event recorded |  |  |

Expected block message:

```text
Blocked: only approved redacted content can enter the AI workflow.
```

## Approval-gate checks

| Check | Action | Expected result | Pass / Fail | Notes |
|---|---|---|---|---|
| Approve with reason | Enter reason and click `Approve for AI` | State becomes `approved_for_ai` |  |  |
| Request changes | Click `Request changes` from review state | State returns to `redacted` |  |  |
| Block decision | Click `Block` from review state | State becomes `blocked`; downstream use blocked |  |  |
| Missing reason | Clear reason and click `Approve for AI` | Approval blocked or warning shown |  |  |

## Audit-summary checks

| Check | Expected result | Pass / Fail | Notes |
|---|---|---|---|
| Normal events recorded | received, extracted, classified, detection, redaction, review, approval, summary/export events are visible |  |  |
| Blocked events recorded | blocked action events appear after blocked attempts |  |  |
| Evidence references visible | each event includes reason and evidence reference |  |  |
| Raw values minimised | audit avoids unnecessary raw values and uses labels/references where possible |  |  |
| Limitations visible | prototype shows known limitations |  |  |

## Pass/fail recording template

Use this table for the review result.

| Area | Result | Evidence / notes | Follow-up issue needed? |
|---|---|---|---|
| Happy path | PASS / FAIL |  | YES / NO |
| Blocked paths | PASS / FAIL |  | YES / NO |
| Approval gate | PASS / FAIL |  | YES / NO |
| Audit summary | PASS / FAIL |  | YES / NO |
| Limitations visible | PASS / FAIL |  | YES / NO |
| Overall demo readiness | PASS / FAIL |  | YES / NO |

## Failure handling

If a check fails:

1. Record the exact step.
2. Record expected behaviour.
3. Record observed behaviour.
4. Create a follow-up issue.
5. Do not call the prototype demo-ready until the failure is fixed or explicitly accepted as a known limitation.

## Demo-ready threshold

The prototype is demo-ready when:

```text
Happy path passes.
Blocked paths pass.
Approval gate checks pass.
Audit summary checks pass.
Known limitations remain visible.
No real data or external calls are introduced.
```

## Final reviewer judgement

```text
Reviewer:
Date:
Prototype version / commit:
Overall result: PASS / FAIL
Main evidence:
Main issue found:
Next action:
```
