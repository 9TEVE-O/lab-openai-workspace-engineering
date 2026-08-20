# CAPABILITY_INGEST_TEST_002 — Task-Level Model Routing Evidence

## Status

PASS — verified by pull-request-triggered CI on the exact reviewed PR #42 head.

## Test contract

The deterministic routing test proved:

1. a task matching active `system-zero-security` domains resolves to the active T0 route;
2. the selected default and fallback models are permitted by the T0 registry contract;
3. a task matching only a planned skill does not receive an active route;
4. an unregistered task does not receive an active route;
5. no planned skill is silently promoted or activated by the test.

## Bound evidence

- Pull request: #42
- Reviewed head: `3aefbf4b87f8371f561ad69b264568b998bdb5e0`
- Merge commit: `6e287f28abeeebeee45d1555f434fb23039a6a03`
- Workflow: `CAPABILITY_INGEST_TEST_002 routing PR gate`
- Workflow run: `32379353483`
- Job: `96458436770` — `Deterministic task-level model routing`
- Job conclusion: `success`
- Test output: `CAPABILITY_INGEST_TEST_002 task-level model routing: PASS`

Observed routing result:

- security task → `system-zero-security`, T0, default `claude_opus_4_8`, fallback `gpt_5_5`;
- planned-only task → `NO_ACTIVE_ROUTE`;
- unknown task → `NO_ACTIVE_ROUTE`.

## Evidence boundary

This PASS establishes only the bounded task-level routing behaviour tested here. It does not establish production readiness, broad model quality, automatic activation of planned skills, or promotion of unrelated candidate patterns.
