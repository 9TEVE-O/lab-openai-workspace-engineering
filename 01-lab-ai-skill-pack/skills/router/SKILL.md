# Router Skill

## Purpose

Route LAB AI workspace requests to the correct skill, checklist, control record, capability record or project folder so work does not sprawl into another loose chat.

This skill is the first decision layer for the LAB AI skill pack.

## Trigger phrases / when to use

Use this skill when the user asks to:

- decide where a new workflow, prompt, note, artefact, capability or tool belongs
- continue work inside the LAB OpenAI workspace
- find an existing capability, reusable method, operator, tool or MCP-related control before creating something new
- determine whether stored work is active, completed, held, stale, archived or not canon
- choose between Safe Intake, app submission, workflow audit, tool security review, proof-pack work or an existing governed capability
- turn scattered chat material into reusable files
- avoid drifting into broad research or unrelated build ideas

## Inputs required

Ask for or infer:

- the user's immediate task
- the artefact, capability or tool being created, retrieved or reviewed
- whether the task touches sensitive data, external actions, or client-facing claims
- whether the output should be a skill, checklist, proof pack, spec, issue, capability record or control update
- any repo path or file path already provided

If the missing information would not materially change routing, proceed with the best route and state the assumption.

## Routing table

| Request type | Route to |
|---|---|
| Find or classify an existing reusable tool, method or operator | `00-control/intelligence-tool-library-register-v1.0.md`, then apply `00-control/ai-asset-activation-operator-v0.1.md` when activation status matters |
| Determine whether dormant/completed work should be activated | `00-control/ai-asset-activation-operator-v0.1.md` |
| Capability-ingest experiment or runtime-evidence test | `capability-ingest/` |
| Document intake, redaction, approval, audit log | `safe-intake` |
| ChatGPT App / MCP submission readiness | `app-submission` |
| MCP protocol architecture, interoperability, `2026-07-28` migration or extension decision | `research/technology-extractions/mcp-2026-07-28-canonical-integration.md`; apply `05-build-checklists/mcp-tool-security-checklist.md` for security/readiness review |
| Process accuracy, completeness, risks, gaps | `workflow-audit` |
| Tool annotations, permissions, side effects, security | `tool-hint-security-review` |
| Client-ready proof, demo script, evidence summary | `client-facing-proof-pack` |
| Credential handling or provider setup | `credential-gate` |
| ChatGPT app construction | `chatgpt-app-builder` |
| Agent evaluation | `agent-eval` |
| API failure diagnosis | `api-troubleshooting-router` |
| System Zero security or registry consistency | `system-zero-security` / `system-zero/` |
| OpenAI Developers plugin extraction | `02-openai-developers-extractions/` |

## Discovery rule

Before creating a new capability, tool library, Tool Bank, MCP registry or reusable method:

1. inspect `REPO-MAP.md`;
2. inspect `00-control/intelligence-tool-library-register-v1.0.md`;
3. inspect the plugin manifest and relevant skill directories;
4. inspect `capability-ingest/` for applicable experiment records;
5. for MCP architecture/protocol questions, inspect `research/technology-extractions/mcp-2026-07-28-canonical-integration.md` and the current security checklist before inventing a new MCP structure;
6. use AAO-001 when retrieved work may be dormant, completed, archived or not canon;
7. create new structure only if the existing routes cannot represent the item without ambiguity.

The absence of a remembered folder name is not evidence that no governed home exists.

## Workflow

1. Identify the user's requested outcome.
2. Classify the work type: skill, spec, checklist, proof pack, issue, review, capability, tool or control record.
3. Check whether an existing governed item already fits.
4. Check whether the request involves sensitive data, approvals, external actions, or client-facing claims.
5. Select the most specific skill, control record or folder.
6. State the routing decision and why.
7. Name the immediate next artefact to create or update only if a change is actually required.
8. Flag any blocker before work begins.

## Output contract

Return:

```text
Selected route:
Reason:
Immediate next action:
Files or folders involved:
Blocker, if any:
```

If the task is simple and routing is obvious, proceed directly after a short routing note.

## Safety rules

- Route sensitive data, approvals, or client-facing evidence through a review skill before build.
- Do not route raw client data into examples or public proof packs.
- Do not create broad new project branches when the task fits an existing folder.
- Do not create a second Tool Bank or capability registry until the existing control register has been checked.
- Do not infer activation, approval or canon from storage, memory, filenames or repetition.
- Do not infer local MCP implementation, security assurance or protocol conformance merely because the MCP architecture is handbook canon.
- Do not treat external actions as read-only work.
- Prefer evidence-preserving artefacts over loose summaries.

## Failure modes

- Routing to a broad research task when a narrow artefact is needed.
- Creating a new folder when an existing project folder or control register already fits.
- Failing to discover an admitted capability because the router only lists product-oriented skills.
- Treating a proposed folder name as canonical architecture.
- Reactivating completed or archived work because it was retrieved.
- Sending a security-sensitive task directly to build without review.
- Treating protocol canon as proof that a host implementation has passed its local gates.
- Treating a proof pack as marketing instead of evidence.
- Ignoring the user's explicit file or issue number.

## Example request

```text
Find the existing governed method for deciding whether an old AI asset should be reused.
```

## Example output

```text
Selected route: 00-control/ai-asset-activation-operator-v0.1.md
Reason: The request is about activation status for previously created work, which AAO-001 already governs.
Immediate next action: Apply AAO-001 to classify the candidate asset before any implementation change.
Files or folders involved: 00-control/ai-asset-activation-operator-v0.1.md
Blocker, if any: none
```
