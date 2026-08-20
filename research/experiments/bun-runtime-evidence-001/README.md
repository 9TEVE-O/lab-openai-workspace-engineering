# BUN_RUNTIME_EVIDENCE_001

## Status

**Active bounded experiment — candidate under validation.**

## Objective

Test whether Bun's Markdown CPU profiler produces materially useful, machine-readable runtime evidence for AI-assisted diagnosis without changing the repository's authorised runtime architecture.

## Scope

This experiment uses one deterministic JavaScript workload that runs unchanged under Node.js and Bun 1.4. It records correctness output, timing evidence, and Bun's Markdown CPU profile.

Bun is installed only inside the experiment workflow. This does not adopt Bun as a repository runtime, package manager, build system or production dependency.

## Test sequence

1. Run `workload.mjs` with the GitHub runner's current Node.js runtime.
2. Install Bun 1.4.0 for this workflow only.
3. Run the exact same workload with Bun 1.4.0.
4. Assert Node and Bun produce the same deterministic result.
5. Run the workload again under `bun --cpu-prof-md`.
6. Assert that a non-empty Markdown profile is produced.
7. Surface the profile in the workflow log for direct agent inspection.
8. Identify one evidence-supported optimisation only if the profile exposes a clear hotspot.
9. Apply that optimisation only on this experiment branch, rerun the identical correctness gate and compare before/after evidence.

## Acceptance criteria

The candidate passes this experiment only if all of the following hold:

- the same workload produces identical deterministic output under Node and Bun;
- Bun 1.4.0 emits a non-empty Markdown CPU profile;
- the profile identifies runtime behaviour with enough source/function specificity to support a bounded diagnosis;
- any optimisation proposed from the profile preserves deterministic output;
- before/after evidence can show whether the change helped rather than relying on an implementation claim;
- no existing runtime, package-management or architectural authority is changed.

## Failure conditions

Fail or leave the capability as unverified if:

- Bun changes workload correctness;
- profiling output is absent, unstable or too vague to support diagnosis;
- the profile cannot be consumed directly from durable workflow evidence;
- an apparent optimisation cannot be verified with the same workload;
- the test requires migration or weakening existing controls to succeed.

## Authority boundary

This experiment may create test-only files, a test-only GitHub Actions workflow and evidence on this branch. It does not authorise migration to Bun or modification of Steven's Creative Software.

## Stop condition

Stop when one before/after profiling cycle has either demonstrated materially useful machine-readable runtime evidence or shown that the capability does not earn promotion beyond candidate status.
