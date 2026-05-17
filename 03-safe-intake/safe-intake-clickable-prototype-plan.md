# Safe Intake Clickable Prototype Plan

## Purpose

Define the simplest clickable prototype that demonstrates the Safe Intake control flow without real client data, live integrations, external storage, or hosted model calls.

The prototype should show the workflow shape clearly enough that a reviewer can see what entered, what was detected, what was redacted, what was blocked, what was approved, and what evidence remains.

## Prototype format chosen

Build the first prototype as a single-page HTML demo.

Recommended format:

```text
single-file HTML
inline CSS
inline JavaScript
synthetic fixture only
no external APIs
no external assets
no real client data
```

Why this format:

- fastest to build
- easy to open locally
- easy to share as a proof artefact
- no deployment or account setup required
- no credential handling required
- visible enough for a client or internal reviewer

## Prototype objective

Demonstrate the Safe Intake state path:

```text
received
→ extracted
→ classified
→ redacted
→ needs_review
→ approved_for_ai or blocked
→ used_or_exported
```

The prototype is successful when a viewer can click through the workflow and see:

- the source document entering the system
- detected categories
- redacted working copy
- review gate
- approved or blocked state
- blocked action explanation
- audit summary

## Target reviewer

First reviewer:

```text
internal LAB reviewer
```

Secondary reviewer:

```text
music / creative industry operator who handles contracts, onboarding forms, grants, or client documents
```

## Sample fixture defined

Use a synthetic sample artist onboarding form.

Fixture file to create later:

```text
03-safe-intake/fixtures/synthetic-artist-onboarding-form.md
```

The fixture should include fake placeholder-style data only:

- artist name
- representative name
- email
- phone
- address
- payment term
- private note
- signature placeholder

No real personal, client, artist, or business data should be used.

## Screen / state list

### Screen 1: Start / Document received

State:

```text
received
```

Shows:

- demo title
- plain-English explanation
- synthetic document preview
- current state badge
- button: `Extract text`

Evidence shown:

- source type: synthetic fixture
- timestamp placeholder
- document ID placeholder

### Screen 2: Text extracted

State:

```text
extracted
```

Shows:

- extracted text preview
- simple metadata
- text length placeholder
- button: `Classify sensitivity`

Evidence shown:

- extraction method: fixture text parse
- metadata captured

### Screen 3: Sensitivity classified

State:

```text
classified
```

Shows:

- sensitivity result: `contains personal / contract-like information`
- confidence placeholder
- reason summary
- button: `Detect sensitive categories`

Evidence shown:

- classification result
- reason
- confidence label

### Screen 4: Sensitive categories detected

State:

```text
classified_with_findings
```

Shows detected categories:

- `[PERSON_NAME]`
- `[EMAIL]`
- `[PHONE]`
- `[ADDRESS]`
- `[PAYMENT_TERM]`
- `[PRIVATE_NOTE]`
- `[SIGNATURE]`

Buttons:

- `Create redacted copy`
- `Try summarise raw document` blocked-path button

Evidence shown:

- detection categories only
- no unnecessary raw values in audit view

### Screen 5: Redacted working copy

State:

```text
redacted
```

Shows:

- redacted document preview
- redacted copy ID placeholder
- redaction method summary
- button: `Send to review`

Evidence shown:

- before/after boundary stated
- redaction method
- redacted copy ID

### Screen 6: Review required

State:

```text
needs_review
```

Shows:

- reviewer decision panel
- redacted copy preview
- decision options:
  - `Approve for AI`
  - `Request changes`
  - `Block`

Blocked-path buttons:

- `Export before approval`
- `Query before approval`

Evidence shown:

- reviewer role placeholder
- pending decision

### Screen 7A: Approved for AI

State:

```text
approved_for_ai
```

Shows:

- approval status
- reviewer decision
- decision reason
- approved redacted content boundary
- button: `Generate safe summary`
- button: `Export audit summary`

