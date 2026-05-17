# Tool Hint and Security Review Skill

## Purpose

Review AI tool definitions for accurate annotations, side-effect labels, permission boundaries, and security risks.

## Tool hints to check

- `readOnlyHint`
- `destructiveHint`
- `openWorldHint`
- `idempotentHint`, where supported

## Review workflow

1. List every tool
2. Compare tool name, description, schema, and implementation
3. Identify state-changing behaviour
4. Identify external-world behaviour
5. Identify destructive or irreversible behaviour
6. Check whether the tool can access sensitive data
7. Check whether approval is required before execution
8. Flag missing, false, or misleading annotations

## Security checks

- Secrets are never printed, logged, committed, or exposed
- Sensitive data is not sent to AI without approval
- External actions require clear user intent
- Destructive actions require explicit confirmation or review
- Output schemas are present where reliability matters

## Output contract

Return:

- tool inventory
- hint judgement
- side-effect classification
- sensitive-data exposure
- approval requirements
- blockers
- recommended fixes
