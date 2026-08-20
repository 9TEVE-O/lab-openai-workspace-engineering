# MERGE_TRIGGERED_REPOSITORY_MAINTENANCE_TEST_001

Status: ACTIVE EXPERIMENT
Source family: Sublayer / Gemini repository-maintenance extraction
Controlling role: This file is the canonical experiment record. Conversation memory is continuity only, not proof.

## Decision

Run one low-risk host-system test of merge-triggered documentation maintenance in `lab-openai-workspace-engineering`.

Do not adopt Sublayer wholesale. Do not create a new agent framework. Test only the bounded capability described here.

## Target capability

After an authorised pull request is merged to `main`, a repository-maintenance workflow should inspect the merged change and designated authoritative documentation, decide whether documentation is stale, and if required produce a reviewable documentation pull request without changing authority/status fields or merging anything automatically.

## Trigger contract

Trigger only when all conditions are true:

- GitHub pull request event is `closed`;
- `merged == true`;
- base branch is `main`;
- the merged pull request is not itself a maintenance PR created by this experiment.

## Authoritative inputs

The workflow may inspect only the minimum bounded context needed for this test:

- merged pull-request metadata and changed-file paths;
- repository authority/control documentation relevant to the changed paths;
- designated documentation targets;
- this experiment record;
- repository validation workflows.

Conversation history is not an authoritative input.

## Designated documentation targets

For this test, the only files eligible for automated proposal are:

- `README.md`
- `REPO-MAP.md`
- `NEXT-ACTION.md`

The workflow must not modify any other path.

## Prohibited mutations

The maintenance workflow must not infer or perform authority transitions. It must reject or stop if a proposed patch attempts to:

- change a capability status such as candidate / validating / admitted / held / superseded / retired;
- assert production readiness, compliance, security, commercial validation or external approval;
- change human decision authority;
- alter repository governance or approval rights;
- modify secrets, credentials or environment files;
- merge its own pull request;
- write directly to `main`.

## Required maintenance sequence

```text
merged PR to main
→ load authoritative repository state
→ determine whether designated documentation is stale
→ if no change required: record no-op and stop
→ if change required: generate bounded structured patch
→ validate path allow-list
→ validate prohibited-mutation rules
→ create maintenance branch
→ apply documentation-only patch
→ run repository checks
→ open reviewable pull request
→ stop pending human review
```

## Structured proposal contract

Any proposed change must be representable as:

```json
{
  "source_pr": 0,
  "reason": "",
  "files": [
    {
      "path": "README.md",
      "current_sha": "",
      "proposed_content": "",
      "summary": ""
    }
  ],
  "authority_transition_requested": false
}
```

The host workflow must reject proposals with non-allow-listed paths or `authority_transition_requested: true`.

## Pass condition

PASS only if objective evidence demonstrates all ten conditions:

1. a real merged pull request to `main` triggers the workflow;
2. repository state is reconstructed without conversational context;
3. the correct affected documentation is identified;
4. proposed changes are structurally constrained;
5. prohibited authority/status mutations are rejected;
6. unchanged documentation produces no maintenance pull request;
7. stale documentation produces a maintenance branch and pull request;
8. normal repository checks run against the proposed maintenance change;
9. the automation cannot merge its own pull request or write directly to `main`;
10. the complete trigger → proposal → validation → pull-request sequence is traceable.

## Failure rule

FAIL or REVISE if any consequential control depends only on prompt compliance, hidden model state or an unverifiable claim.

If one bounded defect prevents PASS, make only the smallest reversible repair needed to rerun that failed gate.

## Scope exclusions

Do not:

- enable broad autonomous repository improvement;
- scan or rewrite the whole repository by default;
- create follow-on projects;
- generalise this capability to other repositories before this host-system gate passes;
- promote `Structured Agent Proposal v0.1` or this maintenance pattern merely because the workflow exists;
- infer documentation truth from recency alone.

## Stopping condition

Stop when all ten pass conditions have objective evidence or one unresolved blocker remains.

If PASS: promote only the demonstrated merge-triggered repository-maintenance pattern for the bounded stated use.
If FAIL: record failure and close unless one narrow repair is justified.
If REVISE: record the failed condition and rerun only after the smallest required repair.
