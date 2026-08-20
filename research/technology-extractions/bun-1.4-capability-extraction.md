# Bun 1.4 Capability Extraction

## Status

**Candidate under validation.**

This record extracts only the parts of Bun 1.4 that add a genuinely useful capability or implementation pattern beyond the current authorised development architecture. Bun itself is not adopted as an architectural dependency by this record.

Source: Bun 1.4 release notes, 20 August 2026.

## Extraction boundary

Do not treat release-note presence, implementation availability, benchmark claims or this record as proof that any Bun capability is production-ready or authorised for use. Each extracted item remains a candidate until a bounded test produces evidence.

## Extracted capabilities

### 1. Machine-Readable Runtime Evidence

**Purpose:** expose measured runtime behaviour in a format that an AI agent can directly inspect and reason over.

**Bun 1.4 implementation examples:**

- `bun --cpu-prof-md ./app.ts`
- Markdown CPU profiling output intended for direct human or LLM consumption
- related machine-readable profiling and diagnostic outputs

**Why this is additive:**

The existing architecture already requires execution evidence, validation, provenance and observability. The missing capability is a deliberate interface that turns measured runtime behaviour into an agent-consumable evidence artefact.

**Architectural pattern:**

```text
execute workload
→ capture structured runtime evidence
→ attach evidence to task
→ agent diagnoses bounded issue
→ proposed change
→ rerun identical workload
→ compare before / after evidence
→ accept or reject
```

**Authority boundary:** runtime evidence informs diagnosis; it does not authorise an agent to make consequential changes without the existing review, test and merge gates.

**Validation test:** run the same bounded TypeScript workload under the current runtime and Bun 1.4, capture profiler evidence, ask an agent to identify one optimisation, apply only if authorised, then rerun the same test and compare correctness plus measured performance.

**Pass condition:** the machine-readable profile materially improves diagnosis or verification without weakening existing test or authority boundaries.

---

### 2. Enforced Runtime Resource Boundary

**Purpose:** translate declared process-resource requirements into enforceable execution constraints.

**Bun 1.4 implementation example:**

On Linux, `Bun.spawn()` and `Bun.spawnSync()` can place a child process into an existing cgroup before execution begins, allowing limits such as memory and process count to apply from the first instruction and to descendants.

**Why this is additive:**

The current architecture can declare CPU, GPU and RAM requirements and can constrain which tools may execute. Declaration is not enforcement. This capability introduces a possible host-runtime mechanism for enforcing resource admission and containment.

**Architectural pattern:**

```text
capability resource declaration
→ runtime admission
→ constrained execution boundary
→ kernel-enforced process limits
→ exit / resource evidence
```

**Authority boundary:** resource enforcement belongs in the runtime adapter or host execution layer. Bun is one candidate implementation, not the architectural authority.

**Validation test:** run a bounded child workload inside a configured Linux cgroup with a deliberately low memory or process limit and verify that the child is contained, the parent remains healthy, and the runtime records the failure correctly.

**Pass condition:** declared limits are enforced predictably and failure preserves parent/runtime integrity.

---

### 3. Browser Execution Adapter

**Purpose:** provide inspectable, bounded headless-browser execution as a registered capability rather than as arbitrary browser automation.

**Bun 1.4 implementation example:** `Bun.WebView`, including browser navigation, DOM interaction, native input, console capture and browser-state handling through WebKit or Chrome/Chromium interfaces.

**Why this is additive:**

The current authorised capability architecture does not yet include browser execution as a registered tool family. A browser adapter could support UI regression checks, rendered-output verification, browser-based integration testing and other bounded workflows.

**Architectural pattern:**

```text
registered browser task
→ bounded browser adapter
→ page interaction / observation
→ console + DOM + screenshot evidence
→ validation result
```

**Authority boundary:** do not replace established browser tooling solely because Bun exposes a browser API. Treat `Bun.WebView`, Playwright and future implementations as interchangeable adapter candidates behind a common browser-execution contract.

**Validation test:** run one deterministic local-page acceptance test through an adapter, capture DOM/console evidence, and compare it against the existing browser-testing path where available.

**Pass condition:** the adapter produces reliable, inspectable evidence with equal or lower complexity than the existing approach.

---

### 4. Machine-Readable Build Evidence

**Purpose:** expose build topology, dependency chains and bundle contribution as inspectable evidence for deterministic and AI-assisted analysis.

**Bun 1.4 implementation examples:** Markdown build/metafile reporting with largest-module analysis, entry-point analysis, dependency chains, module graph and raw searchable build data.

**Why this is additive:**

The current development architecture uses source control, tests, dependency management and documentation, but does not yet define build/dependency topology as a first-class evidence artefact for agents.

**Architectural pattern:**

```text
source change
→ build
→ machine-readable dependency / bundle evidence
→ deterministic or AI-assisted analysis
→ bounded remediation
→ rebuild
→ evidence diff
```

**Potential use:** feed material dependency or module-graph changes into documentation-maintenance, architecture-review or dependency-risk workflows instead of requiring an agent to infer all structural change from source diffs alone.

**Authority boundary:** build evidence can trigger review or proposals; it does not by itself establish that an architecture change is correct or approved.

**Validation test:** produce build metadata for one stable TypeScript project, make a small known dependency change, regenerate the report and verify that the evidence clearly identifies the structural delta.

**Pass condition:** the report makes the material dependency/build change directly discoverable and can be consumed reliably by an agent or deterministic check.

## Explicit non-extractions

The following Bun 1.4 additions are not promoted into separate capability records at this stage:

- `Bun.Image` — potential backend for an already-existing image/media capability family.
- `Bun.markdown` — library/runtime convenience, not a missing architectural capability.
- `Bun.cron()` — possible scheduling backend for an already-existing job/scheduling concept.
- `Bun.Terminal` — potentially useful later for interactive CLI/agent tooling, but premature while constrained execution remains the governing boundary.
- parallel test/run execution — build optimisation, not a new capability.
- Node compatibility improvements — runtime qualification evidence, not architecture.
- lower CPU, memory and startup benchmarks — performance claims requiring local verification.
- package audit/dedupe/prune features — package-management tooling rather than a missing system capability.
- JSON5/JSONL support — parser convenience.
- global virtual store — installation optimisation.
- Windows ARM64 support — platform coverage only.
- Bun's Zig-to-Rust rewrite — implementation detail with no required architectural action.

## Recommended experiment order

Do not migrate an active repository to Bun as the first test.

Run the four candidates independently, in this order:

1. Machine-Readable Runtime Evidence
2. Machine-Readable Build Evidence
3. Enforced Runtime Resource Boundary
4. Browser Execution Adapter

The first two are low-risk, read-mostly evidence experiments. Resource containment and browser execution alter host execution behaviour and therefore require stronger isolation and acceptance criteria.

## Stop condition

This extraction is complete when the four candidate records exist and remain clearly separated from adoption. No architecture migration, runtime replacement or production-readiness claim is authorised by this record.
