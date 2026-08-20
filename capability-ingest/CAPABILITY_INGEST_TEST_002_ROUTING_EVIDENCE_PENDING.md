# CAPABILITY_INGEST_TEST_002 — Task-Level Model Routing Evidence

## Status

PENDING — evidence record created to trigger and bind the pull-request verification gate.

## Test contract

The deterministic routing test must prove:

1. a task matching active `system-zero-security` domains resolves to the active T0 route;
2. the selected default and fallback models are permitted by the T0 registry contract;
3. a task matching only a planned skill does not receive an active route;
4. an unregistered task does not receive an active route;
5. no planned skill is silently promoted or activated by the test.

## Evidence boundary

Do not mark this gate PASS from implementation alone. PASS requires the pull-request-triggered CI execution of `capability-ingest/task-level-model-routing-test.py` to succeed on the exact reviewed head commit.
