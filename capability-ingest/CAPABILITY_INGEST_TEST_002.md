# CAPABILITY_INGEST_TEST_002

## Status

COMPLETED — both bounded operational gates passed with durable repository evidence.

## Purpose

Validate task-level model routing while proving that the experiment can be reconstructed from durable state rather than conversational memory.

## Authoritative state

`capability-ingest/CAPABILITY_INGEST_TEST_002_STATE.json`

The durable state record controls the final task status, gate evidence, authority boundary and closure conditions for this experiment.

## Admitted patterns in use

- Shared Authoritative State Surface v0.1 — admitted for bounded internal use.
- Durable Human-to-Agent Work Request v0.1 — admitted for bounded internal use.

No broader status is inferred.

## Gate results

### Restart-safe reconstruction

PASS.

A fresh working context recovered from durable state alone:

1. task identity;
2. current status;
3. requested operation;
4. authority boundary;
5. next permitted action;
6. prohibited actions.

Evidence: `capability-ingest/CAPABILITY_INGEST_TEST_002_RECONSTRUCTION_EVIDENCE_001.md`, merged through PR #40.

### Task-level model routing

PASS.

The pull-request-triggered deterministic CI gate on PR #42 verified that:

- an active security-domain task routes to `system-zero-security` under the T0 model contract;
- a task matching only a planned skill receives `NO_ACTIVE_ROUTE`;
- an unregistered task receives `NO_ACTIVE_ROUTE`;
- planned skills are not silently activated.

Evidence: `capability-ingest/CAPABILITY_INGEST_TEST_002_ROUTING_EVIDENCE_PENDING.md`, workflow run `32379353483`, job `96458436770`.

## Evidence boundary

Completion establishes the bounded behaviours tested by this experiment. It does not establish production readiness, broad model quality, general cross-system validity, or promotion of Structured Agent Proposal v0.1 or Lightweight Live State Synchronisation v0.1.

## Closure

`CAPABILITY_INGEST_TEST_002` is closed. Reopen only if new evidence exposes a material defect in the tested reconstruction or routing behaviour.
