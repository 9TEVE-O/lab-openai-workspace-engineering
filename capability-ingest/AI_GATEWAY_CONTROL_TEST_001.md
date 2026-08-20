# AI_GATEWAY_CONTROL_TEST_001

Status: ACTIVE EXPERIMENT
Source family: TrueForge / TrueFoundry agent-harness extraction
Controlling role: This file is the canonical experiment record. Conversation memory is continuity only, not proof.

## Decision

Test one bounded capability: whether a shared, model-independent gateway/control boundary can enforce model and tool authority outside the reasoning agent.

Do not adopt TrueForge wholesale. Do not create separate projects for each extracted pattern.

## Target architecture

Agent / AI application
→ Gateway / control plane
→ Session
→ Turn
→ Per-turn resource resolution
→ Policy / approval
→ Model, MCP tool or isolated sandbox execution
→ Event stream / trace
→ Durable artefacts and result

## Capabilities under test

The gateway should independently enforce:

1. model access/routing;
2. MCP/tool access;
3. budget or bounded-resource policy;
4. approval interception;
5. trace/audit capture.

Supporting implementation requirements:

- consequential approval cannot be bypassed by the reasoning agent;
- credentials remain outside the agent and are scoped at the harness/gateway/sandbox boundary;
- canonical application state is provider-neutral;
- provider-specific compacted context is runtime state, not authoritative memory;
- tools, skills and context may be resolved per turn rather than permanently exposed;
- execution should emit inspectable structured events.

## Acceptance gate

PASS only if a minimal proof-of-concept demonstrates all seven conditions:

1. An agent requests a tool/action.
2. The gateway intercepts the request.
3. Policy permits, denies or pauses it.
4. A required human approval cannot be bypassed by the agent.
5. Execution resumes correctly after approval.
6. The complete sequence produces an inspectable trace.
7. Changing the underlying model does not remove those controls.

Additional required check: the agent must not receive unrestricted credentials directly.

FAIL or REVISE if any control depends only on prompt compliance, hidden model state, or an unverifiable implementation claim.

## Extracted reference patterns

These are supporting reference, not independently active projects.

### SESSION_TURN_EVENT_MODEL

Treat the session as the durable container, each turn as a bounded execution unit, events as observable occurrences, and artefacts as durable outputs. This supports replay, evaluation, debugging and provenance.

### JIT_RESOURCE_RESOLUTION

Capability availability and capability activation are separate. Resolve only the models, tools, skills, sandbox and context required for the current turn where practical.

### PROVIDER_NEUTRAL_STATE

Keep evidence references, decisions, approvals, artefacts and task state in canonical application state. Treat provider-specific conversation/compaction state as replaceable runtime state.

### STRUCTURED_AGENT_UI_PATTERN

Agents should emit structured semantic events such as approval_required, tool_started, tool_completed, artefact_created and turn_completed. Presentation belongs to the application/UI layer.

### AGENT_VS_REQUEST_REPLY

Use an agent only when a stateful, interruptible, multi-step execution loop earns its complexity. Use bounded request/reply for deterministic extraction, classification or structured model judgements.

### LOCAL_TO_HOSTED_PROGRESSION

Prove behaviour locally with minimal infrastructure first. Introduce production persistence, distributed infrastructure, authentication and deployment complexity only after the capability passes its behavioural gate.

### VERSIONED_SKILLS

Reusable AI capabilities should become identifiable, versioned and traceable instruction/code packages rather than existing only as prose in conversation memory.

## Evidence status

Verified from the TrueForge public repository/documentation during extraction:

- monorepo separation between core/runtime, server/harness, SDK, UI SDK and frontend;
- first-class session and turn implementation;
- per-turn resource resolver interfaces/implementation;
- model-provider support and MCP/tool integration;
- human checkpoints/tool approval;
- context-engineering features including subagents, deferred tool loading, large-result offloading and compaction;
- local SQLite mode and hosted Postgres/Redis modes;
- OpenAPI/SDK boundary;
- git-backed skills and sandbox-as-tool architecture.

Not yet verified for this experiment:

- that our own implementation enforces these controls correctly;
- cross-model invariance of the gateway controls;
- actual token/cost benefit from JIT context or compaction in our workloads;
- production readiness;
- security properties beyond the bounded test.

## Scope exclusions

Do not:

- reproduce the full TrueForge platform;
- introduce Kubernetes/Helm/Redis/Postgres merely for this test;
- claim production readiness;
- treat vendor benchmarks as proof of our performance;
- create separate active projects for the extracted patterns;
- expand into general agent-framework comparison unless a failed test creates a specific evidence gap.

## Minimal implementation sequence

1. Define one mock or low-consequence tool action.
2. Put a gateway/policy interceptor between agent request and execution.
3. Implement allow / deny / approval-required policy outcomes.
4. Persist a minimal Session → Turn → Event trace.
5. Demonstrate blocked execution pending approval.
6. Resume the same turn after approval and record the result.
7. Repeat with a second model/provider while keeping gateway policy unchanged.
8. Record PASS / FAIL / REVISE against every acceptance condition.

## Stopping condition

Stop when the seven acceptance conditions and credential-boundary check have objective evidence.

If PASS: promote only the demonstrated gateway-control pattern as reusable capability.
If FAIL: record the failure and close unless one narrow reversible repair is justified.
If REVISE: make only the smallest repair needed to rerun the failed gate.
