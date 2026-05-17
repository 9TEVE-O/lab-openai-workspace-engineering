# Audit Log Spec

## Purpose

Record material Safe Intake actions so the workflow can be reviewed after the fact.

## Events to log

- document received
- text extracted
- sensitivity classified
- PII/confidential content detected
- redacted copy created
- human review requested
- approval granted
- approval denied
- AI query executed
- export generated
- blocked action attempted

## Minimum event fields

| Field | Purpose |
|---|---|
| event_id | Unique event identifier |
| timestamp | When the event occurred |
| actor | User, system, or service responsible |
| item_id | Document/content item affected |
| action | What happened |
| previous_state | State before event |
| new_state | State after event |
| reason | Why the event occurred |
| evidence_ref | Pointer to source evidence |

## Rule

The audit log should record control decisions, not sensitive raw content.
