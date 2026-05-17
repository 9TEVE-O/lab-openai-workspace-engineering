# Synthetic Artist Onboarding Form Fixture

## Fixture status

This is a synthetic fixture for the Safe Intake demo.

It contains no real personal data, no real client data, no real artist data, and no real business data.

Use this fixture only for demo, testing, documentation, and prototype walkthroughs.

## Source document preview

```text
ARTIST ONBOARDING FORM — SYNTHETIC DEMO ONLY

Artist / Project Name:
River Echo Demo Project

Primary Contact:
Avery Placeholder

Representative / Manager:
Morgan Example

Email:
avery.placeholder@example.test

Phone:
+61 400 000 000

Postal Address:
100 Example Street, Demo Suburb, NT 0800, Australia

ABN / Business Reference:
00 000 000 000

Payment Term:
Invoice payable within 14 days of approved milestone delivery.

Banking Note:
Payment details to be confirmed through secure approved channel. Do not process from this form.

Private Note:
Artist has requested that unreleased project details are not shared outside the review team.

Signature Placeholder:
/s/ Avery Placeholder

Date:
01 January 2026
```

## Intended demo use

Use this fixture to demonstrate:

```text
received
→ extracted
→ classified
→ classified_with_findings
→ redacted
→ needs_review
→ approved_for_ai or blocked
→ used_or_exported
```

## Expected detection labels

| Source field | Expected label | Notes |
|---|---|---|
| River Echo Demo Project | `[PROJECT_NAME]` | Synthetic artist/project name |
| Avery Placeholder | `[PERSON_NAME]` | Synthetic contact name |
| Morgan Example | `[PERSON_NAME]` | Synthetic representative name |
| avery.placeholder@example.test | `[EMAIL]` | Reserved `.test` domain |
| +61 400 000 000 | `[PHONE]` | Fake demo phone number |
| 100 Example Street, Demo Suburb, NT 0800, Australia | `[ADDRESS]` | Synthetic address |
| 00 000 000 000 | `[BUSINESS_REFERENCE]` | Synthetic ABN-style placeholder |
| Invoice payable within 14 days of approved milestone delivery | `[PAYMENT_TERM]` | Contract/payment term |
| Payment details to be confirmed through secure approved channel | `[PAYMENT_NOTE]` | Sensitive payment-process note |
| Artist has requested that unreleased project details are not shared outside the review team | `[PRIVATE_NOTE]` | Confidential/private note |
| /s/ Avery Placeholder | `[SIGNATURE]` | Signature placeholder |
| 01 January 2026 | `[DATE]` | Synthetic date |

## Expected redacted output

```text
ARTIST ONBOARDING FORM — SYNTHETIC DEMO ONLY

Artist / Project Name:
[PROJECT_NAME]

Primary Contact:
[PERSON_NAME]

Representative / Manager:
[PERSON_NAME]

Email:
[EMAIL]

Phone:
[PHONE]

Postal Address:
[ADDRESS]

ABN / Business Reference:
[BUSINESS_REFERENCE]

Payment Term:
[PAYMENT_TERM]

Banking Note:
[PAYMENT_NOTE]

Private Note:
[PRIVATE_NOTE]

Signature Placeholder:
[SIGNATURE]

Date:
[DATE]
```

## Expected classification

```text
classification: contains personal, business-reference, payment-process, and confidential project information
recommended_state: needs_review
reason: the document contains contact details, address-style information, payment-related notes, signature placeholder, and private project information
```

## Expected blocked actions before approval

Before `approval_state == approved_for_ai`, the prototype should block:

- summarising the raw source document
- querying the raw source document
- exporting the raw source document
- embedding the raw source document
- generating a client-facing report from unreviewed content

## Expected safe summary after approval

```text
This synthetic artist onboarding form contains contact, address, business-reference, payment-process, and private project fields. Sensitive values were replaced with category labels before approval.
```

## Fixture review note

This fixture is intentionally artificial. It is useful for proving the Safe Intake control path, not for proving detection accuracy on real-world documents.
