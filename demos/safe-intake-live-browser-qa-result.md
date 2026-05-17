# Safe Intake Live Browser QA Result

## Status

```text
LIVE BROWSER QA COMPLETE — PASS
```

This result records an observed browser automation run of the Safe Intake clickable prototype.

## Prototype under test

```text
Prototype file: demos/safe-intake-clickable-prototype.html
Prototype commit reviewed: current main prototype source fetched before run
Prototype file SHA observed before run: f216d53049b412a5283c1edc1c50c6a384f8847d
QA run date: 2026-05-18
Reviewer: ChatGPT assisted browser automation QA
```

## Browser / device environment

| Field | Value |
|---|---|
| Browser | Chromium |
| Browser version | 144.0.7559.96 |
| Operating system | Linux container |
| Device | Headless browser automation |
| Viewport size | 1366x900 primary; 390x844 mobile smoke check |
| Local open method | Current prototype HTML source rendered in Chromium using Playwright `page.set_content` |
| URL or file path opened | `/tmp/safe-intake-clickable-prototype.html` rendered in Chromium |
| Console checked? | YES |
| Console errors observed? | NO |

## QA scope note

The environment blocked direct `file://` and local HTTP navigation, so the current fetched prototype source was rendered directly into Chromium using Playwright. Button clicks, state transitions, DOM updates, audit-panel rendering, and viewport checks were executed in Chromium.

## Happy-path result table

| Step | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---:|---|---|---|---|---|
| 1 | Open prototype | State is `received`; synthetic fixture visible | State `received`; fixture text visible | PASS | `River Echo Demo Project` visible |
| 2 | Click `Extract text` | State becomes `extracted`; metadata visible | State became `extracted` | PASS | Button click changed active state |
| 3 | Click `Classify sensitivity` | State becomes `classified`; classification visible | State became `classified` | PASS | Classification panel rendered |
| 4 | Click `Detect sensitive categories` | State becomes `classified_with_findings`; labels visible | State became `classified_with_findings`; labels visible | PASS | All expected labels present |
| 5 | Click `Create redacted copy` | State becomes `redacted`; redacted copy visible | State became `redacted`; redacted copy visible | PASS | `redacted_copy_001` visible |
| 6 | Click `Send to review` | State becomes `needs_review`; reviewer panel visible | State became `needs_review`; reviewer panel visible | PASS | Decision reason textarea visible |
| 7 | Keep or enter decision reason | Reason is present before approval | Default reason present | PASS | Non-empty reason confirmed |
| 8 | Click `Approve for AI` | State becomes `approved_for_ai`; approved boundary visible | State became `approved_for_ai` | PASS | Approved boundary visible |
| 9 | Click `Generate safe summary` | State becomes `used_or_exported`; safe summary visible | State became `used_or_exported`; safe summary visible | PASS | Safe summary rendered |
| 10 | Review audit summary | Audit events show material transitions | Audit included `safe_summary_generated` | PASS | Audit panel updated |

## Blocked-path result table

| Check | Starting state | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|---|---|
| Raw summary blocked | before `approved_for_ai` | Click `Try summarise raw document` | Block message and audit event | Blocked message shown; `raw_summary_attempt_before_approval` recorded | PASS | Pass |
| Query before approval blocked | `needs_review` | Click `Query before approval` | Block message and audit event | Blocked message shown; `query_before_approval_attempt` recorded | PASS | Pass |
| Export before approval blocked | `needs_review` | Click `Export before approval` | Block message and audit event | Blocked message shown; `export_before_approval_attempt` recorded | PASS | Pass |
| Missing approval-state blocked | pre-approved state | Click `Simulate missing approval state`, then attempt summary | Fail-closed message and audit event | State became `approval_state_missing`; `missing_approval_state_test` and `safe_summary_attempt` recorded | PASS | Pass |
| Raw source export blocked | any state | Click `Try export raw source` | Block message and audit event | Blocked message shown; `raw_source_export_attempt` recorded | PASS | Pass |
| Raw source still not approved boundary | `approved_for_ai` | Click raw-source negative control | Block message and audit event | Blocked message shown; `raw_summary_attempt_after_approval` recorded | PASS | Pass |

