export function attachAuditMarker(record: string): string {
  return `${record}|audit:v1`;
}
