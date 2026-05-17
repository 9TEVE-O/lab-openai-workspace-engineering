# App Submission Skill

## Purpose

Prepare an AI app, ChatGPT App, MCP server, or tool bundle for submission or review by checking declared behaviour against real behaviour.

## Trigger

Use this skill when reviewing:

- ChatGPT App submissions
- MCP servers
- plugin-style tool bundles
- app metadata and tool descriptions
- positive and negative test cases

## Review workflow

1. Identify all exposed tools
2. Read tool names, descriptions, input schemas, output schemas, and annotations
3. Inspect implementation behaviour, not names alone
4. Classify side effects: read, write, delete, send, publish, external mutation
5. Check tool hints and permission claims
6. Check widget or app security metadata where present
7. Generate positive test cases
8. Generate negative test cases
9. List blockers and warnings separately from submission data

## Required judgement

Do not infer tool behaviour from the tool name alone. Inspect the implementation path and helper functions.

## Output contract

Return:

- submission readiness status
- tool inventory
- annotation review
- output schema warnings
- side-effect map
- positive test cases
- negative test cases
- blockers
- recommended fixes
