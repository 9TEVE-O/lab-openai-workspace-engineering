# Repo Map

This file is the navigation layer for `lab-openai-workspace-engineering`.

Use it when entering the repo cold, deciding where a piece of AI work belongs, checking whether a workflow has a reusable place, process, skill and evidence trail, or locating an existing governed capability before creating another structure.

## Core transformation

```text
Random chats
→ organised workspace
→ reusable skills
→ governed capabilities and tools
→ evidence trails
→ repeatable AI work
```

## Current discovery paths

```text
00-control/
  REPO-SYNC-2026-08-19.md
  ai-asset-activation-operator-v0.1.md
  intelligence-tool-library-register-v1.0.md

00-workspace-map/
01-lab-ai-skill-pack/
02-openai-developers-extractions/
03-safe-intake/
04-proof-packs/
05-build-checklists/
06-prototypes/
capability-ingest/
system-zero/
docs/
scripts/
```

This is a discovery map, not a claim that every stored item is active or admitted.

## Authoritative discovery rule

When the question is “what capability/tool already exists?” or “where should this reusable pattern live?” use this order:

1. `REPO-MAP.md` — navigation and discovery entry point.
2. `01-lab-ai-skill-pack/skills/router/SKILL.md` — task routing.
3. `00-control/intelligence-tool-library-register-v1.0.md` — governed reusable tool/method/operator status.
4. `00-control/ai-asset-activation-operator-v0.1.md` — determine whether retrieved dormant/completed work may be activated.
5. `01-lab-ai-skill-pack/.codex-plugin/plugin.json` — current packaged skill inventory.
6. `capability-ingest/` — experiment and runtime-evidence records.
7. The relevant host repository for implementation code.

Do not create a second Tool Bank, capability registry or MCP/tool hierarchy merely because a remembered folder name is absent.

## Folder guide

| Folder | Purpose | Start here when... |
|---|---|---|
| `00-control/` | Controlled capability/tool status, activation and repo-sync records | You need to know whether a reusable item is governed, admitted, candidate, held, completed or safe to activate |
| `00-workspace-map/` | Workspace purpose, operating principles and evidence rules | You need the philosophy or decision rules for the repo |
| `01-lab-ai-skill-pack/` | Reusable LAB AI skills and Codex-style plugin manifest | You want an invokable/reusable assistant behaviour or need the packaged skill inventory |
| `02-openai-developers-extractions/` | Extracted implementation and workflow patterns | You are adapting source patterns into LAB workflows without treating the source as authority |
| `03-safe-intake/` | Safe Intake workflow records | You are inspecting the completed/reference Safe Intake capability within its stated status |
| `04-proof-packs/` | Technical-to-client proof artefacts | You need evidence presentation or proof-pack structures |
| `05-build-checklists/` | Build, submission and MCP security checklists | You are reviewing readiness, safety or submission quality |
| `06-prototypes/` | Bounded prototypes | You need prototype implementation evidence rather than authority claims |
| `capability-ingest/` | Capability-ingest experiments and runtime-evidence tests | You need evidence about whether a capability actually works under a defined test |
| `system-zero/` | Registry consistency and system-control assets | You are checking system-level registry/control consistency |

## First-read order

For a new builder or AI agent entering this repo:

1. `README.md`
2. `REPO-MAP.md`
3. `01-lab-ai-skill-pack/skills/router/SKILL.md`
4. `00-control/intelligence-tool-library-register-v1.0.md`
5. `00-control/ai-asset-activation-operator-v0.1.md`
6. `00-workspace-map/operating-principles.md`
7. the specific skill, checklist, experiment record or host repository required by the task

## Routing rule

When adding or integrating material:

- If it defines reusable tool/method/operator status or admission, use `00-control/intelligence-tool-library-register-v1.0.md`.
- If it decides whether dormant/completed material should be activated, use AAO-001 in `00-control/`.
- If it defines how the workspace thinks, use `00-workspace-map/`.
- If it is a reusable assistant behaviour, use `01-lab-ai-skill-pack/skills/` and keep the plugin manifest consistent.
- If it is an extracted source pattern, record it through the existing extraction/control path rather than creating a new doctrine.
- If it is capability-ingest or runtime-evidence work, use `capability-ingest/`.
- If it is host-specific implementation, put code in the host repository rather than this cross-project discovery layer.
- If it defines the Safe Intake workflow, use `03-safe-intake/` without reactivating the historical project by inference.
- If it explains proof to a client, use `04-proof-packs/`.
- If it checks readiness, safety or submission quality, use `05-build-checklists/`.

## Known non-canonical proposed structure

Names resembling `05_CAPABILITIES` and `09_TOOLS_MCP` are not part of the current repository structure and are not established here as canonical paths. Treat them as proposed/not-canon unless a later explicit decision and repository change establishes otherwise.

Their intended concerns are already represented by existing controls:

- capability/tool authority and status → `00-control/intelligence-tool-library-register-v1.0.md`;
- activation of retrieved prior work → `00-control/ai-asset-activation-operator-v0.1.md`;
- reusable assistant behaviours → `01-lab-ai-skill-pack/skills/`;
- MCP/tool security review → `01-lab-ai-skill-pack/skills/tool-hint-security-review/` and `05-build-checklists/mcp-tool-security-checklist.md`;
- capability evidence → `capability-ingest/` and applicable proof/test records.

## Site Studio implementation patterns

The four retained Site Studio patterns are registered as governed candidate reusable implementation patterns in `00-control/intelligence-tool-library-register-v1.0.md`:

- Shared Authoritative State Surface v0.1;
- Durable Human-to-Agent Work Request v0.1;
- Structured Agent Proposal v0.1;
- Lightweight Live State Synchronisation v0.1.

They do not create a separate governance doctrine or Tool Bank. Host-specific implementation belongs in the applicable software repository and remains subject to that repository's gates.

## Review rule

A file belongs in this repo only if it helps convert scattered AI work into a reusable, reviewable, evidence-backed workflow. Presence is storage; status and authority must still be established through the applicable control record.

<!-- merge-doc-maintenance:last-source-pr=48;sha=abcbaa6275df6501b6a16e40b6f8bc474ce73b5d -->