Evidence shown:

- reviewer
- decision
- timestamp placeholder
- approved redacted copy ID

### Screen 7B: Blocked

State:

```text
blocked
```

Shows:

- blocked status
- block reason
- next action: revise redaction or do not use AI
- button: `View audit summary`

Evidence shown:

- block decision
- reviewer reason
- timestamp placeholder

### Screen 8: Audit summary

State:

```text
used_or_exported
```

Shows:

- audit event list
- state transition list
- blocked action log
- final decision
- proof limitation note

Evidence shown:

- event ID
- timestamp placeholder
- actor
- item ID
- action
- previous state
- new state
- reason
- evidence reference

## State transitions defined

| From | Action | To | Notes |
|---|---|---|---|
| `received` | Extract text | `extracted` | creates extraction event |
| `extracted` | Classify sensitivity | `classified` | creates classification event |
| `classified` | Detect categories | `classified_with_findings` | creates detection event |
| `classified_with_findings` | Create redacted copy | `redacted` | creates redacted copy ID |
| `redacted` | Send to review | `needs_review` | review required before AI use |
| `needs_review` | Approve for AI | `approved_for_ai` | reviewer decision required |
| `needs_review` | Request changes | `redacted` | returns to redaction stage |
| `needs_review` | Block | `blocked` | downstream AI use blocked |
| `approved_for_ai` | Generate safe summary | `used_or_exported` | approved redacted content only |
| `approved_for_ai` | Export audit summary | `used_or_exported` | audit export event created |
| any unapproved state | Try AI use | no transition | blocked action event created |

## Blocked actions defined

The prototype must visibly block:

| Attempted action | State | Expected result |
|---|---|---|
| Summarise raw document | before `approved_for_ai` | blocked |
| Query unapproved content | before `approved_for_ai` | blocked |
| Export content | before `approved_for_ai` | blocked |
| Approve without decision reason | `needs_review` | blocked or warning |
| Use missing approval state | any ambiguous state | blocked |

Blocked action message:

```text
Blocked: only approved redacted content can enter the AI workflow.
```

Each blocked action should create an audit event.

## Audit summary output defined

The audit summary should be visible inside the prototype.

Minimum event format:

```text
event_id:
timestamp:
actor:
item_id:
action:
previous_state:
new_state:
reason:
evidence_ref:
```

Required events:

- document received
- text extracted
- sensitivity classified
- categories detected
- redacted copy created
- review requested
- approval granted / changes requested / blocked
- safe summary generated, if approved
- audit summary exported
- blocked action attempted

## Safe summary output

The safe summary must only use the approved redacted copy.

Example safe summary:

```text
This synthetic artist onboarding form contains contact, address, payment, and private-note fields. Sensitive values were replaced with category labels before approval.
```

The summary must not use or reveal raw placeholder values unnecessarily.

## Demo success criterion defined

The prototype succeeds if a reviewer can complete this path:

```text
Open single HTML file
→ view synthetic document
→ extract text
→ classify sensitivity
→ detect categories
→ create redacted copy
→ attempt blocked raw summary
→ send redacted copy to review
→ approve for AI
→ generate safe summary
→ view audit summary
```

And can clearly see:

- what entered
- what was detected
- what was redacted
- what was blocked
- what was approved
- what evidence remains

## Out of scope for first prototype

Do not include:

- real document uploads
- OCR
- live model calls
- external storage
- authentication
- user accounts
- real client data
- legal compliance claims
- production security claims

## Next files to create

1. `03-safe-intake/fixtures/synthetic-artist-onboarding-form.md`
2. `03-safe-intake/safe-intake-demo-test-cases.md`
3. `demos/safe-intake-clickable-prototype.html`

## Build order

1. Create the synthetic fixture.
2. Create test cases.
3. Build the single-page HTML prototype.
4. Run the prototype against the test cases manually.
5. Update the Safe Intake proof pack with screenshots or observed evidence.
