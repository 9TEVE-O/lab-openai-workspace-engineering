# BUN_RUNTIME_EVIDENCE_001

## Status

**PASS — validated for bounded use.**

The validated capability is **Machine-Readable Runtime Evidence** using Bun 1.4 Markdown CPU profiling as one implementation. This result does not adopt Bun as the repository runtime, package manager, build system or production dependency.

## Objective

Test whether Bun's Markdown CPU profiler produces materially useful, machine-readable runtime evidence for AI-assisted diagnosis without changing the repository's authorised runtime architecture.

## Evidence

The test used one deterministic 50,000,000-iteration workload with a retained pre-optimisation baseline and one profile-directed candidate change.

- Node.js and Bun produced the same deterministic result: `{"iterations":50000000,"score":1943356937}`.
- Bun 1.4.0 generated non-empty Markdown CPU profiles with function names, source files, line locations, self time, total time, sample counts and call relationships.
- The baseline profile identified `scoreCandidates` as the dominant hotspot at 98.0% self time (548.1 ms in the captured profile).
- The bounded candidate unrolled the sequential hot loop four iterations at a time while preserving the exact output.
- Five same-run Bun measurements produced a baseline median of 511.440 ms and candidate median of 267.829 ms, a 47.63% reduction for this synthetic workload.
- The candidate profile reported `scoreCandidates` at 89.2% self time (260.5 ms in the captured profile).
- Both baseline and candidate profiles passed the agent-inspectable hotspot assertions.

The performance result is workload-specific evidence, not a general Bun benchmark.

## Conclusion

The capability passes because the profiler produced direct, source-specific evidence that supported a bounded diagnosis, a reversible code change, correctness verification and a measured before/after comparison on the same runner.

The reusable pattern is:

```text
execute workload
→ capture machine-readable runtime evidence
→ identify measured hotspot
→ make one bounded change
→ rerun identical correctness gate
→ compare before / after evidence
→ accept or reject
```

## Authority boundary

Validated for use as an evidence-generating diagnostic pattern in bounded development experiments and test workflows. Runtime evidence may inform diagnosis and proposals; it does not authorise consequential changes or runtime migration without the existing review, test and merge gates.

Bun remains an implementation candidate behind this capability, not an architectural authority.

## Stop condition

Met. One before/after profiling cycle demonstrated materially useful machine-readable runtime evidence while preserving deterministic correctness and existing authority boundaries.
