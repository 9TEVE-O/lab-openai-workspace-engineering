# Skill: Consolidate Duplicate markdownlint-cli2 Configuration

**Scope**: GitHub Issue #34 only  
**Type**: Repository maintenance task with external enforcement controls  
**Created**: 2026-08-09 (trial skill for bounded task execution)

## Purpose

Enforce evidence-based, minimum-diff repository maintenance for Issue #34: consolidate duplicate markdownlint-cli2 configuration files.

## Required Controls

### Before Edits
- [x] Inspect both `.markdownlint-cli2.yaml` and `.markdownlint-cli2.yml`
- [x] Determine which configuration markdownlint-cli2 actually resolves and why
- [x] Inspect the CI workflow (`.github/workflows/markdown-lint.yml`)
- [x] State the smallest justified change
- [x] Document rule-set differences explicitly
- [x] Verify no `.github/skills/` directory existed (creating this skill as external control)

### During Edits
- [ ] **Issue scope only**: All changes must be traceable to Issue #34 requirements
- [ ] **Evidence before edits**: Pre-edit inspection complete and documented (see section below)
- [ ] **Minimum necessary diff**: Remove only the redundant ignored file; preserve canonical config and all ignore paths
- [ ] **No unrelated changes**: Commit only Issue #34 changes
- [ ] **No security/branch weakening**: Verify no changes to branch protections, merge authority, or security checks

### During Acceptance Testing
- [ ] **Existing tests/CI**: Run `.github/workflows/markdown-lint.yml` and verify PASS
- [ ] **Security verification**: Run `/security-review` and record findings
- [ ] **Inspect final diff**: Confirm deletion only (no rule/ignore changes)

### After Testing
- [ ] **Create PR**: Reference Issue #34 explicitly
- [ ] **No automatic merge**: Human retains merge authority
- [ ] **Record controls**: Distinguish GitHub/Copilot-native controls from external (this skill, CI, issue constraints)

## Pre-Edit Evidence

### Configuration Resolution

**Current Active Configuration**: `.markdownlint-cli2.yaml`

**Why**: markdownlint-cli2 auto-discovers configs in this precedence:
1. `.markdownlint-cli2.yaml` ← **ACTIVE**
2. `.markdownlint-cli2.yml` ← **IGNORED**
3. `.markdownlint-cli2.jsonc`
4. `.markdownlint-cli2.json`
5. (other formats...)

**CI Workflow**: `.github/workflows/markdown-lint.yml` runs `markdownlint-cli2-action@v23` without explicitly specifying a config file, relying on auto-discovery.

### Rule-Set Comparison

| Rule | `.yaml` | `.yml` | Impact |
|------|---------|--------|--------|
| MD013 (line length) | false | — | `.yaml` disables; `.yml` allows |
| MD025 (multiple top-level headings) | false | — | `.yaml` disables; `.yml` allows |
| MD033 (inline HTML) | false | false | Both disable |
| MD034 (bare URLs) | false | — | `.yaml` disables; `.yml` allows |
| MD036 (emphasis as heading) | false | — | `.yaml` disables; `.yml` allows |
| MD041 (first line must be heading) | false | false | Both disable |
| MD060 (table pipe alignment) | false | false | Both disable |

**Conclusion**: `.markdownlint-cli2.yml` is MORE STRICT (enables 3 rules). It is currently ignored by the tool.

### Ignore Paths (Both Files Identical)

Both configurations preserve:
```yaml
ignores:
  - node_modules/**
  - dist/**
  - build/**
  - coverage/**
```

## Smallest Justified Change

**Action**: Delete `.markdownlint-cli2.yml`

**Justification**:
1. `.markdownlint-cli2.yaml` is already active (confirmed by tool precedence and CI success)
2. Removing the ignored file eliminates configuration ambiguity without changing linting behavior
3. All `.md` files are already validated against `.yaml` rules in CI
4. Preserves all ignore paths and canonical rule set
5. Does not weaken any checks
6. Minimum diff (1 file deletion)

## Acceptance Criteria Checklist

- [ ] Issue #34 referenced in commit message and PR
- [ ] Only `.markdownlint-cli2.yml` deleted; `.markdownlint-cli2.yaml` and ignore paths unchanged
- [ ] `.github/workflows/markdown-lint.yml` CI passes
- [ ] `/security-review` run and findings recorded in PR
- [ ] No changes to branch protections, merge authority, or credentials
- [ ] PR created; merge decision retained by human
- [ ] Session logs and skill enforcement recorded

## Control Classification

**GitHub/Copilot-Native Controls**:
- Branch creation and isolation
- Git commit and push operations
- PR creation and linking to Issue #34
- CI workflow execution and status checks
- Security scanning workflows

**External Controls (This Skill / Issue Requirements)**:
- Evidence-based pre-edit inspection requirement
- Minimum-diff enforcement (single file deletion only)
- Rule-set difference documentation
- Explicit security/branch verification
- No automatic merge (human decision required)
- Control classification in PR description

**CI-Enforced Controls**:
- Markdown lint workflow (`.github/workflows/markdown-lint.yml`)
- Secret scanning (`.github/workflows/secret-scan.yml`)
- Security checks (`.github/workflows/security-checks.yml`)
- HTML lint (`.github/workflows/html-lint.yml`)
