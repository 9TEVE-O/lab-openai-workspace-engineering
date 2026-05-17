# Agent Eval Skill

## Purpose

Design evaluation cases for agentic workflows so agent behaviour is tested, not merely described.

This skill converts the OpenAI Developers agent pattern into a LAB-owned evaluation workflow.

## Trigger conditions

Use this skill when the user asks to:

- design agent evaluations
- test an agent workflow
- check whether an agent should call or avoid tools
- evaluate Safe Intake agent behaviour
- test approval gates or blocked paths
- turn an agent demo into a repeatable eval set

## Inputs required

Ask for or infer:

- agent job
- available tools
- workflow states
- required tool calls
- forbidden tool calls
- approval gates
- expected outputs
- known failure modes
- regression cases from earlier bugs

If the agent path is not defined, create the workflow contract before writing evals.

## Workflow

1. Define the agent job in one sentence.
2. List tools the agent may use.
3. List tools the agent must not use in specific contexts.
4. Define workflow states and handoffs.
5. Define approval gates.
6. Create happy-path evals.
7. Create missing-evidence evals.
8. Create forbidden-tool evals.
9. Create approval-boundary evals.
10. Create regression evals for known failures.
11. Define pass/fail expectations.

## Output contract

Return:

```text
Agent job:
Tools available:
Workflow states:
Approval gates:
Eval matrix:
Required tool-call cases:
Forbidden tool-call cases:
Missing-evidence cases:
Regression cases:
Pass/fail criteria:
LAB reuse notes:
```

## Safety or review gates

- Do not call an agent reliable because it succeeds once.
- Test blocked behaviour as deliberately as successful behaviour.
- Treat refusal or blocking as correct behaviour when policy or approval gates require it.
- Keep model behaviour evals separate from app-security tests.
- Do not use real sensitive client material in eval fixtures.

## Failure modes

- Only testing happy paths.
- Testing mock paths instead of the real agent path.
- Missing forbidden tool-call cases.
- Treating a policy block as a bug.
- Forgetting regression tests after failures are discovered.

## LAB reuse notes

Use this skill for Safe Intake, app submission review agents, workflow audit assistants, and document-intelligence agents. The key LAB pattern is: every approval gate needs a matching eval.

## Example request

```text
Create eval cases for a Safe Intake agent.
```

## Example output

```text
Agent job: help move a synthetic document through controlled intake
Tools available: classify_doc, redact_doc, request_review, approve_for_ai, export_audit_summary
Workflow states: received, extracted, classified, redacted, needs_review, approved_for_ai, blocked
Approval gates: approve_for_ai requires reviewer decision
Eval matrix: happy path; missing evidence; forbidden raw summary; approval boundary; blocked export; regression case
Required tool-call cases: classify before redact; request_review before approve
Forbidden tool-call cases: export before approval; summarise raw source
Missing-evidence cases: no reviewer decision; missing redacted copy ID
Regression cases: raw content accidentally exported
Pass/fail criteria: correct tool sequence, correct block, evidence recorded
LAB reuse notes: these evals prove control behaviour, not production compliance
```
