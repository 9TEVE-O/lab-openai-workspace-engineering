# SHARED_STATE_DURABLE_REQUEST_TEST_001

## Status

PASS — bounded deterministic host-system validation completed on 2026-08-20.

## Patterns under test

- Shared Authoritative State Surface v0.1
- Durable Human-to-Agent Work Request v0.1

## Host system

`lab-openai-workspace-engineering`

## Pass condition

After conversation context is removed or restarted, both the human interface and agent must independently reconstruct the same current task, status, requested operation and authority boundary from durable state, while unauthorised writes are rejected.

## Durable state contract

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

The durable record, not conversation history, is authoritative for these fields.

## Executable harness

`capability-ingest/shared-state-durable-request-test.js`

Harness commit: `1228078ca35baab49b3cdea1a914ada367beb30b`

The harness creates a fresh durable state file, performs independent reads, attempts an unauthorised mutation, performs an authorised mutation, and then performs independent fresh reads again.

## Execution evidence

Result: `PASS`

### Pre-write reconstruction

Human reconstruction and fresh-agent reconstruction were identical:

```text
task = Verify restart-safe shared workflow state
status = requested
requested_operation = reconstruct-and-advance-after-authorised-write
read_authority = human, agent
write_authority = human-authorised-agent
forbidden_writer = unauthorised-agent
revision = 1
```

### Unauthorised write

Actor: `unauthorised-agent`

Attempted mutation:

```json
{
  "status": "completed",
  "revision": 2
}
```

Result: rejected.

The durable state remained unchanged at `status=requested`, `revision=1`.

### Authorised write

Actor: `human-authorised-agent`

Mutation:

```json
{
  "status": "in_progress",
  "revision": 2
}
```

Result: accepted.

### Post-write restart reconstruction

Fresh human and agent reads were identical:

```text
task = Verify restart-safe shared workflow state
status = in_progress
requested_operation = reconstruct-and-advance-after-authorised-write
read_authority = human, agent
write_authority = human-authorised-agent
forbidden_writer = unauthorised-agent
revision = 2
```

## Determination

All bounded pass criteria were satisfied:

1. durable state alone reconstructed the current work request;
2. independent human and fresh-agent reads matched;
3. no conversational state was required by the executable test;
4. an unauthorised mutation was rejected and left durable state unchanged;
5. an authorised mutation succeeded;
6. independent post-write reads reconstructed the same new state.

## Promotion decision

Promote the following patterns from `candidate` to `admitted — bounded use`:

- Shared Authoritative State Surface v0.1
- Durable Human-to-Agent Work Request v0.1

### Admitted intended use

Use a durable authoritative work record so human and agent participants can reconstruct the same task, status, requested operation and authority boundary after conversational restart, with writes constrained by an explicit actor-authority check.

### Authority boundary

This admission does not create new workflow permissions. Existing host-system policy, human approval rights and repository controls remain controlling.

### Limitations

This test does not establish:

- production readiness;
- distributed or concurrent consistency;
- crash-safe transactional persistence;
- cryptographic actor identity;
- security or regulatory compliance;
- cross-host portability;
- event-driven synchronisation;
- commercial validity.

`Structured Agent Proposal v0.1` and `Lightweight Live State Synchronisation v0.1` were not tested here and remain candidates.

## Review decision

PASS accepted for bounded internal admission only. Any materially broader use requires further host-specific validation.
