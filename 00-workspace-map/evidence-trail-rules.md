# Evidence Trail Rules

Evidence trails make AI work reviewable after the chat is gone.

## Minimum evidence record

For any reusable workflow, capture:

- Source or input used
- What the AI was asked to do
- Key assumptions
- Output produced
- Review decision
- Known limitations
- Next action

## Claim labels

Use these labels when writing analysis or documentation:

| Label | Meaning |
|---|---|
| FACT | Directly supported by a source or observed system behaviour |
| INFERENCE | Reasonable conclusion drawn from available evidence |
| ASSUMPTION | Working belief that still needs confirmation |
| GAP | Missing information or unresolved uncertainty |
| DECISION | Chosen action or rule |
| RISK | Known failure mode, exposure, or constraint |

## Blockers

Do not mark a workflow as ready if:

- Sources are missing for material claims
- Side effects are unclear
- Approval gates are not defined
- Sensitive data handling is not described
- Test cases only cover happy paths
- The output cannot be reviewed by another person

## Final review question

Can someone else inspect this later and understand what happened, why it happened, and what evidence supported the decision?
