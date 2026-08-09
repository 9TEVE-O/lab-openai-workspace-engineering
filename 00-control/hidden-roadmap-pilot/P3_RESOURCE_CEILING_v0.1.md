# Hidden Roadmap P3 Resource Ceiling v0.1

**Status:** CANDIDATE FOR FREEZE  
**Parent:** `HIDDEN_ROADMAP_PILOT_EXECUTION_CONTRACT_v0.1`  
**R0:** `6a456830ca33eb5edaa634a9b0febe5d71bea2be`

## 1. Scope

This ceiling bounds execution resources for the five-feature systems-validation pilot. It does not alter feature requirements or condition semantics.

## 2. Producer-model invocation ceiling

A producer-model invocation is one top-level producer response initiated from an authorised context state. Tool calls occurring inside that top-level response are part of the same invocation. A retry is excluded only when it uses identical inputs after a confirmed infrastructure failure and no model output from the failed attempt was exposed to the workflow.

Per checkpoint maximums:

- Condition A: 9 invocations.
  - up to 8 implementation/debug invocations;
  - up to 1 end-of-feature human-review repair invocation.
- Condition B: 10 invocations.
  - Condition A allowance;
  - exactly 1 reserved same-model self-review invocation.
- Condition C: 12 invocations.
  - Condition B allowance;
  - up to 2 verifier-triggered repair invocations.
- Condition D: same 12-invocation base ceiling as C.
  - additionally, at most 3 evidence-only invocations may be authorised by `REQUEST_BOUNDED_EVIDENCE`, one per authorised decision-boundary consultation;
  - therefore absolute D maximum = 15 invocations.

Unused phase-specific allowances may not be silently reallocated to another phase.

## 3. Active execution time

Per checkpoint:

- producer active engineering runtime: maximum 60 minutes;
- mechanical verifier runtime is excluded from producer active time and bounded separately;
- human engineering time is measured under the H protocol and bounded below;
- infrastructure/admin time remains `H_admin` / infrastructure evidence and does not extend producer active time unless the checkpoint is explicitly resumed after a classified infrastructure interruption.

At the 60-minute producer ceiling the workflow stops and records `RESOURCE_EXHAUSTION` unless the candidate had already been submitted.

## 4. Tool-runtime container ceiling

All repository tool execution for benchmark-controlled runs uses the frozen P1 Linux/amd64 environment with:

- CPU limit: `2.0` CPUs;
- memory limit: `2 GiB`;
- PID limit: `512`;
- outbound network disabled after the environment and repository are materialised;
- temporary storage limit: `2 GiB` outside the Git checkout and benchmark evidence mount.

Model-provider transport is outside this tool container and does not authorise repository network access.

## 5. Verifier runtime ceiling

- each individual verifier command: maximum 120 seconds unless a stricter pre-registered feature/NFI threshold applies;
- complete final verifier sequence: maximum 300 seconds;
- verifier timeout is a `VERIFIER` or `INFRASTRUCTURE` event according to cause, not an automatic software failure.

## 6. Human bounds

Common end-of-feature review:

- maximum 12 active `H_eng` minutes per checkpoint;
- one ACCEPT/REPAIR decision;
- one bounded repair round as already defined by the execution contract.

Condition D decision-boundary consultation:

- maximum 3 consultations per checkpoint;
- maximum 8 active `H_eng` minutes per consultation;
- at most one `REQUEST_BOUNDED_EVIDENCE` producer invocation per consultation;
- unused consultation/evidence allowance cannot be converted into general implementation assistance.

The U diagnostic remains separately capped at 12 active minutes by the parent contract.

## 7. Pre-registered Condition-D scope trigger

The `unexpected implementation expansion` decision boundary fires when the proposed/current implementation exceeds either threshold relative to the checkpoint start SHA:

- more than 8 production Python files under `sqlite_utils/` modified; or
- more than 500 production-source lines of churn (`added + deleted`) under `sqlite_utils/`.

Tests, documentation, benchmark-control files and generated artefacts are excluded from this trigger.

Crossing the threshold does not fail the checkpoint. In Condition D it requires a decision-boundary packet before further implementation. In A/B/C the measurement is recorded only and does not introduce human consultation.

## 8. Exhaustion rule

A ceiling may not be extended after seeing condition performance. If a ceiling is reached:

1. stop the affected phase;
2. retain the current candidate/evidence;
3. record `RESOURCE_EXHAUSTION`;
4. continue to the applicable verifier/acceptance classification where procedurally possible.

No condition-specific discretionary extension is permitted.
