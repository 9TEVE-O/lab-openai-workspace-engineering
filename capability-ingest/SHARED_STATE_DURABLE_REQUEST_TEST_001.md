# SHARED_STATE_DURABLE_REQUEST_TEST_001

## Status

Validating — deterministic host-system test specification and evidence record.

This record does not promote either pattern to admitted capability until the pass conditions below are satisfied by inspectable runtime evidence.

## Patterns under test

- Shared Authoritative State Surface v0.1
- Durable Human-to-Agent Work Request v0.1

## Host system

`lab-openai-workspace-engineering`

The host-system authority and repository controls remain controlling. This test does not create new approval rights or bypass existing gates.

## Objective

Demonstrate that a workflow task can be reconstructed after conversational context is removed or restarted from one durable, authoritative state record, and that unauthorised writes are rejected.

## Minimal durable state contract

A durable work record MUST contain:

```json
{
  "task_id": "STATE_TEST_001",
  "task": "Verify restart-safe shared workflow state",
  "status": "requested",
  "requested_operation": "reconstruct-and-advance-after-authorised-write",
  "authority": {
    "read": ["human", "agent"],
    "write": ["human-authorised-agent"],
    "forbidden": ["unauthorised-agent"]
  },
  "revision": 1
}
```

The durable record, not conversation history, is the source of truth for these fields.

## Deterministic test procedure

### T1 — Seed durable state

Create the durable record exactly as specified above.

Expected result:

- record is persisted;
- revision is `1`;
- no conversational context is required to interpret the task.

### T2 — Human reconstruction

With no access to prior conversation, read only the durable record and reconstruct:

- current task;
- status;
- requested operation;
- authority boundary.

Expected result:

```text
task = Verify restart-safe shared workflow state
status = requested
requested_operation = reconstruct-and-advance-after-authorised-write
read_authority = human, agent
write_authority = human-authorised-agent
forbidden_writer = unauthorised-agent
```

### T3 — Agent reconstruction after restart

Simulate a fresh agent session with no conversation history. Provide access only to the durable record.

The agent MUST return the same six values as T2.

Pass criterion: byte-for-byte equality after canonical serialisation of the reconstructed state fields.

### T4 — Unauthorised write rejection

Attempt this mutation using actor `unauthorised-agent`:

```json
{
  "status": "completed",
  "revision": 2
}
```

Expected result:

- mutation rejected;
- durable record unchanged;
- status remains `requested`;
- revision remains `1`.

### T5 — Authorised write

Attempt this mutation using actor `human-authorised-agent`:

```json
{
  "status": "in_progress",
  "revision": 2
}
```

Expected result:

- mutation accepted;
- durable record status becomes `in_progress`;
- revision becomes `2`.

### T6 — Restart consistency

Simulate another fresh human read and fresh agent read after T5, again without conversation history.

Both MUST independently reconstruct:

```text
task = Verify restart-safe shared workflow state
status = in_progress
requested_operation = reconstruct-and-advance-after-authorised-write
read_authority = human, agent
write_authority = human-authorised-agent
forbidden_writer = unauthorised-agent
revision = 2
```

## Pass condition

PASS only if all of the following are demonstrated:

1. the human reconstruction succeeds from durable state alone;
2. the restarted-agent reconstruction succeeds from durable state alone;
3. both reconstructions are identical for the controlled fields;
4. the unauthorised mutation is rejected and leaves durable state unchanged;
5. the authorised mutation succeeds;
6. both fresh readers reconstruct the authorised post-write state identically;
7. no test step relies on hidden conversational state.

Any failure means the patterns remain `candidate` and this test remains unresolved.

## Promotion boundary

A PASS supports promotion of:

- Shared Authoritative State Surface v0.1; and
- Durable Human-to-Agent Work Request v0.1

only for the stated, bounded use demonstrated by this host-system test.

PASS does not establish production readiness, distributed consistency, resilience under concurrency, security compliance, cross-system portability or commercial validity.

## Evidence required before promotion

Record the following in this file or a linked immutable test output:

- exact durable-state input;
- human reconstruction output;
- restarted-agent reconstruction output;
- unauthorised-write result;
- authorised-write result;
- post-write restart reconstruction outputs;
- test execution identifier or commit SHA;
- review decision.

## Current result

NOT YET EXECUTED.

The test specification is now durable. Candidate status remains unchanged until runtime evidence is attached and reviewed.
