# App Submission Skill

## Purpose

Prepare an AI app, ChatGPT App, MCP server, or tool bundle for submission or review by checking declared behaviour against real implementation behaviour.

The skill is used when an app needs submission readiness, client review readiness, or internal governance review.

## Trigger phrases / when to use

Use this skill when the user asks to:

- prepare a ChatGPT App submission
- review an MCP server or app tool bundle
- generate or review submission artefacts
- inspect app metadata, tool descriptions, or tool hints
- check positive and negative test cases
- compare declared tool behaviour with code behaviour
- identify submission blockers

## Inputs required

Ask for or infer:

- repository or folder path
- app name and purpose
- exposed tool list
- tool definitions and schemas
- implementation files or handler functions
- app/widget metadata, if present
- submission form or JSON requirements, if relevant
- expected review audience

If implementation code is unavailable, state that side-effect review is incomplete.

## Workflow

1. Identify the app or tool bundle under review.
2. List all exposed tools.
3. Read tool names, descriptions, input schemas, output schemas, and annotations.
4. Inspect implementation behaviour and helper functions.
5. Classify side effects: read, write, delete, send, publish, external mutation.
6. Check tool hints and permission claims.
7. Check widget, CSP, or app security metadata where present.
8. Generate positive test cases.
9. Generate negative test cases, including nearby out-of-scope requests.
10. Separate blockers, warnings, and optional improvements.

## Required judgement

Do not infer tool behaviour from the tool name alone. Inspect the implementation path and helper functions.

## Output contract

Return:

```text
Submission readiness status:
App/tool summary:
Tool inventory:
Annotation review:
Side-effect map:
Output schema warnings:
Security/CSP notes:
Positive test cases:
Negative test cases:
Blockers:
Recommended fixes:
```

## Safety rules

- Missing or misleading side-effect hints are blockers, not polish items.
- Do not mark a tool read-only unless implementation confirms it cannot mutate state.
- Flag tools that send, publish, delete, revoke, overwrite, or change third-party systems.
- Do not include secrets, credentials, or private data in submission artefacts.
- Keep review findings separate from generated submission JSON when a strict schema is required.

## Failure modes

- Trusting tool names instead of implementation.
- Missing hidden side effects in helper functions.
- Treating missing output schemas as harmless when reliability matters.
- Generating only happy-path tests.
- Forgetting negative tests for out-of-scope or permission-denied requests.
- Making submission claims stronger than the code supports.

## Example request

```text
Review this MCP app for ChatGPT App submission readiness.
```

## Example output

```text
Submission readiness status: not ready
App/tool summary: document-intake MCP server with classify, redact, approve, and export tools
Tool inventory: classify_document, redact_document, approve_for_ai, export_audit_summary
Annotation review: approve_for_ai changes state and must not be marked read-only
Side-effect map: classify=read/compute, redact=write derived copy, approve=state change, export=external output
Output schema warnings: export_audit_summary missing outputSchema
Security/CSP notes: no widget CSP found
Positive test cases: upload sample doc; classify doc; redact PII; approve redacted copy; export audit summary
Negative test cases: ask to summarise raw unapproved doc; approve without reviewer; export blocked item
Blockers: approval tool annotation mismatch
Recommended fixes: correct hints, add outputSchema, add negative tests
```
