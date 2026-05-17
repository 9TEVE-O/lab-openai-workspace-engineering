# ChatGPT App Builder Skill

## Purpose

Plan and shape a ChatGPT App or MCP-backed app before code is written, with clear tool surfaces, schemas, side-effect boundaries, UI boundaries, and review gates.

This skill converts the OpenAI Developers app-building pattern into a LAB-owned build-planning workflow.

## Trigger conditions

Use this skill when the user asks to:

- build a ChatGPT App
- design an MCP-backed app
- plan app tools before code
- convert Safe Intake into an app demo
- define app architecture, widget boundary, or tool surface
- prepare an app for later submission readiness review

## Inputs required

Ask for or infer:

- app purpose
- target user
- app archetype
- required tools/actions
- data handled by each tool
- side effects for each tool
- UI or widget requirements
- review/approval gates
- test cases
- deployment or demo context

If the app touches sensitive data or external actions, route through review gates before build.

## Workflow

1. Define the app objective.
2. Choose the app archetype: tool-only, widget demo, interactive app, or submission-ready app.
3. Define the tool surface before code.
4. For each tool, define name, purpose, input schema, output schema, and side effects.
5. Separate tool behaviour from presentation UI.
6. Define review and approval gates.
7. Define metadata and security boundaries.
8. Define positive and negative test flows.
9. Produce the build plan or app spec.
10. Route to app-submission review before client review or submission.

## Output contract

Return:

```text
App objective:
App archetype:
Target user:
Tool surface:
UI/widget boundary:
Side-effect map:
Approval gates:
Security notes:
Positive flows:
Negative flows:
Build sequence:
LAB reuse notes:
```

## Safety or review gates

- Plan tools before app code.
- Do not mix raw data handling into UI-only logic.
- Do not mark tools read-only until behaviour is known.
- Add review gates before external, sensitive, or irreversible actions.
- Keep demo claims separate from production claims.
- Do not include real client data in demo fixtures.

## Failure modes

- Writing UI before defining tool boundaries.
- Hiding side effects inside vague tool names.
- Building a broad app before proving one narrow workflow.
- Treating a demo as submission-ready.
- Skipping negative flows.

## LAB reuse notes

For Safe Intake, prefer an interactive decoupled pattern:

```text
upload / classify / redact / review / approve / query / export
```

Each stage should be testable and blockable independently.

## Example request

```text
Plan the Safe Intake ChatGPT App demo before code.
```

## Example output

```text
App objective: show controlled document intake before AI use
App archetype: interactive app demo
Target user: small organisation reviewing sensitive documents
Tool surface: receive_sample_doc, classify_doc, redact_doc, request_review, approve_for_ai, export_audit_summary
UI/widget boundary: UI displays state and evidence; tools perform state transitions
Side-effect map: classify reads; redact creates derived copy; approve changes state; export creates artefact
Approval gates: approve_for_ai requires reviewer decision
Security notes: no real client data; synthetic fixture only
Positive flows: classify, redact, approve, export
Negative flows: summarise raw document; approve without reviewer; export blocked item
Build sequence: prototype state machine first, then UI, then optional provider integration
LAB reuse notes: send through app-submission review before external demo
```
