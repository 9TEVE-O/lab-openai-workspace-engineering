# Tool Hint and Security Review Skill

## Purpose

Review tool definitions so their names, descriptions, annotations, and actual behaviour line up.

## Trigger phrases / when to use

Use this skill when the user asks to review:

- tool hints
- tool annotations
- MCP tool definitions
- app submission readiness
- side-effect labels
- permission boundaries

## Inputs required

Ask for or infer:

- tool names
- tool descriptions
- input schemas
- output schemas
- annotations or hints
- implementation files or handlers
- systems touched by each tool

If implementation details are missing, mark the review incomplete.

## Workflow

1. List every tool.
2. Compare the tool name with its description.
3. Compare the description with the schema.
4. Compare the schema with the implementation.
5. Classify what the tool does.
6. Check whether annotations match behaviour.
7. Identify blockers and warnings.
8. Recommend exact fixes.

## Output contract

Return:

- tool inventory
- annotation judgement
- behaviour classification
- review requirements
- blockers
- recommended fixes
- final question

## Safety rules

- Do not rely on tool names alone.
- Do not mark a tool as low-risk unless behaviour supports that judgement.
- Flag unclear or missing annotations.
- Keep review findings separate from generated submission files.

## Failure modes

- Trusting the name instead of the implementation.
- Missing behaviour hidden in helper functions.
- Ignoring missing schemas.
- Treating unclear annotations as acceptable.

## Example request

Review these tool definitions for correct annotations.

## Example output

Tool inventory: search_docs, approve_doc, export_report
Annotation judgement: search_docs appears low-risk; approve_doc changes workflow state; export_report creates an output artefact
Behaviour classification: lookup, state change, export
Review requirements: approval state must be checked before export
Blockers: approve_doc annotation does not match behaviour
Recommended fixes: correct annotations and add negative tests
Final question: could this tool surprise a user by doing more than its description suggests?
