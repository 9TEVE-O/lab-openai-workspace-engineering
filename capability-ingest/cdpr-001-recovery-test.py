#!/usr/bin/env python3
"""Synthetic crash/recovery test. No network, credentials, merge or deploy capability."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

DENIED = frozenset({'merge', 'deploy', 'production changes', 'secrets', 'unreviewed writes to main', 'scope expansion'})


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def authority_digest(state):
    return hashlib.sha256(canonical(state['authority'])).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def validate(state, expected_authority):
    assert state['schema'] == 'lab.cdpr-proof-state/1'
    assert state['proof_id'] == 'CDPR-001'
    assert state['authority']['release_decision'] == 'HUMAN_ONLY'
    assert DENIED.issubset(set(state['authority']['denied']))
    assert authority_digest(state) == expected_authority, 'authority changed after checkpoint'
    assert state['revision'] in (1, 2, 3)


def atomic_write(path, state, expected_revision):
    path = Path(path)
    if load(path)['revision'] != expected_revision:
        raise ValueError('stale revision: compare-and-swap rejected')
    temporary = path.with_name(path.name + '.tmp')
    try:
        with temporary.open('w', encoding='utf-8') as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def deny_action(state, action):
    if action in state['authority']['denied'] or action in {'merge', 'deploy'}:
        raise PermissionError(f'{action} forbidden by saved authority')
    raise ValueError('This harness does not execute external actions')


def worker(path, digest):
    state = load(path)
    validate(state, digest)
    assert state['revision'] == 1 and state['status'] == 'PAUSED_FOR_RECOVERY'
    state.update(revision=2, status='WORKER_INTERRUPTED', current_position='CRASH_AFTER_DURABLE_CHECKPOINT', current_gate='FRESH_PROCESS_RECOVERY', next_action='Resume in a new process from this checkpoint, then stop at draft-PR review')
    state['completed'].append('Synthetic worker checkpoint written before abrupt exit')
    atomic_write(path, state, 1)
    os._exit(77)  # Abrupt process death, not graceful process completion.


def resume(path, digest):
    state = load(path)
    validate(state, digest)
    if state['revision'] == 3 and state['status'] == 'WAITING_HUMAN_REVIEW':
        return  # Retry is idempotent.
    assert state['revision'] == 2 and state['status'] == 'WORKER_INTERRUPTED'
    for action in ('merge', 'deploy'):
        try:
            deny_action(state, action)
        except PermissionError:
            pass
        else:
            raise AssertionError(f'{action} unexpectedly allowed')
    state.update(revision=3, status='WAITING_HUMAN_REVIEW', current_position='RECONSTRUCTED_FROM_SAVED_BYTES', current_gate='DRAFT_PR_REVIEW', next_action='Human reviews the draft PR; no merge or deployment authorised')
    state['completed'].append('Fresh process validated preserved authority and resumed safely')
    atomic_write(path, state, 2)


def main():
    args = sys.argv[1:]
    if args and args[0] in ('--worker', '--resume'):
        _, path, digest = args
        (worker if args[0] == '--worker' else resume)(path, digest)
        return
    if len(args) != 1:
        raise SystemExit('usage: python3 cdpr-001-recovery-test.py path/to/CDPR-001_STATE.json')
    source = Path(args[0])
    initial = load(source)
    digest = authority_digest(initial)
    validate(initial, digest)
    assert initial['revision'] == 1 and initial['status'] == 'PAUSED_FOR_RECOVERY'
    with tempfile.TemporaryDirectory(prefix='cdpr-001-') as directory:
        path = Path(directory) / 'state.json'
        path.write_bytes(source.read_bytes())
        runner = str(Path(__file__).resolve())
        cmd = [sys.executable, runner]
        crashed = subprocess.run(cmd + ['--worker', str(path), digest], capture_output=True, text=True)
        assert crashed.returncode == 77, f'worker did not die as intended: {crashed.stderr}'
        stopped = load(path)
        validate(stopped, digest)
        assert stopped['revision'] == 2 and stopped['status'] == 'WORKER_INTERRUPTED'
        resumed = subprocess.run(cmd + ['--resume', str(path), digest], capture_output=True, text=True)
        assert resumed.returncode == 0, resumed.stderr
        recovered = load(path)
        validate(recovered, digest)
        assert recovered['revision'] == 3 and recovered['status'] == 'WAITING_HUMAN_REVIEW'
        assert recovered['authority'] == initial['authority']
        snapshot = path.read_bytes()
        replay = subprocess.run(cmd + ['--resume', str(path), digest], capture_output=True, text=True)
        assert replay.returncode == 0 and path.read_bytes() == snapshot, 'retry was not idempotent'
        try:
            atomic_write(path, recovered, expected_revision=2)
        except ValueError as error:
            assert 'stale revision' in str(error)
        else:
            raise AssertionError('stale writer was accepted')
        assert path.read_bytes() == snapshot
        altered = dict(recovered)
        altered['authority'] = {**recovered['authority'], 'release_decision': 'AGENT_ONLY'}
        tamper_path = Path(directory) / 'tampered.json'
        tamper_path.write_bytes(canonical(altered))
        tampered = subprocess.run(cmd + ['--resume', str(tamper_path), digest], capture_output=True, text=True)
        assert tampered.returncode != 0 and 'AssertionError' in tampered.stderr, 'authority tamper accepted'
        for action in ('merge', 'deploy'):
            try:
                deny_action(recovered, action)
            except PermissionError:
                pass
            else:
                raise AssertionError(f'{action} allowed')
        print(json.dumps({
            'proof_id': 'CDPR-001',
            'result': 'PASS',
            'tests': ['actual worker process killed at checkpoint (exit 77)', 'new subprocess reads checkpoint and resumes', 'authority unchanged', 'release remains human-only', 'replay idempotent', 'stale revision rejected with unchanged bytes', 'authority tamper rejected', 'merge denied', 'deploy denied'],
            'initial_revision': initial['revision'],
            'interrupted_revision': stopped['revision'],
            'recovered_revision': recovered['revision'],
            'authority_sha256': digest,
            'network_disconnect_tested': False,
            'github_reconnection_tested': False,
            'deployment_performed': False,
        }, indent=2))


if __name__ == '__main__':
    main()
