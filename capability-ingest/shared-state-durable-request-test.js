const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const initial = {
  task_id: 'STATE_TEST_001',
  task: 'Verify restart-safe shared workflow state',
  status: 'requested',
  requested_operation: 'reconstruct-and-advance-after-authorised-write',
  authority: {
    read: ['human', 'agent'],
    write: ['human-authorised-agent'],
    forbidden: ['unauthorised-agent'],
  },
  revision: 1,
};

function canonicalView(state) {
  return {
    task: state.task,
    status: state.status,
    requested_operation: state.requested_operation,
    read_authority: state.authority.read.join(', '),
    write_authority: state.authority.write.join(', '),
    forbidden_writer: state.authority.forbidden.join(', '),
    revision: state.revision,
  };
}

function load(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeAs(file, actor, patch) {
  const current = load(file);
  if (!current.authority.write.includes(actor)) {
    return { accepted: false, state: current };
  }
  const next = { ...current, ...patch };
  fs.writeFileSync(file, JSON.stringify(next, null, 2));
  return { accepted: true, state: next };
}

const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'shared-state-test-'));
const stateFile = path.join(dir, 'state.json');
fs.writeFileSync(stateFile, JSON.stringify(initial, null, 2));

// T1/T2: durable seed and human reconstruction from file only.
const humanBefore = canonicalView(load(stateFile));
assert.deepEqual(humanBefore, canonicalView(initial));

// T3: fresh agent reconstruction is a new read from durable state only.
const agentBefore = canonicalView(load(stateFile));
assert.deepEqual(agentBefore, humanBefore);

// T4: unauthorised write is rejected and file remains unchanged.
const rejected = writeAs(stateFile, 'unauthorised-agent', { status: 'completed', revision: 2 });
assert.equal(rejected.accepted, false);
assert.deepEqual(load(stateFile), initial);

// T5: authorised write succeeds.
const accepted = writeAs(stateFile, 'human-authorised-agent', { status: 'in_progress', revision: 2 });
assert.equal(accepted.accepted, true);
assert.equal(load(stateFile).status, 'in_progress');
assert.equal(load(stateFile).revision, 2);

// T6: independent fresh reads reconstruct the same post-write state.
const humanAfter = canonicalView(load(stateFile));
const agentAfter = canonicalView(load(stateFile));
assert.deepEqual(agentAfter, humanAfter);
assert.equal(humanAfter.status, 'in_progress');
assert.equal(humanAfter.revision, 2);

console.log(JSON.stringify({
  test: 'SHARED_STATE_DURABLE_REQUEST_TEST_001',
  result: 'PASS',
  human_before: humanBefore,
  agent_before: agentBefore,
  unauthorised_write: { accepted: rejected.accepted },
  authorised_write: { accepted: accepted.accepted },
  human_after: humanAfter,
  agent_after: agentAfter,
}, null, 2));
