# API Key Gate Pattern

## Core pattern

Credential handling must happen before API-backed build, test, run, or debug work.

## Rules

- Never print API keys
- Never commit secrets
- Never treat credentials as normal project text
- Confirm where environment variables live
- Confirm whether a key already exists before creating a new one
- Prefer least privilege where provider controls allow it

## LAB reuse

Use this pattern as a credential gate for all provider-backed workflows, including OpenAI, model gateways, MCP servers, hosted apps, and client demos.

## Review question

Can a reviewer understand where credentials are expected to live without seeing the credentials themselves?
