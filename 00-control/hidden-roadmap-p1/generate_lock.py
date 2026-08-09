from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from email.parser import Parser
from pathlib import Path


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_expected(path: Path) -> dict[str, tuple[str, str]]:
    expected: dict[str, tuple[str, str]] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise SystemExit(f"Unpinned requirement: {line}")
        name, version = line.split("==", 1)
        key = normalize(name)
        if key in expected:
            raise SystemExit(f"Duplicate requirement: {name}")
        expected[key] = (name, version)
    return expected


def wheel_metadata(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as zf:
        candidates = [
            n
            for n in zf.namelist()
            if n.endswith(".dist-info/METADATA") and n.count("/") == 1
        ]
        if len(candidates) != 1:
            raise SystemExit(f"Expected one top-level METADATA in {path.name}, found {len(candidates)}")
        metadata = Parser().parsestr(zf.read(candidates[0]).decode("utf-8"))
    return metadata["Name"], metadata["Version"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--sha256sums", type=Path, required=True)
    args = parser.parse_args()

    expected = parse_expected(args.requirements)
    wheels = sorted(args.wheelhouse.glob("*.whl"))
    found: dict[str, dict[str, str]] = {}

    for wheel in wheels:
        name, version = wheel_metadata(wheel)
        key = normalize(name)
        if key in found:
            raise SystemExit(f"Multiple wheels for {name}")
        digest = sha256(wheel)
        found[key] = {
            "name": name,
            "version": version,
            "filename": wheel.name,
            "sha256": digest,
        }

    missing = sorted(set(expected) - set(found))
    unexpected = sorted(set(found) - set(expected))
    if missing or unexpected:
        raise SystemExit(f"Wheel set mismatch: missing={missing} unexpected={unexpected}")

    for key, (_, expected_version) in expected.items():
        actual = found[key]["version"]
        if actual != expected_version:
            raise SystemExit(
                f"Version mismatch for {found[key]['name']}: expected {expected_version}, got {actual}"
            )

    records = [found[key] for key in sorted(found)]
    args.lock.write_text(
        "".join(
            f"{record['name']}=={record['version']} --hash=sha256:{record['sha256']}\n"
            for record in records
        )
    )
    args.manifest.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    args.sha256sums.write_text(
        "".join(f"{record['sha256']}  {record['filename']}\n" for record in records)
    )


if __name__ == "__main__":
    main()
