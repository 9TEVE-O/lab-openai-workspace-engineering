# Safe Intake Clickable Prototype Logic QA Result

## Review status

```text
Status: LOGIC-LEVEL QA COMPLETE / LIVE BROWSER QA STILL REQUIRED
```

This record checks the prototype source against the QA runbook and test-case expectations.

It does not claim that a real browser session was run.

## Reviewer

```text
Reviewer: ChatGPT assisted logic-level QA
```

## Date

```text
Date: 2026-05-17
```

## Files reviewed

```text
demos/safe-intake-clickable-prototype.html
demos/safe-intake-clickable-prototype-runbook.md
03-safe-intake/safe-intake-demo-test-cases.md
```

## QA method

Source and logic review only.

Checked that the prototype source contains the states, buttons, functions, blocked paths, approval gates, audit event recording, and visible limitations required by the runbook and test cases.

Not checked:

- browser rendering
- real click behaviour in Chromium/Safari/Firefox
- mobile browser behaviour
- keyboard accessibility
- visual layout in an actual viewport
- console errors during live interaction

## Happy-path checks

| Test | Expected behaviour | Logic-level result | Evidence |
|---|---|---|---|
| P1 | Prototype opens at `received` | PASS | `resetDemo()` sets state to `received` and loads synthetic fixture |
| P2 | Extract text moves to `extracted` | PASS | `extractText()` transitions to `extracted` |
| P3 | Classify moves to `classified` | PASS | `classifySensitivity()` transitions to `classified` |
| P4 | Detect categories moves to `classified_with_findings` | PASS | `detectCategories()` transitions and renders findings |
| P5 | Create redacted copy moves to `redacted` | PASS | `createRedactedCopy()` sets `redacted_copy_001` and transitions |
| P6 | Send to review moves to `needs_review` | PASS | `sendToReview()` transitions to `needs_review` |
| P7 | Approve with reason moves to `approved_for_ai` | PASS | `approveForAI()` requires reason then transitions |
| P8 | Safe summary after approval moves to `used_or_exported` | PASS | `safeSummary()` only proceeds from `approved_for_ai` |
| P9 | Audit summary appears | PASS | `renderAudit()` displays recorded events |

## Blocked-path checks

| Test | Expected behaviour | Logic-level result | Evidence |
|---|---|---|---|
| N1 | Raw summary before approval is blocked | PASS | `tryRawSummary()` calls `block()` before approval |
| N2 | Query before approval is blocked | PASS | `queryBeforeApproval()` calls `block()` |
| N3 | Export before approval is blocked | PASS | `exportBeforeApproval()` calls `block()` |
| N4 | Approval without reason is blocked | PASS | `approveForAI()` checks `approvalReason.trim()` |
| N5 | Missing approval state should fail closed | PARTIAL | `safeSummary()` blocks unless state is `approved_for_ai`; no separate missing-state simulation is present |
| N6 | Raw source export before approval is blocked | PARTIAL | export-before-approval path is blocked; dedicated raw-source export button is not separately implemented |

## Approval-gate checks

| Test | Expected behaviour | Logic-level result | Evidence |
|---|---|---|---|
| A1 | Request changes returns to redacted stage | PASS | `requestChanges()` transitions to `redacted` |
| A2 | Block decision prevents AI use | PASS | `blockUse()` transitions to `blocked` |
| A3 | Approval allows safe summary only | PASS | `safeSummary()` requires `approved_for_ai` and uses redacted-copy boundary |

## Audit-summary checks

| Test | Expected behaviour | Logic-level result | Evidence |
|---|---|---|---|
| AU1 | Normal transitions recorded | PASS | `transition()` calls `addAudit()` for state changes |
| AU2 | Blocked actions recorded | PASS | `block()` calls `addAudit()` |
| AU3 | Audit avoids unnecessary raw values | PASS | audit records action/reason/evidence refs, not full raw document values |

## Known limitations check

| Limitation | Logic-level result | Evidence |
|---|---|---|
| Prototype, not production system | PASS | visible limitations list present |
| Does not prove legal compliance | PASS | visible limitations list present |
| Does not test real OCR/access/model behaviour | PASS | visible limitations list present |
| Synthetic fixture only | PASS | header and limitations state synthetic-only use |
| Demonstrates control path, not detection accuracy | PASS | visible limitations list present |

## Overall result

```text
Overall result: LOGIC-LEVEL PASS WITH TWO PARTIAL COVERAGE ITEMS / LIVE BROWSER QA REQUIRED
```

## Follow-up fixes listed

### #14 Add explicit missing-approval-state test control

Reason:

The test cases include a missing/ambiguous approval-state check. The prototype logic fails closed for safe summary unless state is `approved_for_ai`, but there is no explicit UI control that simulates a missing approval state.

Recommended fix:

Add a demo-only button or hidden test control that sets state to an invalid or missing approval state and verifies the block message.

### #15 Add explicit raw-source export blocked control

Reason:

The prototype blocks export before approval and blocks raw source attempts, but it does not expose a dedicated `Export raw source` action matching the test-case wording.

Recommended fix:

Add a visible blocked-path button labelled `Try export raw source` before approval.

### #16 Run live browser QA and update result

Reason:

This record is logic-level QA only. A reviewer still needs to open the HTML in a browser and run the QA runbook manually.

Recommended fix:

Open the prototype locally, click through the runbook, and record observed pass/fail results.

## Final judgement

The prototype is structurally sound enough for live browser QA.

It should not yet be called fully demo-ready because two test-case coverage gaps were found and a real browser session has not been run.
