import { normaliseRecord } from './core';
import { attachAuditMarker } from './audit';

export function buildRecord(input: string): string {
  return attachAuditMarker(normaliseRecord(input));
}

console.log(buildRecord('  Evidence Record  '));
