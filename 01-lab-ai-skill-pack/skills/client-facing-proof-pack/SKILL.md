# Client-Facing Proof Pack Skill

## Purpose

Turn technical workflow notes into a clear client-facing proof artefact with evidence, limits, and next actions.

## Trigger phrases / when to use

Use this skill when the user asks for:

- a proof pack
- a demo summary
- a client-ready explanation
- an evidence table
- a workflow proof map
- a non-technical project summary

## Inputs required

Ask for or infer:

- workflow being shown
- intended audience
- what was tested
- what evidence exists
- what was blocked or held for review
- known limitations
- next decision

If evidence is missing, mark it as a gap.

## Workflow

1. Identify the client problem.
2. Summarise the workflow in plain English.
3. Map the workflow steps.
4. List evidence for each claim.
5. List what was tested.
6. List what was blocked or held for review.
7. State known limitations.
8. Name the next decision.

## Output contract

Return:

- client-ready summary
- workflow map
- evidence table
- what was tested
- what was blocked
- human review points
- known limitations
- next decision

## Safety rules

- Do not overstate what the proof shows.
- Do not hide limitations.
- Do not include private raw material in client-facing examples.
- Separate evidence from assumptions.
- Keep the language clear and practical.

## Failure modes

- Turning proof into hype.
- Making claims without evidence.
- Omitting limitations.
- Forgetting blocked actions.
- Writing only for technical readers.

## Example request

Create a client-facing proof pack for the Safe Intake demo.

## Example output

Client-ready summary: This demo shows a controlled document workflow before AI use.
Workflow map: document received -> checked -> redacted copy prepared -> review -> approved content used -> evidence summary generated
Evidence table: approval state recorded; blocked path documented; summary generated
What was tested: intake, review gate, approval boundary, evidence summary
What was blocked: unapproved content moving forward
Human review points: reviewer approval required
Known limitations: demo does not prove production readiness
Next decision: decide whether to build a clickable prototype
