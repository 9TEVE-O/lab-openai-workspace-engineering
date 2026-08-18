# Runtime Evidence Before Repair

Use this checklist when an AI-assisted build reports or appears to contain a defect.

## Rule

Do not repair from description alone when runtime evidence can be obtained.

The preferred sequence is:

```text
reported defect
→ inspect runtime evidence
→ reproduce
→ identify the actual state transition or failure condition
→ make the smallest bounded repair
→ run regression checks
```

Avoid:

```text
reported defect
→ infer likely cause
→ rewrite broadly
→ assume the result is fixed
```

## Checklist

- [ ] Record the observed behaviour without upgrading assumptions into facts.
- [ ] Capture the relevant runtime state, trace, logs, UI state or reproducible steps available for the defect.
- [ ] Reproduce the failure before modifying code where reasonably possible.
- [ ] Identify the smallest state transition, condition or component that explains the observed failure.
- [ ] Preserve intentional behaviour outside the requested repair as acceptance criteria.
- [ ] Make only the bounded change required to address the evidenced defect.
- [ ] Run the direct regression check for the defect.
- [ ] Run checks for adjacent behaviour likely to be affected by the change.
- [ ] Record what was verified and what remains unverified.
- [ ] Do not promote a local repair into a production-readiness claim.

## Stop condition

Stop when the evidenced defect is fixed, the defined regression checks pass, and no new material failure has been exposed. Do not continue refactoring merely because additional changes appear attractive.
