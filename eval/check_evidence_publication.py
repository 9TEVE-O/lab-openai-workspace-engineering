#!/usr/bin/env python3
"""Fail closed when browser state or unexpected Prompt Vault evidence could be published.

Runs before uploading browser evidence and again before publishing the collected
artifacts branch. Checks paths and file types; deliberately never reads browser data.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ALLOWED_VAULT_FILES = frozenset({
    "prompt-vault-import-report.json",
    "01-before-import.png",
    "02-after-import.png",
})
BLOCKED_PARTS = frozenset({
    "isolated-browser-profile", "browser-profile", "user-data-dir",
    "default", "cookies", "cookies-journal", "local storage",
    "session storage", "indexeddb", "cache", "code cache", "service worker",
    "network", "singletoncookie", "singletonlock",
})


def check_tree(root: Path, mode: str) -> list[str]:
    errors: list[str] = []
    if root.is_symlink() or not root.is_dir():
        return [f"Missing, symlinked, or invalid evidence directory: {root}"]
    files: set[str] = set()
    for item in root.rglob("*"):
        relative = item.relative_to(root)
        parts = tuple(part.casefold() for part in relative.parts)
        label = relative.as_posix()
        if item.is_symlink():
            errors.append(f"Symlink forbidden in evidence: {label}")
            continue
        if not item.is_dir() and not item.is_file():
            errors.append(f"Non-regular evidence entry: {label}")
            continue
        if any(part in BLOCKED_PARTS for part in parts):
            errors.append(f"Browser state forbidden in evidence: {label}")
            continue
        if item.is_dir():
            continue
        files.add(label)
        if mode == "browser":
            if label not in ALLOWED_VAULT_FILES:
                errors.append(f"Unexpected Prompt Vault evidence: {label}")
        elif mode == "collected":
            if len(relative.parts) < 2:
                errors.append(f"Unexpected top-level evidence file: {label}")
            elif relative.parts[0] == "prompt-vault-import":
                if len(relative.parts) != 2 or relative.parts[1] not in ALLOWED_VAULT_FILES:
                    errors.append(f"Unexpected Prompt Vault evidence: {label}")
            elif not relative.parts[0].startswith("model-"):
                errors.append(f"Unexpected evidence namespace: {label}")
        else:
            raise ValueError("Unrecognised evidence mode")
    if mode == "browser" and "prompt-vault-import-report.json" not in files:
        errors.append("Missing Prompt Vault verification report")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("browser", "collected"), required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    errors = check_tree(args.root, args.mode)
    if errors:
        for error in errors:
            print(f"EVIDENCE GATE HOLD: {error}", file=sys.stderr)
        return 1
    print(f"EVIDENCE GATE PASS: {args.mode} evidence paths validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
