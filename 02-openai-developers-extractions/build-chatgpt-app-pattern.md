# Build ChatGPT App Pattern

## Core pattern

Plan the tool surface before writing app code.

## App build sequence

1. Define the app archetype
2. Define tools and side effects
3. Define schemas
4. Define UI/widget boundary
5. Define CSP/security metadata
6. Add review and approval gates where needed
7. Test positive and negative flows

## LAB reuse

For Safe Intake, prefer an interactive decoupled architecture:

```text
upload/classify/redact/review/approve/query/export
```

Keep tool behaviour separate from presentation UI.

## Review question

Can each tool be understood, tested, and blocked independently?
