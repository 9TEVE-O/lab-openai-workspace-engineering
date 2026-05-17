# Secret Handling Rules

## Core rule

Never commit, paste, log, screenshot, summarise, or preserve raw secrets in this repository.

Secrets include:

- API keys
- access tokens
- refresh tokens
- private keys
- `.env` values
- webhook secrets
- OAuth client secrets
- cloud credentials
- database credentials
- provider credentials

## Approved handling pattern

Use placeholders in documentation:

```text
OPENAI_API_KEY
GITHUB_TOKEN
PROVIDER_API_KEY
```

Store real values only in approved secret stores such as:

- local untracked `.env` files
- GitHub Actions secrets
- hosting-provider secret stores
- password managers
- cloud secret managers

## Do not do this

Do not:

- paste real secrets into Markdown
- place real secrets in examples
- commit `.env` files
- include secrets in screenshots
- include secrets in issue comments
- include secrets in test fixtures
- print secrets in logs
- preserve leaked secret values in incident notes

## If a secret is exposed

1. Stop using the secret.
2. Revoke or rotate it immediately.
3. Remove it from the active branch.
4. Check commit history for exposure.
5. Record the incident without copying the raw secret value.
6. Confirm whether logs, screenshots, or generated artefacts also captured it.
7. Add or update ignore/scanning rules if needed.

## Safe issue wording

Use:

```text
A provider API key was exposed in a committed file and has been rotated.
```

Do not use:

```text
The exposed key was sk-...
```

## Repo-specific note

The current Safe Intake prototype must remain synthetic-only. Do not add real client documents, real artist data, real contact details, or real payment data to fixtures, demos, screenshots, reports, or proof packs.
