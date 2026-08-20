# Intelligence Tool Library Register v1.0

## Status

Register structure recorded. This document is not evidence that any listed item has passed admission.

## Purpose

Provide a governed register for reusable AI tools, methods and operators so that discoverability is separated from authority.

## Governing rule

> Storage, repeated mentions and unversioned drafts do not create approval.

A tool becomes admitted only when its status, version, intended use, evidence and authority boundary are explicit and reviewed.

## Minimum register fields

Each admitted item must record:

- canonical name;
- version;
- status;
- intended use;
- evidence or validation basis;
- authority boundary;
- material limitations;
- owner or human decision authority where relevant;
- revision or retirement trigger.

## Lifecycle states

Recommended states include:

- candidate;
- validating;
- admitted;
- held;
- superseded;
- retired.

The exact state must be preserved rather than inferred from file location or recency.

## Current held entry

### AI Workflow Inspection Model v0.1

- Canonical name: AI Workflow Inspection Model
- Version: v0.1
- Status: held — incomplete admission record
- Intended use: GAP — not recorded
- Evidence or validation basis: GAP — no durable supporting record identified in the repository
- Authority boundary: GAP — not recorded
- Material limitations: GAP — not recorded
- Owner or human decision authority: GAP — not recorded
- Revision or retirement trigger: GAP — not recorded

Decision: do not treat this item as admitted. Admission requires every field above to be completed, the supporting evidence to be attached or durably referenced, and a human review decision to be recorded.

## Governed reusable implementation-pattern candidates

The following four patterns were retained from the Site Studio source review because they add implementation value without creating a new governance doctrine. They are registered here as **candidate reusable implementation patterns** pending implementation-level validation in a concrete host system.

### Shared Authoritative State Surface v0.1

- Status: candidate.
- Intended use: expose the same current workflow state to the human interface and agent logic so both act against one inspectable source of truth.
- Evidence basis: source-pattern extraction and architectural review; no host-system runtime validation recorded here.
- Authority boundary: does not define workflow policy, approval rights or canon. Existing host-system authority remains controlling.
- Limitation: a shared surface is not sufficient if the underlying state store permits uncontrolled mutation.
- Promotion trigger: deterministic host-system test demonstrates consistent human/agent reads and controlled writes.

### Durable Human-to-Agent Work Request v0.1

- Status: candidate.
- Intended use: persist explicit requested operations as durable workflow state rather than relying on conversational memory.
- Evidence basis: source-pattern extraction and architectural review; no host-system runtime validation recorded here.
- Authority boundary: the stored request records user intent but does not itself authorise actions outside the host system's existing permissions and approval gates.
- Limitation: stale, superseded or completed requests require explicit lifecycle handling.
- Promotion trigger: host-system test demonstrates persistence, status transitions and correct refusal of unauthorised operations.

### Structured Agent Proposal v0.1

- Status: candidate cross-project pattern.
- Intended use: represent proposed agent changes as current state, proposed state, reason, diff and accept/reject decision so consequential mutation remains inspectable and human-owned where required.
- Evidence basis: source-pattern extraction and architectural review. `stevens-creative-software` already contains a compatible proposal → preview → accept/reject → project-version architecture, but that is not treated here as cross-project runtime validation.
- Authority boundary: proposal generation cannot bypass existing human decision rights, evidence gates or change-control rules.
- Limitation: proposal structure does not prove the proposed change is correct.
- Promotion trigger: host-system test demonstrates accurate diff generation, explicit decision capture and no mutation before acceptance where approval is required.

### Lightweight Live State Synchronisation v0.1

- Status: candidate.
- Intended use: pair a controlled mutation boundary with event-driven UI refresh so local-first tools update visible state without hidden side channels or conversational-memory dependence.
- Evidence basis: source-pattern extraction and architectural review; no host-system runtime validation recorded here.
- Authority boundary: synchronisation transports state changes; it does not create permission to make them.
- Limitation: event delivery, race conditions, restart recovery and stale clients require host-specific testing.
- Promotion trigger: host-system test demonstrates authorised mutation, event propagation, restart consistency and stale-state detection.

## Site Studio placement rule

These four items belong in this existing register as reusable implementation-pattern candidates. They are not a separate Tool Bank, product, governance framework or authority layer.

When implementation begins, apply them inside the relevant host repository under that repository's controlling architecture and gates. In `stevens-creative-software`, structured proposal/accept-reject behaviour already exists architecturally; the other patterns should be implemented only where they fill a demonstrated state-management or orchestration gap. This register remains the cross-project discovery and status record; host-specific code remains in the host repository.

## Control boundary

This register is an authority map, not proof of correctness. A held item remains non-admitted even if it is implemented, stored elsewhere or repeatedly referenced. Candidate status means an item is discoverable and intentionally retained but has not yet earned admission. Admission for a stated use does not imply production readiness, regulatory compliance, external validation or commercial adoption.
