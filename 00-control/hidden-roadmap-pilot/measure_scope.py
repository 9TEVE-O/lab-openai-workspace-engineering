from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()

    changed = [p for p in git(args.repo, "diff", "--name-only", args.base, args.head).splitlines() if p]
    numstat = git(args.repo, "diff", "--numstat", args.base, args.head).splitlines()
    added = deleted = 0
    prod_added = prod_deleted = 0
    for line in numstat:
        a, d, path = line.split("\t", 2)
        if a == "-" or d == "-":
            continue
        a_i, d_i = int(a), int(d)
        added += a_i
        deleted += d_i
        if path.startswith("sqlite_utils/") and path.endswith(".py"):
            prod_added += a_i
            prod_deleted += d_i

    production_files = sorted(
        p for p in changed if p.startswith("sqlite_utils/") and p.endswith(".py")
    )
    test_files = sorted(p for p in changed if p.startswith("tests/") and p.endswith(".py"))
    documentation_files = sorted(
        p for p in changed if p.startswith("docs/") or p in {"README.md", "CHANGELOG.md"}
    )
    payload = {
        "changed_files": sorted(changed),
        "documentation_files": documentation_files,
        "lines_added": added,
        "lines_deleted": deleted,
        "production_churn": prod_added + prod_deleted,
        "production_lines_added": prod_added,
        "production_lines_deleted": prod_deleted,
        "production_python_files": production_files,
        "production_python_files_changed": len(production_files),
        "test_files": test_files,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
