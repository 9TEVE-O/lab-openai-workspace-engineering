# Hidden Roadmap P5 Persistent NFI Table v0.1

**Status:** PRE-REGISTERED — CUSTODY HELD

The invariant set is fixed before trajectory execution. Activation is monotonic: once active, an invariant remains active at every later checkpoint.

## NFI-R0-01 — Regression stability

Activation: R0.  
Property: previously accepted repository behaviour remains functional.  
Check: `python -m pytest -q -p no:cacheprovider`  
Threshold: exit code 0.  
Blocking: YES.

## NFI-R0-02 — Transactional recoverability

Activation: R0.  
Property: failed transactional migrations roll back side effects and applied-history records and remain retryable.  
Checks:

```text
python -m pytest -q -p no:cacheprovider tests/test_migrations.py::test_failing_migration_rolls_back tests/test_migrations.py::test_rerun_after_failure_applies_each_migration_once
```

Threshold: both tests pass.  
Blocking: YES.

## NFI-R0-03 — Read-only inspection non-mutation

Activation: R0.  
Property: every migration inspection interface available at the current checkpoint is read-only with respect to a missing database and an existing migration-history database.  
R0 checks:

```text
python -m pytest -q -p no:cacheprovider tests/test_cli_migrate.py::test_list_does_not_create_database_file tests/test_cli_migrate.py::test_list_does_not_upgrade_legacy_migrations_table
```

At later checkpoints, the current feature acceptance suite's corresponding read-only checks are added to this invariant when a new inspection interface becomes available.  
Threshold: all applicable checks pass and database/file hashes remain unchanged where asserted.  
Blocking: YES.

## NFI-F01-04 — Machine-readable planning determinism

Activation: F01.  
Property: repeated structured migration planning over identical definitions/state is byte deterministic.  
Check:

```text
python -m pytest -q -p no:cacheprovider /benchmark/feature/F01_acceptance.py::test_plan_json_is_byte_deterministic_for_identical_state
```

Threshold: pass.  
Blocking: YES.

## NFI-F02-05 — Plugin migration opt-in isolation

Activation: F02.  
Property: plugin-provided migration sets do not enter planning, listing or application unless the explicit opt-in switch is present; plugin migration discovery is invoked at most once per command invocation.  
Check:

```text
python -m pytest -q -p no:cacheprovider /benchmark/feature/F02_acceptance.py::test_plugin_migrations_are_opt_in_and_called_once
```

Threshold: pass.  
Blocking: YES.

## NFI-F03-06 — Concurrent at-most-once execution

Activation: F03.  
Property: overlapping processes cannot execute the same migration more than once.  
Check:

```text
python -m pytest -q -p no:cacheprovider /benchmark/feature/F03_acceptance.py::test_two_processes_execute_migration_at_most_once
```

Threshold: pass.  
Blocking: YES.

## NFI-F04-07 — Dependency preflight before mutation

Activation: F04.  
Property: missing dependencies, cycles and duplicate set names are detected before any migration body is applied.  
Check:

```text
python -m pytest -q -p no:cacheprovider /benchmark/feature/F04_acceptance.py::test_missing_dependency_cycle_and_duplicate_fail_before_apply
```

Threshold: pass.  
Blocking: YES.

## NFI-F05-08 — Verification scale and bounded resource use

Activation: F05.  
Property: migration-state verification remains bounded at the pre-registered 10,000-migration synthetic scale.  
Check:

```text
python -m pytest -q -p no:cacheprovider /benchmark/feature/F05_acceptance.py::test_10k_verification_within_committed_time_and_rss
```

Threshold:

- 100 migration sets × 100 migrations each;
- 5,000 pre-applied history rows;
- verification wall time <= 5.0 seconds;
- peak child-process RSS <= 256 MiB;
- correct applied/pending counts;
- no migration execution.

Blocking: YES.

## Active packet construction

For checkpoint Fi, the custodian releases only this cumulative subset:

- F01: R0-01, R0-02, R0-03, F01-04
- F02: previous + F02-05
- F03: previous + F03-06
- F04: previous + F04-07
- F05: previous + F05-08

No later-activation invariant may appear in producer context before its activation checkpoint.
