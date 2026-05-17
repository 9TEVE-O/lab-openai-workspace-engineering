# Router Skill

## Purpose

Route LAB AI workspace requests to the correct skill, checklist, or project folder so work does not sprawl into another loose chat.

This skill is the first decision layer for the LAB AI skill pack.

## Trigger phrases / when to use

Use this skill when the user asks to:

- decide where a new workflow, prompt, note, or artefact belongs
- continue work inside the LAB OpenAI workspace
- choose between Safe Intake, app submission, workflow audit, tool security review, or proof-pack work
- turn scattered chat material into reusable files
- avoid drifting into broad research or unrelated build ideas

## Inputs required

Ask for or infer:

- the user's immediate task
- the artefact being created or reviewed
- whether the task touches sensitive data, external actions, or client-facing claims
- whether the output should be a skill, checklist, proof pack, spec, or issue
- any repo path or file path already provided

If the missing information would not materially change routing, proceed with the best route and state the assumption.

## Routing table

| Request type | Route to |
|---|---|
| Document intake, redaction, approval, audit log | `safe-intake` |
| ChatGPT App / MCP submission readiness | `app-submission` |
| Process accuracy, completeness, risks, gaps | `workflow-audit` |
| Tool annotations, permissions, side effects, security | `tool-hint-security-review` |
| Client-ready proof, demo script, evidence summary | `client-facing-proof-pack` |
| Credential handling or provider setup | credential gate pattern / checklist |
| OpenAI Developers plugin extraction | `02-openai-developers-extractions/` |

## Workflow

1. Identify the user's requested outcome.
2. Classify the work type: skill, spec, checklist, proof pack, issue, or review.
3. Check whether the request involves sensitive data, approvals, external actions, or client-facing claims.
4. Select the most specific skill or folder.
5. State the routing decision and why.
6. Name the immediate next artefact to create or update.
7. Flag any blocker before work begins.

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
- Do not treat external actions as read-only work.
- Prefer evidence-preserving artefacts over loose summaries.

## Failure modes

- Routing to a broad research task when a narrow artefact is needed.
- Creating a new folder when an existing project folder already fits.
- Sending a security-sensitive task directly to build without review.
- Treating a proof pack as marketing instead of evidence.
- Ignoring the user's explicit file or issue number.

## Example request

```text
#1 Harden LAB AI skill pack files
```

## Example output

```text
Selected route: 01-lab-ai-skill-pack/skills/
Reason: The request refers to the issue for strengthening reusable skill contracts.
Immediate next action: Update each SKILL.md with purpose, triggers, inputs, workflow, output contract, safety rules, failure modes, and examples.
Files or folders involved: six skill files under 01-lab-ai-skill-pack/skills/
Blocker, if any: none
```
