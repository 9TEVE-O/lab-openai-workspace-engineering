# Static Hosting Security Headers

## Purpose

Use this file when the Safe Intake demo is hosted as static files.

The current demo is still a prototype. Hosting it does not make it production-ready.

## Recommended headers

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

## CSP notes

The CSP assumes:

- JavaScript is loaded from `safe-intake-clickable-prototype.js`
- CSS is loaded from `safe-intake-clickable-prototype.css`
- no external images, fonts, scripts, APIs, or analytics are used
- no form submission is required
- no iframing is required

## Netlify example

```text
/demos/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-origin
```

## Before public hosting

Complete:

- manual accessibility and visual QA
- privacy review
- security review
- deployment review
- explicit demo-only disclaimer review
