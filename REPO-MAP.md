# Repo Map

This file is the navigation layer for `lab-openai-workspace-engineering`.

Use it when entering the repo cold, deciding where a piece of AI work belongs, or checking whether a workflow has a reusable place, process, skill, and evidence trail.

## Core transformation

```text
Random chats
→ organised workspace
→ reusable skills
→ project folders
→ evidence trails
→ repeatable AI work
```

## Top-level structure

```text
00-workspace-map/
  workspace-purpose.md
  operating-principles.md
  evidence-trail-rules.md

01-lab-ai-skill-pack/
  .codex-plugin/
    plugin.json
  skills/
    router/
      SKILL.md
    safe-intake/
      SKILL.md
    app-submission/
      SKILL.md
    workflow-audit/
      SKILL.md
    tool-hint-security-review/
      SKILL.md
    client-facing-proof-pack/
      SKILL.md

02-openai-developers-extractions/
  openai-developers-plugin-review.md
  chatgpt-app-submission-pattern.md
  build-chatgpt-app-pattern.md
  agents-sdk-pattern.md
  api-key-gate-pattern.md
  troubleshooting-router-pattern.md

03-safe-intake/
  safe-intake-operating-invariant.md
  safe-intake-proof-map.md
  approval-gate-spec.md
  audit-log-spec.md
  demo-scope.md

04-proof-packs/
  proof-pack-template.md
  client-facing-proof-pack-example.md
  evidence-led-demo-script.md

05-build-checklists/
  codex-plugin-build-checklist.md
  chatgpt-app-submission-checklist.md
  mcp-tool-security-checklist.md
```

## Folder guide

| Folder | Purpose | Start here when... |
|---|---|---|
| `00-workspace-map/` | Defines the workspace purpose, operating principles, and evidence rules | You need the philosophy or decision rules for the repo |
| `01-lab-ai-skill-pack/` | Holds reusable LAB AI skills and the Codex-style plugin manifest | You want to turn repeated AI work into skill files |
| `02-openai-developers-extractions/` | Captures useful patterns from OpenAI Developers plugin examples | You are adapting OpenAI/Codex/App/MCP patterns into LAB workflows |
| `03-safe-intake/` | Defines Safe Intake’s invariant, proof map, approval gate, audit log, and demo boundary | You are building or explaining Safe Intake |
| `04-proof-packs/` | Converts technical work into client-facing proof artefacts | You need a demo summary, evidence table, or client-facing explanation |
| `05-build-checklists/` | Contains build, submission, and MCP security checklists | You are reviewing a plugin, app, tool, or MCP workflow before use |

## First-read order

For a new builder or AI agent entering this repo:

1. `README.md`
2. `REPO-MAP.md`
3. `00-workspace-map/workspace-purpose.md`
4. `00-workspace-map/operating-principles.md`
5. `01-lab-ai-skill-pack/skills/router/SKILL.md`
6. `03-safe-intake/safe-intake-operating-invariant.md`
7. `05-build-checklists/mcp-tool-security-checklist.md`

## Routing rule

When adding new material:

- If it defines how the workspace thinks, put it in `00-workspace-map/`.
- If it is a reusable assistant behaviour, put it in `01-lab-ai-skill-pack/skills/`.
- If it extracts lessons from OpenAI/Codex/plugin examples, put it in `02-openai-developers-extractions/`.
- If it defines the Safe Intake product/workflow, put it in `03-safe-intake/`.
- If it explains proof to a client, put it in `04-proof-packs/`.
- If it checks readiness, safety, or submission quality, put it in `05-build-checklists/`.

## Review rule

A file belongs in this repo only if it helps convert scattered AI work into a reusable, reviewable, evidence-backed workflow.