## Approval-gate result table

| Check | Action | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|---|
| Approve with reason | Enter reason and approve | State becomes `approved_for_ai` | State became `approved_for_ai` | PASS | Pass |
| Missing reason | Clear reason and approve | Approval blocked or warning shown | State remained `needs_review`; `approval_attempt_without_reason` recorded | PASS | Pass |
| Request changes | Click `Request changes` | State returns to `redacted` | State returned to `redacted` | PASS | Pass |
| Block decision | Click `Block` | State becomes `blocked`; downstream use unavailable | State became `blocked` | PASS | Pass |

## Audit-summary result table

| Check | Expected result | Observed result | PASS / FAIL | Notes / evidence |
|---|---|---|---|---|
| Normal transitions recorded | Audit shows received, extracted, classified, detection, redaction, review, approval, summary/export events | All major happy-path events present | PASS | Pass |
| Blocked actions recorded | Blocked attempts appear in audit list | `raw_source_export_attempt` recorded | PASS | Pass |
| Evidence references visible | Events include reason and evidence reference | `reason:` and `evidence:` visible in audit panel | PASS | Pass |
| Raw values minimised | Audit does not repeat unnecessary raw fixture values | Email and address raw values were not present in audit panel | PASS | Pass |
| Event order understandable | Most recent or chronological order is clear enough for review | Event list rendered visibly after each action | PASS | Pass |

## Accessibility / usability notes

| Area | Observed result | PASS / WARN / FAIL | Notes / follow-up |
|---|---|---|---|
| Page loads without obvious layout break | Body rendered in Chromium | PASS | Headless render loaded |
| Buttons are readable and clickable | Buttons existed and click handlers worked | PASS | 4+ visible buttons observed during flows |
| Mobile/narrow layout usable | Body visible at 390x844 viewport | PASS | Smoke check only, not full visual QA |
| State badge is readable | `.status` visible | PASS | Active state updated |
| Audit panel is readable | `#auditList` visible | PASS | Audit events rendered |
| Keyboard navigation basic check | Not fully tested | WARN | Requires manual accessibility pass |
| Colour contrast obvious enough for review | Not fully measured | WARN | Visual contrast was not measured with tooling |
| Error/block messages noticeable | Block notices appeared in page text | PASS | Blocked paths displayed `Blocked:` |

## Known limitations visibility

| Limitation | Visible in prototype? | Notes |
|---|---|---|
| Prototype, not production system | YES | Visible |
| Does not prove legal compliance | YES | Visible |
| Does not test real OCR/access/model behaviour | YES | Visible |
| Uses synthetic fixture only | YES | Visible |
| Demonstrates control path, not detection accuracy | YES | Visible |

## Follow-up issue table

| Issue needed? | Title | Reason | Severity | Suggested owner |
|---|---|---|---|---|
| YES | Add manual accessibility and visual QA pass | Keyboard navigation and colour contrast were not fully tested | WARN | LAB reviewer |
| NO |  |  |  |  |
| NO |  |  |  |  |

## Final demo-readiness judgement

```text
DEMO READY WITH WARNINGS
```

## Final reviewer note

```text
Reviewer: ChatGPT assisted browser automation QA
Date: 2026-05-18
Overall result: PASS for functional browser automation; DEMO READY WITH WARNINGS
Main evidence: all happy-path, blocked-path, approval-gate, audit-summary, and known-limitation checks passed in Chromium automation.
Main warning: keyboard accessibility and measured colour contrast were not fully tested.
Follow-up issues created: none automatically from this run.
Next action: decide whether to add a manual accessibility/visual QA issue before using this as client-facing proof.
```
