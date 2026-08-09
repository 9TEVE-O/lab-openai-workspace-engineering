# Hidden Roadmap P5 Persistent Non-Functional Invariants — Public Surface v0.1

**Status:** CANDIDATE FOR FREEZE  
**Parent:** `HIDDEN_ROADMAP_PILOT_EXECUTION_CONTRACT_v0.1`  
**R0:** `6a456830ca33eb5edaa634a9b0febe5d71bea2be`

The invariant set is fixed before trajectory execution. To preserve the hidden roadmap, this public file exposes only invariants already meaningful at R0 plus the activation protocol. Future-activated invariant details are committed by hash and remain in custody until their checkpoint is authorised.

## NFI-R0-01 — Backwards compatibility / regression stability

Property: previously accepted repository behaviour remains functional.

Check:

```text
python -m pytest -q -p no:cacheprovider
```

Threshold: exit code 0.  
Blocking: YES.  
Activation: R0 onward.  
Evidence: pytest output, exit code, elapsed time.

## NFI-R0-02 — Transactional recoverability

Property: a migration that fails inside the existing transactional migration path must not leave its migration side effects or an applied-history record committed; the migration must remain retryable.

Check: benchmark-owned deterministic fixture in the active NFI suite.

Threshold:

- intentional transactional failure leaves no committed fixture side effect;
- no applied-history row for the failed migration;
- a subsequent successful application applies exactly once.

Blocking: YES.  
Activation: R0 onward.

## NFI-R0-03 — Existing read-only migration inspection remains non-mutating

Property: existing migration inspection must not create or mutate application state.

At R0 the applicable surface is `migrate --list`.

Threshold:

- missing database path remains absent after inspection;
- for an existing fixture database, SHA-256 of the database file is identical before and after inspection;
- no migration function executes.

Blocking: YES.  
Activation: R0 onward.

## Future activation protocol

The complete invariant table was defined before trajectory execution and is custody-held. When checkpoint `Fi` is revealed:

1. the custodian releases the NFI packet whose activation point is `Fi` or earlier;
2. its SHA-256 is verified against the pre-run commitment;
3. that packet becomes part of the producer's authorised current-state context;
4. once activated, an invariant remains active at all later checkpoints;
5. no invariant may be added, removed, weakened or strengthened after condition outcomes are observed.

Future-activated invariant plaintext must not be supplied to a producer before its activation checkpoint.

## Blocking interpretation

A blocking NFI failure contributes to checkpoint `FAIL` under the execution contract. A verifier/infrastructure inability to perform the check is classified separately and does not become a software failure by assumption.

The complete committed NFI bundle and feature-specific acceptance suites are represented by `P4_P5_COMMITMENT_v0.1.json`.
