# Repository Protection Settings Review

## Purpose

This file records the required GitHub repository-protection settings for `9TEVE-O/lab-openai-workspace-engineering`.

Some settings cannot be fully enforced from repository files alone. They must be configured in GitHub repository settings.

## Repository

```text
9TEVE-O/lab-openai-workspace-engineering
```

## Required branch protection baseline

| Setting | Recommended value | Status |
|---|---|---|
| Require pull requests before merging | Enabled | Requires GitHub settings review |
| Required approving reviews | 1 minimum | Requires GitHub settings review |
| Dismiss stale approvals | Enabled if collaborating | Requires GitHub settings review |
| Require status checks before merging | Enabled | Requires GitHub settings review |
| Required status checks | Secret scan, Markdown lint, HTML lint, Lightweight security checks | Requires GitHub settings review after workflows run |
| Require conversation resolution | Enabled | Requires GitHub settings review |
| Restrict force pushes | Enabled | Requires GitHub settings review |
| Restrict deletions | Enabled if available | Requires GitHub settings review |
| Require signed commits | Preferred if practical | Requires GitHub settings review |
| Limit admin bypass | Preferred if practical | Requires GitHub settings review |

## Required repository security settings

| Setting | Recommended value | Status |
|---|---|---|
| Secret scanning | Enabled if available | Requires GitHub settings review |
| Push protection | Enabled if available | Requires GitHub settings review |
| Dependabot alerts | Enabled | Requires GitHub settings review |
| Dependabot security updates | Enabled if dependencies are added | Requires GitHub settings review |
| Private vulnerability reporting | Optional for private repo | Requires GitHub settings review |

## File-based protections already added

| Protection | File |
|---|---|
| Security policy | `SECURITY.md` |
| Secret ignore rules | `.gitignore` |
| Secret handling rules | `docs/security/secret-handling.md` |
| Review gate rules | `docs/security/review-gates.md` |
| Dependabot config | `.github/dependabot.yml` |
| Secret scanning workflow | `.github/workflows/secret-scan.yml` |
| Markdown lint workflow | `.github/workflows/markdown-lint.yml` |
| HTML lint workflow | `.github/workflows/html-lint.yml` |
| Lightweight security checks | `.github/workflows/security-checks.yml` |

## Suggested required status checks

Once GitHub Actions has run successfully, configure these as required checks for `main`:

```text
Secret scan / Gitleaks secret scan
Markdown lint / Markdown lint
HTML lint / HTML lint
Lightweight security checks / Repository hygiene checks
```

## Manual settings path

In GitHub:

```text
Settings
→ Branches
→ Branch protection rules
→ Add rule for main
```

Then enable the recommended controls above.

Also review:

```text
Settings
→ Code security and analysis
```

Enable secret scanning, push protection, Dependabot alerts, and Dependabot security updates where available.

## Current decision

The repository file baseline is complete.

The remaining GitHub settings should be treated as pending until verified in the GitHub UI or through an admin API that exposes branch protection/security settings.

## Final status

```text
FILE BASELINE COMPLETE / GITHUB SETTINGS VERIFICATION REQUIRED
```
