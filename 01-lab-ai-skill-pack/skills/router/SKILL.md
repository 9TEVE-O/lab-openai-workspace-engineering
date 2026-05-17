# Router Skill

## Purpose

Route LAB AI workspace requests to the correct skill or checklist.

## Use this skill when

- A request involves Safe Intake, app submission, workflow audit, tool security review, or client proof material
- A task could drift into a broad research rabbit hole
- The user needs the next useful artefact, not another loose chat answer

## Routing table

| Request type | Route to |
|---|---|
| Document intake, redaction, approval, audit log | `safe-intake` |
| ChatGPT App / MCP submission readiness | `app-submission` |
| Process accuracy, completeness, risks, gaps | `workflow-audit` |
| Tool annotations, permissions, side effects, security | `tool-hint-security-review` |
| Client-ready proof, demo script, evidence summary | `client-facing-proof-pack` |

## Default decision rule

If the request touches sensitive data, approvals, external actions, or client-facing claims, route to review before build.

## Output contract

Return:

1. selected skill
2. reason for routing
3. immediate next action
4. blocker, if any
