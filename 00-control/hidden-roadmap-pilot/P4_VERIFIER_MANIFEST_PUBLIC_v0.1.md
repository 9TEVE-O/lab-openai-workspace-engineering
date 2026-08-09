# Hidden Roadmap P4 Verifier Manifest — Public Surface v0.1

**Status:** CANDIDATE FOR FREEZE  
**Parent:** `HIDDEN_ROADMAP_PILOT_EXECUTION_CONTRACT_v0.1`  
**R0:** `6a456830ca33eb5edaa634a9b0febe5d71bea2be`

This file defines the non-secret verifier mechanics. Feature-specific acceptance suites and future-activated NFI details are retained under roadmap custody and are represented here only by commitment hashes.

## Environment

All commands execute inside the frozen P1 Linux/amd64 environment.

Required environment variables:

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
TZ=UTC
LC_ALL=C.UTF-8
LANG=C.UTF-8
```

Repository source is mounted read-only for final verification. Temporary files and caches use `/tmp`.

## V1 — Upstream regression suite

Command:

```text
python -m pytest -q -p no:cacheprovider
```

Timeout: 120 seconds.  
Blocking: YES.  
Pass: process exit code 0.  
Evidence: stdout, stderr, exit code, elapsed time.

## V2 — Static and documentation checks

Commands:

```text
mypy --cache-dir=/tmp/mypy-cache sqlite_utils tests
flake8
black . --check
cog --check --diff README.md docs/*.rst
```

Timeout: 60 seconds per command.  
Blocking: YES.  
Pass: exit code 0 for every command.

## V3 — Current-feature acceptance suite

At checkpoint `Fi`, custody releases only the verifier bundle authorised for `Fi`.

Command:

```text
python -m pytest -q -p no:cacheprovider --tb=short /benchmark/feature/Fi_acceptance.py
```

Timeout: 120 seconds unless the suite contains a stricter pre-registered threshold.  
Blocking: YES.  
Pass: exit code 0.

The test source is not supplied to the producer. Conditions C and D may receive verifier failure evidence sufficient for repair, but future-feature suites remain inaccessible.

## V4 — Reverse-classical validity

Before producer implementation begins for `Fi`, run the exact `Fi` acceptance suite against the checkpoint-start repository SHA:

```text
python -m pytest -q -p no:cacheprovider --tb=no --no-summary /benchmark/feature/Fi_acceptance.py
```

Expected result: non-zero exit code.

If the entire current-feature suite already passes on the checkpoint-start state, the checkpoint is `INVALID` for benchmark interpretation unless a pre-registered acceptance item is explicitly a regression-only check and at least one feature-defining check still fails.

The reverse-classical result is retained before the producer sees verifier feedback.

## V5 — Scope measurement

Command:

```text
python /benchmark/public/measure_scope.py --repo /workspace/sqlite-utils --base <CHECKPOINT_START_SHA> --head <CANDIDATE_SHA>
```

Output: deterministic JSON containing at least:

- changed files;
- production Python files changed;
- production lines added;
- production lines deleted;
- production churn;
- test files changed;
- documentation files changed.

Blocking: NO by itself.  
Condition-D trigger: more than 8 production Python files or more than 500 production-source churn, as fixed by P3.

## V6 — Persistent non-functional invariant suite

Command:

```text
python -m pytest -q -p no:cacheprovider --tb=short /benchmark/nfi/active_nfi.py
```

Timeout: 120 seconds unless a stricter committed NFI threshold applies.  
Blocking: according to the committed NFI record for each active invariant.

Only the active checkpoint packet is released. Future-activated invariants remain in custody.

## V7 — Resource measurement

Where time/RSS thresholds apply, execute the target command through:

```text
/usr/bin/time -v <COMMAND>
```

Record:

- exit code;
- elapsed wall time;
- maximum resident set size;
- stdout/stderr.

A threshold is interpreted only as specified in the pre-registered active NFI or feature acceptance record.

## V8 — Final verifier order

Every A/B/C/D checkpoint receives the same final verifier sequence:

1. current-feature acceptance suite;
2. active persistent NFI suite;
3. upstream regression suite;
4. mypy;
5. flake8;
6. Black check;
7. Cog consistency check;
8. scope measurement;
9. evidence-hash generation.

Conditions C/D may additionally run the same deterministic feature/NFI verifier earlier as workflow-visible verification. Final acceptance always reruns the common final sequence from the submitted candidate.

## Repository non-modification rule

Verifier tooling must not edit tracked repository files. Python bytecode generation and pytest cache are disabled; mypy cache is redirected to `/tmp`. Any tracked-file modification by the verifier is a verifier defect and invalidates that verifier execution.

## Hidden verifier bundle

Feature-specific suites, the full NFI activation table and their exact hashes are recorded in `P4_P5_COMMITMENT_v0.1.json` on the shareable control surface. Their plaintext remains on the roadmap-custody branch until authorised reveal.
