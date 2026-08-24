# Quickstart

## Purpose

This repository turns scattered AI work into a structured, reusable, reviewable and evidence-bound engineering workspace.

The operating rule is:

```text
Evidence over intentions.
```

Repository presence is not approval. A prompt is not a system. An implementation is not proof of correctness. Status and authority must come from the applicable control and evidence records.

## Current entry path

For current work, start here:

```text
README.md
REPO-MAP.md
NEXT-ACTION.md
01-lab-ai-skill-pack/skills/router/SKILL.md
00-control/intelligence-tool-library-register-v1.0.md
```

Use `00-control/ai-asset-activation-operator-v0.1.md` when retrieved work may be dormant, completed, archived, held or otherwise unsafe to reactivate by inference.

`PHASE-CLOSEOUT.md` is a historical record of the completed 17 May 2026 foundation phase. Its former Phase 2 recommendations are preserved as historical context only and are not the current execution queue.

## Current repository shape

The workspace includes:

- governed capability/tool and activation records in `00-control/`;
- reusable skills and routing in `01-lab-ai-skill-pack/`;
- source-pattern extractions in `02-openai-developers-extractions/`;
- Safe Intake reference material in `03-safe-intake/` and `demos/`;
- proof artefacts in `04-proof-packs/`;
- build, submission and security checks in `05-build-checklists/`;
- bounded prototypes in `06-prototypes/`;
- capability and runtime-evidence experiments in `capability-ingest/`;
- evidence-bound research, technology extractions and research experiments in `research/`;
- System Zero controls in `system-zero/`;
- security and operating documentation in `docs/`.

Use `REPO-MAP.md` for the authoritative discovery route rather than creating a new folder or registry from memory.

## MCP work

For MCP protocol architecture, interoperability, migration or extension decisions, start with:

```text
research/technology-extractions/mcp-2026-07-28-canonical-integration.md
```

For MCP security/readiness review, use:

```text
05-build-checklists/mcp-tool-security-checklist.md
```

The canonical MCP research record does not establish that a host system has implemented MCP, passed conformance, achieved production readiness or should migrate.

## Experiments and evidence

Use `capability-ingest/` and applicable `research/experiments/` records when the question is whether a proposed capability actually passed a defined test.

Preserve the recorded result exactly. Do not promote `ACTIVE`, `REVISE`, `held`, candidate or otherwise incomplete work because an implementation exists or a repository check passed.

Host-specific implementation belongs in the applicable host repository unless this repository explicitly owns the bounded experiment or prototype under test.

## Safe Intake reference workflow

Safe Intake remains a completed/reference capability within its recorded limitations. It is not the repository-wide execution queue.

Start with:

```text
03-safe-intake/safe-intake-operating-invariant.md
03-safe-intake/demo-scope.md
03-safe-intake/safe-intake-demo-test-cases.md
demos/safe-intake-clickable-prototype-runbook.md
demos/safe-intake-live-browser-qa-result.md
demos/safe-intake-accessibility-visual-qa-result.md
```

To run the bounded demo from the repository root:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/demos/safe-intake-clickable-prototype.html
```

The demo does not prove legal compliance, production security, privacy-law compliance, real OCR accuracy, real model safety, real access-control enforcement, real-world PII detection accuracy or suitability for real client documents.

## Data safety rules

Do not add real personal, client, artist, contract, payment or credential data to repository fixtures or demonstrations unless a separately authorised and controlled process explicitly permits it.

Use synthetic fixtures for current demo/test work.

Never commit raw secrets such as:

```text
.env
.env.*
*.secret
*.key
*.pem
```

Never paste raw secrets into Markdown files, issues, pull requests, comments, fixtures, screenshots, logs or proof packs.

Read:

```text
docs/security/secret-handling.md
docs/security/review-gates.md
```

If a secret is exposed:

1. revoke or rotate it;
2. remove it from the branch;
3. check history and generated artefacts;
4. record the incident without reproducing the raw secret value.

## Documentation maintenance

`capability-ingest/merge-doc-maintenance.js` is bounded staleness signalling, not semantic documentation repair.

It can refresh a maintenance marker in designated navigation files after relevant merges. A marker change does not establish that documentation is correct or current. Semantic corrections require an explicit reviewed patch.

## Opening follow-up issues

Use one issue per concrete job with a defined file or scope, acceptance criteria and review question.

Avoid broad tasks such as “improve everything”, “make it production ready” or “add AI governance”.

An open issue or pull request is not automatically the repository's current next action. Check `NEXT-ACTION.md` and the item's own lifecycle/status before activating it.
