#!/usr/bin/env bash
set -u -o pipefail

EVIDENCE_DIR="${EVIDENCE_DIR:-/evidence}"
EXPECTED_R0="6a456830ca33eb5edaa634a9b0febe5d71bea2be"
mkdir -p "${EVIDENCE_DIR}"

STATUS=0

run_check() {
  local name="$1"
  shift
  echo "=== ${name} ==="
  "$@" >"${EVIDENCE_DIR}/${name}.log" 2>&1
  local rc=$?
  cat "${EVIDENCE_DIR}/${name}.log"
  printf '%s\n' "${rc}" >"${EVIDENCE_DIR}/${name}.exitcode"
  if [ "${rc}" -ne 0 ]; then
    STATUS=1
  fi
}

{
  echo "expected_r0=${EXPECTED_R0}"
  echo "actual_r0=$(git rev-parse HEAD)"
  echo "python=$(python --version 2>&1)"
  echo "pip=$(python -m pip --version 2>&1)"
  echo "git=$(git --version 2>&1)"
  echo "gcc=$(gcc --version | head -1)"
  echo "uname=$(uname -a)"
  echo "sqlite=$(python -c 'import sqlite3; print(sqlite3.sqlite_version)')"
  echo "spatialite=$(python - <<'PY'
import sqlite3
con = sqlite3.connect(':memory:')
con.enable_load_extension(True)
con.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
print(con.execute('select spatialite_version()').fetchone()[0])
PY
)"
  echo "setuptools=$(python -c 'import setuptools; print(setuptools.__version__)')"
} | tee "${EVIDENCE_DIR}/environment-summary.txt"

if [ "$(git rev-parse HEAD)" != "${EXPECTED_R0}" ]; then
  echo "R0 identity mismatch" | tee -a "${EVIDENCE_DIR}/environment-summary.txt"
  STATUS=1
fi

python -m pip freeze --all | sort >"${EVIDENCE_DIR}/pip-freeze.txt"
dpkg-query -W -f='${Package}=${Version}\n' | sort >"${EVIDENCE_DIR}/dpkg-packages.txt"
sha256sum /control/requirements.lock /control/lock-manifest.json /control/wheelhouse.sha256 >"${EVIDENCE_DIR}/control-hashes.txt"
cp /control/requirements.lock "${EVIDENCE_DIR}/requirements.lock"
cp /control/lock-manifest.json "${EVIDENCE_DIR}/lock-manifest.json"
cp /control/wheelhouse.sha256 "${EVIDENCE_DIR}/wheelhouse.sha256"

run_check pytest pytest -v
run_check mypy mypy sqlite_utils tests
run_check flake8 flake8
run_check black black . --check
run_check cog bash -lc 'cog --check --diff README.md docs/*.rst'

PYTEST_EXPECTATION='1389 passed, 1 skipped'
if ! grep -Fq "${PYTEST_EXPECTATION}" "${EVIDENCE_DIR}/pytest.log"; then
  echo "Expected pytest summary not reproduced: ${PYTEST_EXPECTATION}" | tee "${EVIDENCE_DIR}/pytest-parity-failure.txt"
  STATUS=1
fi

python - <<'PY' "${EVIDENCE_DIR}" "${STATUS}"
import json
import pathlib
import sys

evidence = pathlib.Path(sys.argv[1])
status = int(sys.argv[2])
checks = {}
for name in ("pytest", "mypy", "flake8", "black", "cog"):
    checks[name] = int((evidence / f"{name}.exitcode").read_text().strip())
summary = {
    "p1_candidate_result": "PASS" if status == 0 else "FAIL",
    "expected_r0": "6a456830ca33eb5edaa634a9b0febe5d71bea2be",
    "checks": checks,
    "pytest_expected_summary": "1389 passed, 1 skipped",
    "pytest_parity": not (evidence / "pytest-parity-failure.txt").exists(),
}
(evidence / "baseline-result.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
PY

exit "${STATUS}"
