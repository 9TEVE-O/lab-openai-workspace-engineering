# Agents SDK Pattern

## Core pattern

Agent workflows need evaluation, not just orchestration.

## Build sequence

1. Define the agent job
2. Start with one agent
3. Add tools deliberately
4. Define state and handoffs
5. Add approval gates
6. Add evals for real workflow paths
7. Test regressions from known failures

## Eval cases

- Happy path
- Missing evidence
- Escalation boundary
- Required tool call
- Forbidden tool call
- Approval gate
- State update
- Regression case

## LAB reuse

Use this as the pattern for Safe Intake agent evaluation. A refusal or block may be correct behaviour, not a bug.
