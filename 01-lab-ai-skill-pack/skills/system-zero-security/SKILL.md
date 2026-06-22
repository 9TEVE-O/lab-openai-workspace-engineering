# System Zero — Security Review Skill

## Purpose

Apply T0-tier (heavyweight model) security review to any task that touches authentication,
authorisation, RBAC, multi-tenant boundaries, secrets management, or agentic permission scopes.

This skill is the highest-stakes entry point in System Zero's model-routing hierarchy.
It enforces that security work is never silently downgraded to a lighter model tier, even
under token quota pressure.

## Tier contract

- **Model tier:** T0 — Claude Opus 4.8 or GPT-5.5 only
- **Token budget:** 8 192 tokens in / 4 096 tokens out per task
- **Cost weight:** 1.0× (full cost, no discount)
- **Cascade failure policy:** if T0 quota is exhausted, escalate to human review — do not
  silently reroute to T1 or T2
- **Retry budget:** maximum 2 retries; each retry emits a `retry_cost` span

## Trigger phrases / when to use

Use this skill when any task involves:

- authentication flows (OAuth, API key gates, session tokens, JWTs)
- authorisation rules (RBAC, ABAC, policy enforcement, permission boundaries)
- multi-tenant data isolation or cross-tenant boundary checks
- secrets management (Vault, KMS, environment variable handling, credential injection)
- MCP tool annotations with side-effect labels or permission scopes
- agentic supervisor decisions that grant, revoke, or escalate permissions
- security annotations on any tool definition that touches external systems
- any task flagged by the `tool-hint-security-review` skill as requiring deeper analysis
- CI gate failures related to security or credential exposure
- Safe Intake approval gates that interact with protected data paths

## Inputs required

Ask for or infer:

- the specific resource or permission being reviewed
- the current access control model (RBAC roles, policy files, annotations)
- the threat model or adversary assumption
- whether multi-tenant boundaries are involved
- whether the change touches secrets, tokens, or credentials
- whether an approval gate exists before the permission change takes effect
- whether an audit log records the decision

If any of these are absent, mark the review as **incomplete** and block downstream build work.

## Workflow

1. Classify the security domain: auth / authz / secrets / boundary / annotation / audit.
2. Identify the resource being protected and the principal requesting access.
3. Check whether the access control model explicitly denies by default.
4. Verify that least-privilege is applied — no over-provisioned roles or wildcards.
5. Check for multi-tenant isolation: confirm no cross-tenant data path exists.
6. Review secrets handling: confirm no secrets in logs, env vars in plaintext, or
   in-process exposure.
7. Check approval gates: verify that state-changing operations require explicit human sign-off.
8. Check audit trail: confirm that decisions and changes are logged with actor, timestamp,
   resource, and outcome.
9. Classify findings: **blocker** / **warning** / **observation**.
10. Emit a structured span: `{task_id, model_used, tier, tokens_in, tokens_out, domain,
    outcome, confidence}`.
11. If `confidence < 0.7`, flag for human review before any change is merged.

## Output contract

Return:

```text
Security domain:
Resource protected:
Principal:
Least-privilege check:
Multi-tenant isolation check:
Secrets handling check:
Approval gate check:
Audit trail check:
Blockers:
Warnings:
Observations:
Confidence score (0.0–1.0):
Recommended fixes (ordered by severity):
Span emitted: yes / no
Human review required: yes / no
```

## Safety rules

- Never mark a task as low-risk based on its name alone — inspect the implementation.
- Never accept a wildcard permission (`*`) without an explicit documented justification.
- Never treat a missing approval gate as acceptable for state-changing operations.
- Never allow secrets in log output, even in debug mode.
- Never silently downgrade to a lighter model tier when T0 quota is exhausted.
- Treat an incomplete input set as a blocker, not a warning.

## Evidence Layer integration

Every task processed by this skill emits an OpenTelemetry span into the OTLP collector:

```json
{
  "task_id": "<uuid>",
  "skill": "system-zero-security",
  "model_used": "claude_opus_4_8 | gpt_5_5",
  "tier": 0,
  "tokens_in": 0,
  "tokens_out": 0,
  "domain": "auth | authz | secrets | boundary | annotation | audit",
  "outcome": "PASS | FAIL | FLAGGED | ESCALATED",
  "confidence": 0.0,
  "retry_count": 0,
  "human_review_required": false
}
```

Spans with `outcome = FAIL` or `confidence < 0.7` are written to the Daily Review Log
and surfaced in the EOD digest.

## Skill feedback loop

If this skill produces an incorrect or incomplete result:

1. Log an incident entry in the Daily Review Log (Notion).
2. Propose a targeted patch to this SKILL.md in a GitHub PR.
3. After human approval, bump `registry.json` version for this skill.
4. The next day's tasks pick up the patched skill automatically.

## Failure modes

- Approving a permission change because the task name sounds safe.
- Missing a cross-tenant data path hidden behind an abstraction layer.
- Accepting a missing audit log because the flow "looks simple."
- Treating a retry as a resolved issue without logging the root cause.
- Silently using T1 when T0 quota is exhausted — this is a **critical violation**.

## Relationship to existing skills

| Skill | Relationship |
|---|---|
| `tool-hint-security-review` | Upstream — initial annotation check; escalates here when deeper review is needed |
| `credential-gate` | Sibling — handles credential provisioning; this skill reviews the security of that provisioning |
| `safe-intake` | Downstream consumer — Safe Intake approval gates must pass this review before live use |
| `agent-eval` | Companion — security evals must cover forbidden tool-call cases for every auth boundary |
| `router` | Dispatcher — routes security-domain tasks here; this skill does not self-route |

## Example request

```text
Review the RBAC configuration for the Safe Intake approval gate.
The reviewer role can call `approve_for_ai` — confirm this is correctly scoped.
```

## Example output

```text
Security domain: authorisation — RBAC role boundary
Resource protected: approve_for_ai tool
Principal: reviewer role
Least-privilege check: PASS — role is scoped to document-approval only; no wildcard
Multi-tenant isolation check: PASS — role is tenant-scoped via middleware claim
Secrets handling check: N/A — no credentials in this flow
Approval gate check: PASS — approve_for_ai requires an explicit reviewer decision
Audit trail check: WARNING — audit log records decision but not the reviewer's user ID
Blockers: none
Warnings: audit log missing actor user ID — add before production use
Observations: consider adding a time-bounded token to prevent replay
Confidence score: 0.88
Recommended fixes: 1. Add actor user ID to audit log entry  2. Add token expiry to approval
Span emitted: yes
Human review required: no
```
