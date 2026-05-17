# NEXT ACTION

This file is the execution dashboard for `lab-openai-workspace-engineering`.

Use it when entering the repo cold and deciding what to do next.

## Current objective

Turn the LAB OpenAI workspace scaffold into a usable execution system for reusable AI work, Safe Intake proof, skill-pack development, app/MCP review, and client-facing evidence.

## Completed work

The first scaffold pass is complete:

- [x] README operating thesis added
- [x] `REPO-MAP.md` added
- [x] workspace map created
- [x] LAB AI skill pack created
- [x] LAB AI skill pack hardened
- [x] Safe Intake demo specification created
- [x] OpenAI Developers extraction notes converted into reusable LAB skills
- [x] evidence-led proof pack examples added
- [x] MCP/App submission review harness added

Completed issues:

- [x] #1 Harden LAB AI skill pack files
- [x] #2 Add Safe Intake demo specification
- [x] #3 Convert OpenAI Developers extraction notes into reusable skills
- [x] #4 Add evidence-led proof pack examples
- [x] #5 Add MCP/App submission review harness

## Active next move

Create the next execution layer:

```text
Safe Intake demo spec
→ clickable prototype plan
→ build checklist
→ test cases
→ proof artefact
```

Recommended next issue:

```text
#7 Add Safe Intake clickable prototype plan
```

## Do not do yet

- Do not add real client documents.
- Do not add secrets, API keys, `.env` values, or credentials.
- Do not connect live external systems yet.
- Do not claim production compliance.
- Do not build a broad agent platform before proving the Safe Intake demo path.
- Do not expand into unrelated AI tool research until the demo plan exists.

## Open questions

- What format should the first prototype use: single-page HTML, React app, or ChatGPT App/MCP demo?
- What synthetic sample document should be the default fixture?
- Should the demo prioritise visual proof, tool-state proof, or app-submission readiness?
- Who is the first intended reviewer: internal LAB, a music/creative client, or a technical evaluator?
- What counts as the first successful demo: screenshot, walkthrough, working local app, or hosted preview?

## Next 3 issues to create

### #7 Add Safe Intake clickable prototype plan

Define the simplest prototype that demonstrates the Safe Intake control flow without real client data or live integrations.

Acceptance criteria:

- prototype format chosen
- screen/state list defined
- sample fixture defined
- state transitions defined
- blocked actions defined
- audit summary output defined
- demo success criterion defined

### #8 Add synthetic Safe Intake sample document fixture

Create a safe synthetic sample document for the demo.

Acceptance criteria:

- no real personal or client data
- includes placeholder PII/confidential categories
- suitable for artist onboarding or music contract demo
- includes expected detection labels
- includes expected redacted output

### #9 Add Safe Intake demo test cases

Create positive and negative test cases for the demo.

Acceptance criteria:

- at least five positive test cases
- at least five negative/blocking test cases
- approval-gate tests included
- audit-summary tests included
- raw-content blocked-path tests included

## Review rule

Before starting a new task, ask:

```text
Does this move the repo closer to a demonstrable, evidence-backed Safe Intake workflow?
```

If not, park it.
