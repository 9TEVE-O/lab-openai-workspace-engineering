# MCP Tool Review Proof Pack

## Plain-English summary

This proof pack shows how an MCP or app toolset can be reviewed before use. The review checks whether tool names, descriptions, schemas, annotations, and behaviour line up.

The proof is that a tool should not be trusted just because its name sounds safe. Its declared behaviour must match what it can actually do.

## Workflow map

```text
Tool list received
→ descriptions reviewed
→ schemas checked
→ implementation behaviour inspected
→ annotations compared
→ side effects classified
→ blockers recorded
→ fixes recommended
```

## Evidence table

| Claim | Evidence | Status |
|---|---|---|
| Tool inventory is required | Review starts by listing every tool | FACT |
| Declared behaviour must match real behaviour | Review compares names, descriptions, schemas, and implementation | FACT |
| Missing or unclear annotations create review risk | Tool-hint review skill flags unclear or missing annotations | FACT |
| Runtime safety is proven | Not proven without running the toolset | GAP |

## What was tested

- tool inventory completeness
- tool name versus description
- description versus schema
- schema versus implementation
- annotation alignment
- side-effect classification
- blocked or unclear behaviour

## What was blocked

- treating tool names as proof of behaviour
- accepting unclear annotations
- approving tools without implementation review
- treating missing schemas as ready for submission

## Human review points

- reviewer confirms whether implementation details are available
- reviewer checks whether annotations match behaviour
- reviewer decides whether blockers must be fixed before use

## Known limitations

- This proof pack is a review pattern, not a runtime security test.
- It does not prove the tool works correctly in production.
- It does not replace app-specific permission testing.
- It requires implementation access for complete judgement.

## Next decision

Create a reusable MCP/App review harness that can be applied to any app or tool repo before submission or client review.
