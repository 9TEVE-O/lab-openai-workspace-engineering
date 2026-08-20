# BUN_BUILD_EVIDENCE_001

## Status

**Active bounded experiment — candidate under validation.**

## Provenance correction

`bun build --metafile-md` is available in Bun 1.4, but it was introduced earlier in Bun 1.3.8. This experiment therefore validates Machine-Readable Build Evidence as a useful Bun capability relative to the current development architecture; it does not claim the feature was introduced by Bun 1.4.

## Objective

Test whether Bun's Markdown build metafile makes a known dependency-graph change directly discoverable and agent-inspectable without changing the repository's authorised runtime or package-management architecture.

## Controlled fixture

Two tiny TypeScript fixtures are built with the same Bun version and build settings:

- `baseline/` imports only `core.ts`;
- `candidate/` preserves the same core path and adds one known dependency, `audit.ts`, which is used by the entrypoint so it cannot be tree-shaken away.

This is intentionally a controlled fixture rather than an application migration.

## Test sequence

1. Install Bun 1.4.0 inside the workflow only.
2. Build baseline and candidate fixtures with JSON and Markdown metafiles.
3. Assert both builds succeed.
4. Assert the JSON metafiles show the candidate has exactly one additional source input: `audit.ts`.
5. Assert the baseline Markdown report does not contain `audit.ts` and the candidate Markdown report does.
6. Surface both Markdown reports in the workflow log for direct agent inspection.
7. Record module counts and output-size delta as durable evidence.
8. Decide PASS only if the known structural change is directly discoverable from the generated evidence.

## Acceptance criteria

- both builds succeed under Bun 1.4.0;
- baseline and candidate use the same build settings;
- the JSON metafile deterministically proves the known graph delta;
- the Markdown metafile exposes that delta in agent-readable form;
- no repository runtime or package-manager migration occurs;
- no claim is made that `--metafile-md` originated in Bun 1.4.

## Stop condition

Stop after one controlled baseline/candidate build-evidence comparison establishes whether the report makes the known dependency change directly discoverable.
