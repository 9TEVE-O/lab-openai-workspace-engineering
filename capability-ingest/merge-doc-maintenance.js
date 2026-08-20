#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const allowedTargets = new Set(['README.md', 'REPO-MAP.md', 'NEXT-ACTION.md']);
const protectedStatusTokens = [
  'candidate',
  'validating',
  'admitted',
  'held',
  'superseded',
  'retired',
  'production readiness',
  'production-ready',
  'compliance',
  'commercial validation',
  'external approval',
];

function parseArgs(argv) {
  const result = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const value = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    result[key] = value;
  }
  return result;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function changedFilesFromEvent(event) {
  const body = event.pull_request?.body || '';
  const marker = '<!-- doc-maintenance-changed-files:';
  const start = body.indexOf(marker);
  if (start === -1) return [];
  const end = body.indexOf('-->', start);
  if (end === -1) return [];
  return body
    .slice(start + marker.length, end)
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function determineTargets(changedFiles) {
  const targets = new Set();

  for (const file of changedFiles) {
    if (file === 'README.md' || file.startsWith('docs/') || file.startsWith('01-lab-ai-skill-pack/')) {
      targets.add('README.md');
    }
    if (
      file === 'REPO-MAP.md' ||
      file.startsWith('00-control/') ||
      file.startsWith('00-workspace-map/') ||
      file.startsWith('capability-ingest/')
    ) {
      targets.add('REPO-MAP.md');
    }
    if (
      file === 'NEXT-ACTION.md' ||
      file.startsWith('capability-ingest/') ||
      file.startsWith('00-control/')
    ) {
      targets.add('NEXT-ACTION.md');
    }
  }

  return [...targets].filter((target) => allowedTargets.has(target));
}

function proposalForTarget(target, sourcePr, sourceSha) {
  const current = fs.readFileSync(target, 'utf8');
  const marker = `<!-- merge-doc-maintenance:last-source-pr=${sourcePr};sha=${sourceSha} -->`;
  const existingPattern = /<!-- merge-doc-maintenance:last-source-pr=\d+;sha=[^ ]+ -->/;

  if (current.includes(marker)) return null;

  const proposed = existingPattern.test(current)
    ? current.replace(existingPattern, marker)
    : `${current.replace(/\s+$/, '')}\n\n${marker}\n`;

  return {
    path: target,
    current_sha: '',
    proposed_content: proposed,
    summary: `Refresh durable maintenance pointer after merged PR #${sourcePr}.`,
  };
}

function validateProposal(proposal) {
  if (!proposal || typeof proposal !== 'object') throw new Error('proposal must be an object');
  if (proposal.authority_transition_requested !== false) {
    throw new Error('authority transitions are prohibited');
  }
  if (!Array.isArray(proposal.files)) throw new Error('proposal.files must be an array');

  for (const file of proposal.files) {
    if (!allowedTargets.has(file.path)) throw new Error(`path not allowed: ${file.path}`);
    const before = fs.readFileSync(file.path, 'utf8').toLowerCase();
    const after = String(file.proposed_content || '').toLowerCase();

    for (const token of protectedStatusTokens) {
      const beforeCount = before.split(token).length - 1;
      const afterCount = after.split(token).length - 1;
      if (beforeCount !== afterCount) {
        throw new Error(`protected authority/status token changed in ${file.path}: ${token}`);
      }
    }

    const strippedBefore = before.replace(/<!-- merge-doc-maintenance:last-source-pr=\d+;sha=[^ ]+ -->/g, '').trim();
    const strippedAfter = after.replace(/<!-- merge-doc-maintenance:last-source-pr=\d+;sha=[^ ]+ -->/g, '').trim();
    if (strippedBefore !== strippedAfter) {
      throw new Error(`proposal attempted content mutation outside maintenance marker in ${file.path}`);
    }
  }
}

function applyProposal(proposal) {
  validateProposal(proposal);
  for (const file of proposal.files) {
    fs.writeFileSync(file.path, file.proposed_content);
  }
}

function main() {
  const args = parseArgs(process.argv);
  const eventPath = args.event || process.env.GITHUB_EVENT_PATH;
  if (!eventPath) throw new Error('missing event path');

  const event = readJson(eventPath);
  const pr = event.pull_request || {};
  const sourcePr = pr.number;
  const sourceSha = pr.merge_commit_sha || pr.head?.sha || 'unknown';
  const title = pr.title || '';

  if (!pr.merged || pr.base?.ref !== 'main') {
    console.log('NOOP: event is not a merged PR to main');
    return;
  }

  if (/^docs\(maintenance\):/i.test(title)) {
    console.log('NOOP: maintenance PR recursion guard');
    return;
  }

  const changedFiles = changedFilesFromEvent(event);
  const targets = determineTargets(changedFiles);
  const files = targets.map((target) => proposalForTarget(target, sourcePr, sourceSha)).filter(Boolean);

  const proposal = {
    source_pr: sourcePr,
    reason: files.length ? 'Designated documentation may be stale after merged repository change.' : 'No designated documentation update required.',
    files,
    authority_transition_requested: false,
  };

  validateProposal(proposal);

  if (args['proposal-out']) writeJson(args['proposal-out'], proposal);

  if (!files.length) {
    console.log('NOOP: no maintenance change required');
    return;
  }

  if (args.apply) applyProposal(proposal);

  console.log(`CHANGE_REQUIRED: ${files.map((file) => file.path).join(', ')}`);
}

main();
