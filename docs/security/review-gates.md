# Security Review Gates

## Purpose

This document defines the review gates required before the repository moves from documentation and local demos into client-facing, hosted, or production-style use.

## Manual accessibility / visual QA

Required before using the demo externally.

Check:

- keyboard navigation
- visible focus states
- readable text at desktop and mobile widths
- colour contrast
- clear error and blocked-action messages
- readable audit log
- no visual implication that the demo is production-ready

## Privacy review

Required before any real or client-like document handling.

Check:

- only synthetic data is used in fixtures
- raw sensitive data is not copied into proof packs
- audit records use references and categories where possible
- retention expectations are documented
- no provider/model receives raw unreviewed content

## Security review

Required before hosting or adding integrations.

Check:

- no secrets in repo
- secret scanning enabled
- branch protection enabled
- dependency scanning enabled if dependencies exist
- no unsafe workflow permissions
- no hidden external calls
- prototype limitations are visible

## Deployment review

Required before public hosting.

Check:

- Content Security Policy is defined
- static-site headers are configured
- inline scripts are removed or explicitly justified
- no real data is included
- no unnecessary external assets are loaded
- hosting logs do not capture sensitive content

## Demo-only disclaimer review

Required before client-facing use.

Confirm the demo clearly states:

- synthetic-only fixture
- not production-ready
- not legal compliance proof
- not real OCR/model/access-control testing
- control-path demonstration only

## Repository settings review

Configure in GitHub settings:

- require pull requests before merging
- require status checks before merging
- require conversation resolution
- restrict force pushes
- require signed commits if practical
- limit admin bypass where possible
- enable secret scanning and push protection if available
- enable Dependabot alerts

## Decision rule

If a review cannot be completed, mark the status as:

```text
incomplete — do not treat as ready
```
