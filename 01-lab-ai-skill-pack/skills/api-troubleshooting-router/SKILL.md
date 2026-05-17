# API Troubleshooting Router Skill

## Purpose

Classify API, model, app, or tool failures before trying to fix them.

This skill converts the OpenAI Developers troubleshooting pattern into a LAB-owned triage workflow.

## Trigger conditions

Use this skill when the user reports:

- API calls failing
- authentication errors
- quota or billing errors
- rate limits
- model, project, or organisation access problems
- tool schema errors
- MCP or app tool failures
- policy or approval gate blocks
- uncertainty about whether a block is a bug

## Inputs required

Ask for or infer:

- provider or system involved
- exact error message, if available
- endpoint, model, tool, or action involved
- whether credentials are configured
- whether quota or billing is available
- whether the workflow touches an approval gate
- whether the failure happened locally, in hosting, or in a sandbox
- what the user expected to happen

Do not ask for raw secrets, API keys, or tokens.

## Workflow

1. Capture the visible symptom.
2. Classify the failure before proposing fixes.
3. Check whether the request reached the provider or tool.
4. Check authentication and credential configuration without exposing secrets.
5. Check quota, billing, rate limits, model access, project access, and organisation access.
6. Check tool schema and input/output mismatches.
7. Check whether a policy, review, or approval gate correctly blocked the action.
8. Separate confirmed facts from likely causes.
9. Recommend the smallest safe next diagnostic step.
10. Record whether the failure was a bug, missing setup, limit, access issue, or correct block.

## Output contract

Return:

```text
Failure class:
System/provider:
Observed symptom:
Confirmed facts:
Likely cause:
What not to do:
Safe diagnostic step:
Fix path:
Escalation needed:
LAB reuse notes:
```

## Safety or review gates

- Never request or expose raw credentials.
- Do not treat a refusal or approval-gate block as a bug until checked.
- Do not advise bypassing gates, policies, or permission controls.
- Do not guess exact provider state without evidence.
- Keep sensitive logs, tokens, and client material out of issue comments and proof packs.

## Failure classes

| Failure class | Meaning |
|---|---|
| network_or_sandbox | Request cannot reach provider/tool |
| authentication | Missing, invalid, or misconfigured credentials |
| quota_or_billing | Account or project cannot spend/call |
| rate_limit | Request volume or concurrency exceeded |
| model_or_project_access | Model, project, org, or permission issue |
| schema_mismatch | Tool input/output contract mismatch |
| approval_gate_block | Workflow correctly blocked action pending review |
| correct_refusal | System refused for a valid control reason |
| unknown | Evidence is insufficient |

## Failure modes

- Trying random fixes before classifying the failure.
- Confusing quota errors with rate limits.
- Exposing secrets while debugging.
- Treating a policy block as broken behaviour.
- Ignoring schema mismatch in tool calls.
- Making unsupported claims about provider-side status.

## LAB reuse notes

Use this skill for Safe Intake demos, MCP apps, provider-backed prototypes, app submission testing, and any workflow where a failure might be a correct control gate.

## Example request

```text
The Safe Intake demo will not export the audit summary. Is it broken?
```

## Example output

```text
Failure class: approval_gate_block
System/provider: Safe Intake demo workflow
Observed symptom: export is blocked
Confirmed facts: export requires approved redacted content
Likely cause: approval_state is missing or not approved_for_ai
What not to do: do not bypass the approval gate
Safe diagnostic step: inspect approval record and redacted copy ID
Fix path: approve the redacted copy or keep export blocked
Escalation needed: no, unless approval state is correct and export still fails
LAB reuse notes: a blocked export may prove the control is working
```
