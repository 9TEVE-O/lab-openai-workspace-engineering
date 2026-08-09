# Hidden Roadmap P1 Baseline Result v0.1

**Status:** P1 CLOSED — PASS  
**Repository:** `simonw/sqlite-utils`  
**R0:** `6a456830ca33eb5edaa634a9b0febe5d71bea2be`  
**Successful workflow run:** `31296553201`  
**Successful benchmark-control SHA:** `b0b852ea284c56b708be464c5b94d2c1cabb645f`  
**Evidence artifact ID:** `9033129872`  
**Evidence artifact digest:** `sha256:79a5a4e62e92d92ef43cedd5e0e454d871c9ad7df5c992fcf69343c72573ac90`

## Decision

P1 is closed as **PASS**.

The exact R0 commit was checked out detached and clean, a benchmark-owned Python 3.12.13 environment was materialised with one exact wheel per Python dependency and SHA-256 hash enforcement, an immutable container was built, and the baseline verifier was executed once successfully.

The upstream R0 repository was not modified.

## Frozen environment identity

- Base image: `python:3.12.13-slim-trixie@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de`
- Built image ID: `sha256:5ecc566081ea99ea24b781fa1209b0ce86497dbf0cc9c061ca1794ab35b1283e`
- Debian snapshot: `20260809T000000Z`
- Architecture: Linux x86_64 / amd64
- Python: `3.12.13`
- pip: `26.1.2`
- Setuptools / build backend implementation: `83.0.0`
- Git: `2.47.3`
- GCC: `14.2.0` (`gcc-14=14.2.0-19`)
- SQLite runtime: `3.46.1`
- Debian SQLite package: `libsqlite3-0=3.46.1-7+deb13u1`
- SQLite development package: `libsqlite3-dev=3.46.1-7+deb13u1`
- SpatiaLite runtime: `5.1.0`
- Debian SpatiaLite package: `libsqlite3-mod-spatialite=5.1.0-3+b2`

## Python dependency lock

The frozen lock contains 36 exact wheel artefacts. Every line carries a SHA-256 hash and installation is performed with `pip --require-hashes` from the generated wheelhouse.

Control-file hashes from the successful run:

- `requirements.exact.txt`: `dac9e64c66d3c97b8ee529ca84d6b16568a381323a9ed32d9934d53c5facf877`
- `requirements.lock`: `79a5fd7ed89df564794284dfc382cb3d099d647ba452d2c236ddb2ff9054ddd8`
- `lock-manifest.json`: `1110945a85c51bb03dd3b7f472aadd0fcfd40f44be456544f733febae63b82e7`
- `wheelhouse.sha256`: `69cbdedc48389a7baf5880223af62a15bd8e6195650dcf257c5f02e282c3a77b`

Notable bootstrap/build hashes:

- `pip==26.1.2`: `sha256:382ff9f685ee3bc25864f820aa50505825f10f5458ffff07e30a6d96e5715cab`
- `setuptools==83.0.0`: `sha256:29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3`

The complete lock is retained beside this result as `requirements.lock`; wheel filenames and SHA-256 values are retained as `wheelhouse.sha256`.

## Baseline verifier result

- R0 identity: PASS — actual SHA exactly matched expected R0
- R0 clean status: PASS — no working-tree changes before execution
- `pytest -v`: PASS — `1389 passed, 1 skipped in 15.07s`
- Historical pytest parity: PASS — exact count `1389 passed, 1 skipped`
- `mypy sqlite_utils tests`: PASS — no issues in 61 source files
- `flake8`: PASS
- `black . --check`: PASS — 62 files unchanged
- `cog --check --diff README.md docs/*.rst`: PASS
- Container exit code: `0`

`ty` remains non-blocking for this Python 3.12 baseline because the upstream R0 workflow does not execute it in that matrix condition.

## Failed first attempt

Workflow run `31296515778` failed before container construction because the benchmark lock generator counted vendored nested `.dist-info/METADATA` files inside the Setuptools wheel as top-level wheel metadata.

That failure was classified as benchmark-control infrastructure, not R0 evidence. The smallest repair restricted metadata detection to the wheel's top-level `.dist-info/METADATA`; no repository, dependency version, verifier, or acceptance criterion changed. The succeeding run then passed end-to-end.

## Gate consequence

**P1 — Repository and baseline reproducibility: CLOSED — PASS.**

This closes only the repository/environment reproduction gate. It does not itself define or approve F01–F05, a roadmap implementation, trajectory execution, or thesis conclusions.

F01–F05 design is now unblocked and must use this frozen R0 and environment without retroactive changes to P1.
