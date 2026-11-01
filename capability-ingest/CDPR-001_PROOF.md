# CDPR-001 — Bounded interruption, recovery and draft PR proof

**Date:** 2026-11-01  
**Status:** Execution evidence pending PR checks; not a network reliability certification  
**Host:** Private `9TEVE-O/lab-openai-workspace-engineering`  
**Scope:** Synthetic branch-only proof. No production services, data, credentials, merge or deployment.

## Authority chain

1. **Parent objective:** Keep AI engineering governed and evidence-backed, subject to human release.
2. **Current objective:** Persist checkpoint; recover after interruption; run deterministic tests; create a draft PR; stop.
3. **Persisted authority:** `capability-ingest/CDPR-001_STATE.json`, first saved as revision 1 on branch `proof/cdpr-001-resume-pr-20261101`.
4. **Initial checkpoint commit:** `27b96ca833b9bc1dbe3543b84db1e2eecbfa0cf6`.
5. **Actual remote readback:** A separate GitHub connector invocation fetched revision 1, status `PAUSED_FOR_RECOVERY`, blob `bdb4e3213e53a998dbbcd2c540cbb720be59560f`, and `HUMAN_ONLY` release authority.
6. **Allowed:** Synthetic test, branch write, CI checks, draft PR.
7. **Denied:** Merge, deployment, production changes, secrets, writes to main, scope expansion.

The checkpoint file is retained as the immutable starting fixture for CI. A later continuation receipt must cite this original commit and preserve its authority.

## Synthetic failure test

Run:

```sh
python3 capability-ingest/cdpr-001-recovery-test.py capability-ingest/CDPR-001_STATE.json
```

The harness copies the source checkpoint into a temporary directory, starts a worker subprocess, writes revision 2 using a temporary file, flush, fsync and rename, then terminates the worker abruptly using `os._exit(77)`. A **new subprocess** reads that saved file, checks the pinned authority digest and required deny rules, and writes revision 3 with `WAITING_HUMAN_REVIEW`.

Additional checks reject stale revision writes, reject an altered human-release rule, enforce no merge/deploy operations and verify idempotent recovery. All actual working files are synthetic and local to the temporary directory.

## Evidence and limits

- Local authoring-environment execution: **PASS** on 2026-11-01 for the nine checks printed by the harness.
- GitHub checkpoint write and fresh connector readback: **observed**.
- Ecosystem task creation: **NOT_AVAILABLE**; do not claim that the Ecosystem task service stored this continuation.
- Real ChatGPT client-to-MCP network disconnection and session-token expiry: **not tested**.
- GitHub API reconnection under an actual dropped socket: **not tested**.
- Crash consistency under power loss or concurrent competing writers: **not tested**.
- Production authority enforcement and protected-branch settings: **not established**.
- GitHub Actions PR check: **pending** until the PR produces a run.
- Real merge/deploy prohibition is effected by deliberately stopping before either action, not by claiming this Python harness controls GitHub permissions.

## Human release gate

The resulting pull request must be **draft** and remain **unmerged**. A successful synthetic CI run proves only the local crash/restart behaviour and authority checks within its test boundaries. Human review is required for any merge or subsequent host-specific implementation.
