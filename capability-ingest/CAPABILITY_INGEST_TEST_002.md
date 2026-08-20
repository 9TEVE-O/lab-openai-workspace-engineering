# CAPABILITY_INGEST_TEST_002

## Status

ACTIVE — operational shared-state reconstruction gate in progress.

## Purpose

Validate task-level model routing while proving that the active experiment can be reconstructed from durable state rather than conversational memory.

## Authoritative state

`capability-ingest/CAPABILITY_INGEST_TEST_002_STATE.json`

The durable state record controls the current task, status, requested operation, authority boundary, next permitted action and prohibited actions for this experiment.

## Admitted patterns in use

- Shared Authoritative State Surface v0.1 — admitted for bounded internal use.
- Durable Human-to-Agent Work Request v0.1 — admitted for bounded internal use.

No broader status is inferred.

## Operational pass condition

A fresh working context must be able to recover, from durable state alone:

1. task identity;
2. current status;
3. requested operation;
4. authority boundary;
5. next permitted action;
6. prohibited actions.

The fresh context must not require Steven to restate those fields manually.

## Current gate

Prepared for one real conversational restart/reconstruction cycle.

This record is not evidence that the restart gate has passed. Until a genuinely fresh context reads and correctly reconstructs the durable state, CAPABILITY_INGEST_TEST_002 remains active and incomplete.

## Stop condition

Mark the operational reconstruction gate PASS only after a fresh context independently reads the authoritative state file and reproduces the controlled fields correctly. If reconstruction fails, repair only the exposed discoverability, state-contract or authority defect before retesting.
