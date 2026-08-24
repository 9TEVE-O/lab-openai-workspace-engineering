# MCP 2026-07-28 Canonical Integration

## Status

**Handbook canon — approved 25 August 2026.**

This record captures the evidence-verified Model Context Protocol (MCP) `2026-07-28` architecture adopted into the Applied AI Capability Research Handbook and the cross-project capability system.

Approval here establishes a reusable research/architecture reference. It does **not** establish that every LAB AI host, tool, agent or product has implemented MCP, passed production validation, or should migrate to MCP.

## Canonical decision

Use modern MCP as an increasingly credible interoperability and tool-boundary layer when independent clients, agent hosts, servers, gateways or remote tools need a shared inspectable protocol.

Do not make MCP mandatory architecture. Prefer a direct local API when it remains the smaller, safer and more observable boundary and MCP adds no concrete interoperability, deployment, governance or verification benefit.

## Verified protocol changes

### Stateless remote core

The `2026-07-28` revision removes protocol-level session dependence from the modern remote path. Requests are self-describing and can be routed independently across ordinary HTTP infrastructure.

Application state may still exist. Stateless protocol behaviour must not be misread as stateless application behaviour.

### Discovery-first negotiation

Modern clients can use `server/discover` and explicit per-request protocol metadata instead of assuming the legacy initialize/session lifecycle.

Backward compatibility and downgrade behaviour should be intentional and testable rather than inferred.

### Multi Round-Trip Requests (MRTR)

MRTR supports additional input, validation, elicitation or human participation before a request completes without requiring custom persistent-session workarounds.

This is useful for explicit human/control boundaries but does not by itself determine who is authorised to approve a consequential action.

### Authorization hardening

The 2026-07-28 direction includes stronger OAuth/OpenID-aligned validation, including issuer identification and stricter client/authorization metadata handling. Implementations must treat identity, redirect and PKCE-related metadata as security boundaries rather than convenience fields.

### HTTP-native routing, policy and caching

Method/name/version metadata and cache hints make MCP traffic more observable and governable through standard HTTP infrastructure. This can support gateway routing, policy enforcement, telemetry and stable catalogue caching without requiring every control to inspect request bodies.

### Extensions framework

MCP now has a formal extensions mechanism. Tasks, MCP Apps and Enterprise-Managed Authorization can evolve outside the core protocol.

Extension availability is not equivalent to universal maturity. Each extension must be assessed against its current specification, SDK support and the host system's actual need.

## SDK evidence boundary — verified 25 August 2026

SDK tier/version claims are time-sensitive and must be re-verified before migration or public compatibility claims.

- **C#** — Tier 1. Official v2.0 release evidence supports stable alignment with MCP `2026-07-28`.
- **Go** — Tier 1 and included in the official Tier 1 set supporting the new revision.
- **Ruby** — officially Tier 2 on the verification date. Ruby 1.0 stabilised the public API on 2025 revisions; Ruby 1.2.0 on 15 August 2026 completed the SEP-2575 stateless lifecycle and associated `2026-07-28` work. Do not attribute full new-revision lifecycle support to Ruby 1.0.
- **Kotlin** — official SDK documentation listed Tier 3 on the verification date. Do not label it Tier 2 without new authoritative evidence.
- **PHP** — official SDK documentation listed Tier 3. Stateless-core work had landed, while governance/tiering and some extension work remained separate evidence questions.

## Cross-system integration rules

### Evidence-bound and RAG systems

MCP may expose bounded retrieval, document, evidence or evaluation tools. Corpus authority, provenance, conflict handling, no-answer behaviour and release verification remain application controls outside the protocol.

### Agent and tool workflows

MCP may provide the transport/interface boundary. Worker/verifier separation, structural argument validation, tool allowlists, credential controls and human-owned consequential decisions remain independent controls where applicable.

### Observability

When MCP participates in an execution trace, record the negotiated protocol version, server/client identity, method/tool name and relevant request/task identifiers where available.

### Security

Treat tool descriptions, resource content, logs, elicited input and tool results as potentially untrusted data. MCP does not solve prompt injection, authority escalation, malicious tool semantics or unsafe host permissions by itself.

### Long-running work and UI

Use Tasks or MCP Apps when their capability and maturity materially improve the workflow. Do not add an extension merely because it exists.

### Architecture selection rule

```text
Need shared cross-component protocol boundary?
  NO  -> prefer the smaller direct interface.
  YES -> assess MCP.

MCP assessment:
  interoperability value
  + remote/deployment value
  + explicit identity/auth value
  + MRTR/Tasks/Apps value
  + gateway observability value
  > dependency + migration + attack-surface cost

If the inequality is not demonstrated, do not adopt MCP.
```

## Reusable reference pattern

```text
CLIENT / AGENT HOST
  -> DISCOVERY + AUTH
  -> MCP SERVER
  -> BOUNDED TOOL / RESOURCE / PROMPT
  -> MRTR OR TASK WHEN REQUIRED
  -> STATE EVIDENCE
  -> INDEPENDENT VERIFICATION / HUMAN GATE
```

Policy and verification remain outside the worker-facing protocol surface.

## Material limitations

- Handbook canon is not evidence that a local system has implemented MCP.
- Protocol conformance is not security assurance, correctness, production readiness or market validation.
- SDK tiers and implementation details can change after the verification date.
- Extension maturity is separate from core protocol maturity.
- MCP does not replace source authority, evidence controls, human decision rights, rollback, monitoring or deterministic verification.

## Revision triggers

Re-open this record when one of the following materially changes:

- a new MCP specification revision supersedes `2026-07-28`;
- the official roadmap changes the status of Tasks, MCP Apps, agentic messaging or transport architecture;
- an SDK tier/version claim is used for implementation or public compatibility work;
- a LAB AI host adopts MCP and produces runtime evidence requiring local implementation guidance;
- new security evidence changes the authority or threat model.

## Primary source basis

Verified against official sources on 25 August 2026:

- Model Context Protocol maintainers, **The 2026-07-28 Specification**, 28 July 2026 — https://blog.modelcontextprotocol.io/posts/2026-07-28/
- Model Context Protocol maintainers, **The New MCP Roadmap**, 22 August 2026 — https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
- Official MCP SDK documentation/tier table for the `2026-07-28` documentation set — `modelcontextprotocol/modelcontextprotocol`, `docs/docs/2026-07-28/sdk.mdx`
- Official C# SDK v2.0 release notes — `modelcontextprotocol/csharp-sdk`
- Official Ruby SDK 1.2.0 changelog and Ruby 1.0 announcement — `modelcontextprotocol/ruby-sdk` and MCP maintainers' blog

## Authority boundary

This record is the cross-project research/architecture reference for the MCP `2026-07-28` decision. Host-specific implementation evidence, tests and repository controls govern whether MCP is actually used in a particular system.
