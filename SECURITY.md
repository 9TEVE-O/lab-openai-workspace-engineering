# Security Policy

## Scope

This repository contains LAB AI workspace documentation, Safe Intake demo artefacts, reusable skill files, proof packs, and prototype review material.

It is not a production compliance system and must not be treated as one.

## Reporting a security issue

If you find a security issue in this repository, report it privately to the repository owner instead of opening a public issue.

Do not include secrets, credentials, private client data, personal information, screenshots containing sensitive content, or raw exploit payloads in public issues, pull requests, comments, or commits.

## What to report

Report issues such as:

- exposed API keys, tokens, credentials, or `.env` values
- unsafe workflow or automation configuration
- prototype behaviour that leaks raw document content
- demo artefacts that accidentally include real personal, client, artist, or business data
- security checks that silently fail open
- misleading claims that make a prototype look production-ready

## Out of scope

The current Safe Intake prototype is a local demo using synthetic fixture content only. It does not claim to provide production security, legal compliance, real OCR, real access control, or real model safety.

## Handling rules

- Rotate any exposed secret immediately.
- Remove the secret from the current branch.
- Check commit history for historical exposure.
- Record what was exposed, when, and where.
- Do not preserve raw secret values in reports.
- Prefer evidence references over copying sensitive content.

## Security baseline

Before using this repository for client-facing proof or app work, confirm:

- branch protection is enabled
- pull requests are required before merging
- status checks are required before merging
- conversation resolution is required
- force pushes are restricted
- secret scanning or equivalent scanning is enabled
- generated artefacts and local files are ignored
- demo-only limitations remain visible
