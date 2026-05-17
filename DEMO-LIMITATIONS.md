# Demo Limitations

## Purpose

This file keeps the repository honest about what the Safe Intake demo proves and what it does not prove.

## Current demo status

The Safe Intake clickable prototype is a local demonstration of a controlled document-intake workflow.

It uses synthetic fixture content only.

## What the demo proves

The demo can show:

- staged document intake
- sensitivity classification as a visible workflow stage
- category-labelled redaction
- a human approval gate
- blocked raw-content paths
- audit-event recording
- visible evidence of workflow decisions

## What the demo does not prove

The demo does not prove:

- legal compliance
- production security
- privacy-law compliance
- real OCR accuracy
- real model safety
- access-control enforcement
- secure hosting
- secure storage
- real-world PII detection accuracy
- suitability for real client documents

## Data rule

Do not use real personal, client, artist, business, legal, financial, health, or confidential data in the current demo.

Only use synthetic fixtures that are clearly marked as synthetic.

## Required reviews before client-facing use

Before using the demo as client-facing proof, complete:

- manual accessibility and visual QA
- privacy review
- security review
- deployment review if hosted
- explicit demo-only disclaimer review

## Required reviews before production use

Before production use, this would require a separate production architecture and security review covering:

- authentication and authorisation
- secure storage
- encryption
- logging and retention
- secret management
- threat modelling
- dependency scanning
- model/provider data handling
- incident response
- privacy assessment
- legal review
