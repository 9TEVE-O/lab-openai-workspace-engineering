# Credential Gate Skill

## Purpose

Control how API keys, tokens, environment variables, and provider credentials are handled before any API-backed build, test, run, or debug work begins.

This skill converts the OpenAI Developers API-key pattern into a LAB-owned credential safety workflow.

## Trigger conditions

Use this skill when a task involves:

- API keys or provider credentials
- `.env` files
- hosted model calls
- MCP servers that need provider access
- client demos using external APIs
- debugging authentication failures
- deciding whether a key already exists or a new one is needed

## Inputs required

Ask for or infer:

- provider name
- project or repo name
- expected environment variable name
- whether credentials already exist
- where credentials should live
- whether the task is local, hosted, demo, or production-facing
- whether the user authorised credential creation or reuse

Do not ask the user to paste secrets into chat.

## Workflow

1. Identify the provider and credential type.
2. Check whether the task truly requires credentials.
3. Confirm expected environment variable names.
4. Confirm where secrets should live.
5. Check whether existing credentials are available without exposing them.
6. If credentials are missing, describe the safe creation path.
7. Confirm secrets are excluded from commits, logs, screenshots, prompts, and generated artefacts.
8. Record the credential expectation without recording the credential value.

## Output contract

Return:

```text
Credential gate status:
Provider:
Credential type:
Expected environment variables:
Storage location:
Missing items:
Blocked actions:
Safe next action:
LAB reuse notes:
```

## Safety or review gates

- Never print, log, commit, summarise, or expose raw secrets.
- Never place secrets in Markdown examples.
- Never treat credentials as normal project text.
- Use placeholders such as `OPENAI_API_KEY` instead of values.
- Block build/run/debug steps if required credentials are missing.
- Prefer least privilege where provider controls allow it.

## Failure modes

- Asking the user to paste a key into chat.
- Committing `.env` files.
- Writing secrets into examples or proof packs.
- Debugging authentication without confirming environment variables.
- Creating a new key when an authorised existing key should be reused.

## LAB reuse notes

Use this skill before Safe Intake demos, MCP app builds, provider-backed test harnesses, and client-facing prototypes that rely on hosted APIs.

## Example request

```text
Set up the OpenAI key for this Safe Intake demo.
```

## Example output

```text
Credential gate status: blocked until credential location is confirmed
Provider: OpenAI
Credential type: API key
Expected environment variables: OPENAI_API_KEY
Storage location: local `.env` or hosting provider secret store
Missing items: key presence not confirmed
Blocked actions: running provider-backed demo calls
Safe next action: add the key to the approved secret store, never to Markdown or source code
LAB reuse notes: document the expected variable name, not the secret value
```
