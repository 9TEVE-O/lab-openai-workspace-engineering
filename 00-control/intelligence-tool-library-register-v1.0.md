# Intelligence Tool Library Register v1.0

## Status

Register structure recorded. This document is not evidence that any listed item has passed admission unless an item below explicitly records an evidence-backed admission decision.

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

## Governed reusable implementation patterns

The following four patterns were retained from the Site Studio source review because they add implementation value without creating a new governance doctrine. Status is recorded per item and must not be generalised across the group.

### Shared Authoritative State Surface v0.1

- Status: admitted — bounded internal use.
- Intended use: expose the same current workflow task, status, requested operation and authority boundary to human and agent readers from one durable inspectable source of truth, including after conversational restart.
- Evidence basis: `capability-ingest/SHARED_STATE_DURABLE_REQUEST_TEST_001.md` and executable harness `capability-ingest/shared-state-durable-request-test.js`; deterministic test PASS recorded 2026-08-20.
- Authority boundary: does not define workflow policy, approval rights or canon. Existing host-system authority remains controlling.
- Material limitations: admission does not establish distributed consistency, concurrent-write safety, crash-safe transactions, cryptographic actor identity, production readiness, compliance, cross-host portability or commercial validity.
- Owner or human decision authority: consequential permissions and promotion remain human-owned under the host system's existing controls.
- Revision or retirement trigger: materially broader use, changed state contract, changed mutation boundary or evidence of inconsistent reconstruction requires retest and review.

### Durable Human-to-Agent Work Request v0.1

- Status: admitted — bounded internal use.
- Intended use: persist an explicit work request and its lifecycle-relevant fields as durable workflow state so a fresh human or agent session can reconstruct the request without relying on conversational memory.
- Evidence basis: `capability-ingest/SHARED_STATE_DURABLE_REQUEST_TEST_001.md` and executable harness `capability-ingest/shared-state-durable-request-test.js`; deterministic test PASS recorded 2026-08-20, including rejection of an unauthorised mutation and acceptance of an authorised mutation.
- Authority boundary: the stored request records user intent but does not itself authorise actions outside the host system's existing permissions and approval gates.
- Material limitations: stale, superseded or completed request lifecycle handling beyond the tested transition remains host-specific; admission does not establish production security, distributed consistency or cross-host portability.
- Owner or human decision authority: consequential permissions remain human-owned under the host system's existing controls.
- Revision or retirement trigger: materially broader lifecycle states, actor model, permissions model or host architecture requires retest and review.

### Structured Agent Proposal v0.1

- Status: admitted — bounded internal use.
- Intended use: represent proposed agent changes as current state, proposed state, reason, diff and accept/reject decision so consequential mutation remains inspectable and human-owned where required.
- Evidence basis: `capability-ingest/SITE_STUDIO_PATTERN_VALIDATION_001.md`; bounded host-system implementation in `9TEVE-O/stevens-creative-software`; validation PR `#4`; GitHub Actions run `32401800419` completed successfully; merged commit `d7c3be851171d208ce1817969526462750b99608`.
- Authority boundary: proposal generation cannot bypass existing human decision rights, evidence gates or change-control rules. Acceptance is a decision input to the controlled mutation path, not proof that the proposed change is correct.
- Material limitations: admission is bounded to the tested host architecture and does not establish correctness of proposals, production readiness, cross-host portability, external validation or commercial validity.
- Owner or human decision authority: consequential proposal acceptance/rejection remains human-owned where required by the host system.
- Revision or retirement trigger: materially changed proposal schema, approval semantics, mutation path or host authority model requires retest and review.

### Lightweight Live State Synchronisation v0.1

- Status: admitted — bounded internal use.
- Intended use: pair a controlled mutation boundary with event-driven state refresh so local-first tools update visible state without hidden side channels or conversational-memory dependence.
- Evidence basis: `capability-ingest/SITE_STUDIO_PATTERN_VALIDATION_001.md`; bounded host-system implementation in `9TEVE-O/stevens-creative-software`; validation PR `#4`; GitHub Actions run `32401800419` completed successfully; merged commit `d7c3be851171d208ce1817969526462750b99608`.
- Authority boundary: synchronisation transports authorised state changes; it does not create permission to make them. The tested implementation enforces authorisation and revision-based stale-state rejection at the controlled mutation boundary.
- Material limitations: admission is bounded to the tested local host architecture and does not establish distributed consistency, multi-process coordination, guaranteed network delivery, crash-safe transactions, cryptographic actor identity, production readiness, cross-host portability or commercial validity.
- Owner or human decision authority: consequential permissions remain governed by the host system; event subscribers receive state but do not gain mutation authority.
- Revision or retirement trigger: materially changed event transport, state revision model, persistence/restart strategy, actor/permission model or host architecture requires retest and review.

## Site Studio placement rule

These four items belong in this existing register as reusable implementation patterns. They are not a separate Tool Bank, product, governance framework or authority layer.

When implementation begins, apply them inside the relevant host repository under that repository's controlling architecture and gates. In `stevens-creative-software`, all four now have bounded internal validation evidence for their recorded use; broader adoption remains subject to the limitations and retest triggers above. This register remains the cross-project discovery and status record; host-specific code remains in the host repository.

## Control boundary

This register is an authority map, not proof of correctness. A held item remains non-admitted even if it is implemented, stored elsewhere or repeatedly referenced. Candidate status means an item is discoverable and intentionally retained but has not yet earned admission. Admission is bounded to the stated use and evidence basis and does not imply production readiness, regulatory compliance, external validation or commercial adoption.
