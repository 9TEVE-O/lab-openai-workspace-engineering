# Quickstart

## Purpose

This repository turns scattered AI work into a structured, reusable, reviewable workspace.

It contains:

- LAB AI skill-pack files
- Safe Intake specifications
- Safe Intake clickable demo artefacts
- QA runbooks and result records
- security baseline files
- evidence-led proof-pack material
- OpenAI/plugin extraction notes
- build and review checklists

The operating rule is:

```text
Evidence over intentions.
```

If a workflow matters, it should have a place, a purpose, a repeatable process, a skill file, an evidence trail, and a review gate.

## Current status

Start here:

```text
PHASE-CLOSEOUT.md
```

That file records the current completed phase, known warnings, blocked tasks, and recommended next phase.

Current summary:

```text
PHASE 1 COMPLETE
SAFE INTAKE DEMO READY WITH WARNINGS
SECURITY BASELINE COMPLETE
GITHUB SETTINGS VERIFICATION STILL MANUAL
ROBOT/PROFILE PATCH TASK BLOCKED
```

## First files to read

Read these in order:

```text
README.md
PHASE-CLOSEOUT.md
NEXT-ACTION.md
DEMO-LIMITATIONS.md
SECURITY.md
```

Then, for Safe Intake work:

```text
03-safe-intake/safe-intake-operating-invariant.md
03-safe-intake/demo-scope.md
03-safe-intake/safe-intake-clickable-prototype-plan.md
03-safe-intake/safe-intake-demo-test-cases.md
demos/safe-intake-clickable-prototype-runbook.md
demos/safe-intake-live-browser-qa-result.md
demos/safe-intake-accessibility-visual-qa-result.md
```

Then, for security/hardening work:

```text
docs/security/secret-handling.md
docs/security/review-gates.md
docs/security/repository-protection-settings-review.md
docs/security/static-hosting-headers.md
```

## How to run the Safe Intake demo

From the repository root, run:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/demos/safe-intake-clickable-prototype.html
```

Alternative:

```text
Open demos/safe-intake-clickable-prototype.html directly in a browser.
```

## What the Safe Intake demo shows

The demo shows a controlled document-intake flow:

1. Synthetic document received
2. Text extraction stage
3. Sensitivity classification stage
4. Sensitive-category findings
5. Redacted working copy
6. Human review gate
7. Approval, request-changes, or block decision
8. Safe summary only after approval
9. Raw-content blocked paths
10. Audit event trail

## What the Safe Intake demo does not prove

The demo does not prove:

- legal compliance
- production security
- privacy-law compliance
- real OCR accuracy
- real model safety
- real access-control enforcement
- real-world PII detection accuracy
- suitability for real client documents

Do not describe it as a production compliance product.

## QA workflow

Use the runbook first:

```text
demos/safe-intake-clickable-prototype-runbook.md
```

Use the live-browser QA template when doing a new browser run:

```text
demos/safe-intake-live-browser-qa-result-template.md
```

Record the actual observed result here:

```text
demos/safe-intake-live-browser-qa-result.md
```

Review accessibility and visual warnings here:

```text
demos/safe-intake-accessibility-visual-qa-result.md
```

## Data safety rules

Do not add real data to this repository.

Do not use:

- real personal data
- real client data
- real artist data
- real contracts
- real payment information
- real credentials
- real API keys
- real screenshots containing sensitive material

Use synthetic fixtures only.

Current fixture:

```text
03-safe-intake/fixtures/synthetic-artist-onboarding-form.md
```

## Secret handling

Read:

```text
docs/security/secret-handling.md
```

Never commit:

```text
.env
.env.*
*.secret
*.key
*.pem
```

Never paste raw secrets into:

- Markdown files
- issues
- pull requests
- comments
- fixtures
- screenshots
- logs
- proof packs

Use placeholders only:

```text
OPENAI_API_KEY
GITHUB_TOKEN
PROVIDER_API_KEY
```

If a secret is exposed:

1. Revoke or rotate it.
2. Remove it from the branch.
3. Check history and generated artefacts.
4. Record the incident without copying the raw secret value.

## Security baseline

The repo includes:

```text
SECURITY.md
.gitignore
DEMO-LIMITATIONS.md
docs/security/secret-handling.md
docs/security/review-gates.md
docs/security/repository-protection-settings-review.md
docs/security/static-hosting-headers.md
.github/dependabot.yml
.github/workflows/secret-scan.yml
.github/workflows/markdown-lint.yml
.github/workflows/html-lint.yml
.github/workflows/security-checks.yml
.markdownlint-cli2.yaml
```

Repository settings still require manual verification in GitHub settings:

- pull request requirement
- required status checks
- conversation resolution
- force-push restriction
- signed commits, if practical
- admin bypass limits, if practical
- secret scanning / push protection, if available
- Dependabot alerts/security updates

## How to open follow-up issues

Use one issue per concrete job.

Good issue shape:

```markdown
## Objective

Describe the one job.

## File to create or update

- `path/to/file.md`

## Acceptance criteria

- [ ] specific check
- [ ] specific check
- [ ] specific check

## Review question

Can a future reviewer verify this without reading the original chat?
```

Avoid broad issues such as:

```text
Improve everything
Make it production ready
Add AI governance
```

Prefer concrete issues such as:

```text
Add ARCHITECTURE.md
Add Safe Intake demo proof summary
Verify GitHub branch protection settings
Add ARIA live region for blocked messages
```

## Blocked task

The following task is blocked:

```text
CODE BEHAVIOUR / TEACH THE ROBOT SPECIFIC patches
```

Do not continue this task until the exact source file path and repository are provided.

Do not apply those patches to `.github/workflows/secret-scan.yml`.

Do not create a replacement file unless explicitly instructed.

## Recommended next jobs

From the phase closeout, the next useful jobs are:

```text
#24 Add ARCHITECTURE.md
#25 Add Safe Intake demo proof summary
#26 Verify GitHub repository settings manually
```

Work in that order unless a higher-priority issue appears.
