# MCP/App Submission Review Harness

## Purpose

Use this harness to review an MCP server, ChatGPT App, or app tool bundle before submission, client review, or internal approval.

The harness checks whether declared behaviour, implementation behaviour, and review evidence line up.

## Use this when

- preparing a ChatGPT App submission
- reviewing an MCP server
- checking app tool definitions
- checking tool annotations or hints
- preparing a client-facing app review
- deciding whether an app is ready for demo, pilot, or submission

## Required inputs

| Input | Required? | Notes |
|---|---:|---|
| App or repo name | Yes | Name of the reviewed app/tool bundle |
| App purpose | Yes | Plain-English purpose |
| Tool inventory | Yes | Every exposed tool/action |
| Tool definitions | Yes | Names, descriptions, schemas, annotations |
| Implementation files | Strongly preferred | Required for complete side-effect review |
| App/widget metadata | If present | Include CSP or app metadata where relevant |
| Test cases | Yes | Positive and negative cases |
| Known blockers | Yes | Any missing information, unsafe mismatch, or unresolved review point |

If implementation files are not available, mark the review as incomplete.

## Review summary

```text
App/repo reviewed:
Reviewer:
Date:
Review purpose:
Submission readiness status: ready / not ready / incomplete
Main blocker:
Next action:
```

## 1. Tool inventory

| Tool name | Purpose | Source file | Handler/function | Status |
|---|---|---|---|---|
| | | | | PASS / WARN / BLOCK |

Checklist:

- [ ] Every exposed tool is listed.
- [ ] Every tool has a clear purpose.
- [ ] Every tool points to an implementation location.
- [ ] No hidden or undocumented tool is present.

## 2. Tool descriptions

| Tool name | Declared description | Behaviour observed | Match? | Evidence |
|---|---|---|---|---|
| | | | YES / NO / UNCLEAR | |

Checklist:

- [ ] Tool names do not overstate behaviour.
- [ ] Descriptions match the actual implementation.
- [ ] Descriptions do not hide external actions or state changes.
- [ ] Descriptions are specific enough for review.

## 3. Input schemas

| Tool name | Input schema present? | Required fields clear? | Risk notes | Status |
|---|---|---|---|---|
| | YES / NO | YES / NO / UNCLEAR | | PASS / WARN / BLOCK |

Checklist:

- [ ] Each tool has an input schema.
- [ ] Required fields are clear.
- [ ] Sensitive fields are named carefully.
- [ ] Optional fields do not allow unintended behaviour.

## 4. Output schemas

| Tool name | Output schema present? | Output shape clear? | Warning needed? | Status |
|---|---|---|---|---|
| | YES / NO | YES / NO / UNCLEAR | YES / NO | PASS / WARN / BLOCK |

Checklist:

- [ ] Each important tool has an output schema.
- [ ] Missing output schemas are recorded as warnings.
- [ ] Output shape supports reliable downstream use.
- [ ] Output does not expose unnecessary sensitive material.

## 5. Tool hint review

| Tool name | `readOnlyHint` | `openWorldHint` | `destructiveHint` | Judgement | Status |
|---|---:|---:|---:|---|---|
| | true/false/missing | true/false/missing | true/false/missing | | PASS / WARN / BLOCK |

Checklist:

- [ ] `readOnlyHint` matches implementation behaviour.
- [ ] `openWorldHint` matches external-world behaviour.
- [ ] `destructiveHint` matches destructive or hard-to-reverse behaviour.
- [ ] Missing or unclear hints are recorded.
- [ ] Any misleading hint is treated as a blocker.

## 6. Side-effect map

| Tool name | Reads data | Writes state | Sends/publishes/exports | Deletes/overwrites/revokes | External system touched | Status |
|---|---:|---:|---:|---:|---|---|
| | YES/NO | YES/NO | YES/NO | YES/NO | | PASS / WARN / BLOCK |

Checklist:

- [ ] Read-only behaviour is actually read-only.
- [ ] State changes are explicit.
- [ ] External actions are visible.
- [ ] Destructive actions are labelled.
- [ ] Side effects are reflected in tool descriptions and hints.

## 7. Sensitive-data exposure

| Tool name | Sensitive data possible? | Exposure path | Control present? | Status |
|---|---:|---|---|---|
| | YES / NO / UNCLEAR | | YES / NO / UNCLEAR | PASS / WARN / BLOCK |

Checklist:

- [ ] Secrets are not printed, logged, committed, or returned.
- [ ] Raw sensitive content is not exposed unnecessarily.
- [ ] Sensitive content is not sent to models or third parties without approval.
- [ ] Outputs avoid unnecessary raw values.
- [ ] Review notes do not copy sensitive material.

## 8. Approval gates

| Action | Approval required? | Approval condition | Block condition | Evidence retained |
|---|---:|---|---|---|
| | YES / NO | | | |

Checklist:

- [ ] External actions require clear user intent.
- [ ] Sensitive or irreversible actions require review.
- [ ] Missing approval state fails closed.
- [ ] Blocked actions produce reviewable evidence.
- [ ] Approval records include actor, decision, reason, and timestamp where relevant.

## 9. Positive test cases

Minimum: five positive test cases.

| Test | User request | Expected tool/action | Expected result | Evidence |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

Checklist:

- [ ] Tests cover normal expected use.
- [ ] Tests use exact tool/action names where relevant.
- [ ] Tests check outputs, not just tool triggering.
- [ ] Tests include evidence expected from the workflow.

## 10. Negative test cases

Minimum: three negative test cases.

| Test | User request | Expected non-action/block | Reason | Evidence |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

Checklist:

- [ ] Negative tests include nearby out-of-scope requests.
- [ ] Negative tests include permission or approval failures where relevant.
- [ ] Negative tests include sensitive-data or raw-content edge cases where relevant.
- [ ] Blocked actions are auditable.

## 11. Submission blockers

| Blocker | Severity | Evidence | Required fix | Owner |
|---|---|---|---|---|
| | BLOCK / WARN | | | |

Blocker examples:

- tool description does not match implementation
- misleading `readOnlyHint`, `openWorldHint`, or `destructiveHint`
- missing implementation evidence
- missing required schema
- hidden external action
- missing approval gate
- insufficient negative tests
- sensitive data exposure without control

## Final readiness judgement

Choose one:

| Status | Meaning |
|---|---|
| `ready` | No blockers remain; warnings are documented |
| `not_ready` | One or more blockers must be fixed |
| `incomplete` | Required evidence is missing, so review cannot be finished |

Final review question:

```text
Does the harness prove that declared behaviour, implementation behaviour, and review evidence line up?
```

## Final output format

```text
Submission readiness status:
Reviewed app/repo:
Tools reviewed:
Blockers:
Warnings:
Positive tests count:
Negative tests count:
Approval gates checked:
Sensitive-data review status:
Required fixes:
Next action:
```
