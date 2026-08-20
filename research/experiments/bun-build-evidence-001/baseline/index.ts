import { normaliseRecord } from './core';

export function buildRecord(input: string): string {
  return normaliseRecord(input);
}

console.log(buildRecord('  Evidence Record  '));
