#!/usr/bin/env python3
"""Safely import the private Codex+ChatGPT skills bridge into a local Codex project.

This helper takes a locally supplied ZIP. It neither downloads anything nor
modifies GitHub, app/plugin permissions, or the active Codex process. No overwrite.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from zipfile import BadZipFile, ZipFile

EXPECTED = frozenset({
    "engineering-closure",
    "role-evaluation",
    "skill-routing-audit",
    "source-bound-recovery",
    "vendor-tool-triage",
    "verified-deliverable",
})
MAX_FILE_BYTES = 1_048_576
MAX_TOTAL_BYTES = 12_000_000


class ImportErrorSafe(Exception):
    """Unsafe archive, incomplete bundle, or destination conflict."""


def _verify_filename(info):
    name = info.filename
    if not name or name.startswith("/") or "\\" in name or "\x00" in name:
        raise ImportErrorSafe("Unsafe archive member name")
    parts = PurePosixPath(name).parts
    if ".." in parts or any(part in ("", ".") for part in parts):
        raise ImportErrorSafe("Unsafe relative archive path")
    mode = (info.external_attr >> 16) & 0xFFFF
    if stat.S_ISLNK(mode):
        raise ImportErrorSafe("Archive contains a symbolic link")
    if info.file_size > MAX_FILE_BYTES:
        raise ImportErrorSafe("Archive member exceeds the file size limit")
    return parts


def _load_archive(path):
    contents = {}
    exec_bits = {}
    total = 0
    try:
        with ZipFile(path) as archive:
            for info in archive.infolist():
                parts = _verify_filename(info)
                total += info.file_size
                if total > MAX_TOTAL_BYTES:
                    raise ImportErrorSafe("Archive exceeds the size limit")
                if info.is_dir():
                    continue
                # Portable plugin archives have one optional wrapper root.
                idx = parts.index("skills") if "skills" in parts else -1
                if idx < 0 or len(parts) < idx + 3:
                    continue
                if parts[idx + 1] not in EXPECTED:
                    raise ImportErrorSafe("Unexpected skill in archive")
                if idx > 1:
                    raise ImportErrorSafe("Unsupported archive nesting")
                rel = PurePosixPath(*parts[idx + 1:])
                if rel in contents:
                    raise ImportErrorSafe("Duplicate archive member")
                contents[rel] = archive.read(info)
                # Preserve only the safe executable bits; never set setuid/setgid.
                exec_bits[rel] = stat.S_IMODE((info.external_attr >> 16) & 0xFFFF) & 0o111
    except (BadZipFile, OSError) as exc:
        raise ImportErrorSafe(f"Could not read archive: {exc}") from exc

    present = {p.parts[0] for p in contents}
    if present != EXPECTED:
        raise ImportErrorSafe(f"Skill mismatch: expected {sorted(EXPECTED)}, found {sorted(present)}")
    for name in EXPECTED:
        manifest = PurePosixPath(name, "SKILL.md")
        try:
            text = contents[manifest].decode("utf-8")
        except (KeyError, UnicodeDecodeError) as exc:
            raise ImportErrorSafe(f"Missing or invalid SKILL.md: {name}") from exc
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            raise ImportErrorSafe(f"Invalid manifest frontmatter: {name}")
        try:
            closing = lines.index("---", 1)
        except ValueError as exc:
            raise ImportErrorSafe(f"Missing closing frontmatter delimiter: {name}") from exc
        frontmatter = "\n".join(lines[1:closing])
        if not re.search(
            r"^name:[ \t]*['\\\"]?" + re.escape(name) + r"['\\\"]?[ \t]*$",
            frontmatter, re.MULTILINE,
        ) or not re.search(r"^description:[ \t]*\S+", frontmatter, re.MULTILINE):
            raise ImportErrorSafe(f"Invalid manifest frontmatter: {name}")
    return contents, exec_bits


def _check_destination(root, contents, exec_bits):
    if not root.is_dir() or root.is_symlink():
        raise ImportErrorSafe("Project root must be an existing real directory")
    dest = root / ".agents" / "skills"
    for component in (root / ".agents", dest):
        if component.is_symlink() or (component.exists() and not component.is_dir()):
            raise ImportErrorSafe("Destination path is not a safe directory")
    decisions = {}
    for name in sorted(EXPECTED):
        folder = dest / name
        if folder.is_symlink():
            raise ImportErrorSafe(f"Existing skill is a symlink: {name}")
        files = {'/'.join(p.parts[1:]): blob
                 for p, blob in contents.items() if p.parts[0] == name}
        if not folder.exists():
            decisions[name] = "install"
            continue
        if not folder.is_dir():
            raise ImportErrorSafe(f"Existing skill is not a directory: {name}")
        actual = {}
        for file in folder.rglob("*"):
            if file.is_symlink():
                raise ImportErrorSafe(f"Existing skill contains symlinks: {name}")
            if file.is_file():
                relative = file.relative_to(folder).as_posix()
                actual[relative] = file.read_bytes()
                expected = exec_bits.get(PurePosixPath(name, relative), 0)
                observed = stat.S_IMODE(file.stat().st_mode) & 0o111
                if observed != expected:
                    raise ImportErrorSafe(f"Existing skill executable permissions differ: {name}/{relative}")
        if actual != files:
            raise ImportErrorSafe(f"Existing skill differs; refusing overwrite: {name}")
        decisions[name] = "unchanged"
    return dest, decisions


def import_bridge(archive_path, root, mode):
    archive_path = Path(archive_path).expanduser().resolve(strict=True)
    root = Path(root).expanduser().resolve(strict=True)
    contents, exec_bits = _load_archive(archive_path)
    dest, plan = _check_destination(root, contents, exec_bits)
    if mode == "verify" and "install" in plan.values():
        raise ImportErrorSafe("Missing installed skills: " + ", ".join(k for k, v in plan.items() if v == "install"))
    if mode == "install" and "install" in plan.values():
        dest.mkdir(parents=True, exist_ok=True)
        # Stage content first; existing skills are never replaced.
        with tempfile.TemporaryDirectory(prefix="skill-bridge-", dir=dest) as tmp:
            tmp_path = Path(tmp)
            for rel, blob in contents.items():
                if plan[rel.parts[0]] != "install":
                    continue
                target = tmp_path.joinpath(*rel.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(blob)
                target.chmod(0o644 | exec_bits[rel])
            for name in sorted(EXPECTED):
                if plan[name] == "install":
                    if (dest / name).exists() or (dest / name).is_symlink():
                        raise ImportErrorSafe(f"Destination appeared during install: {name}")
                    os.rename(tmp_path / name, dest / name)
    if mode != "dry-run":
        _, after = _check_destination(root, contents, exec_bits)
        if "install" in after.values():
            raise ImportErrorSafe("Post-install readback failed")
    return {
        "mode": mode,
        "status": "verified" if mode != "dry-run" else "dry_run",
        "archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        "destination": str(dest),
        "skills": plan,
        "all_six_present": mode != "dry-run",
        "note": "Files only. Host auto-discovery and execution are not verified by this command.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", help="Existing private skills-bridge ZIP file")
    parser.add_argument("--project", default=".", help="Existing local Codex project directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)
    if args.dry_run and args.verify:
        parser.error("Use only one of --dry-run and --verify")
    mode = "verify" if args.verify else "dry-run" if args.dry_run else "install"
    try:
        print(json.dumps(import_bridge(args.archive, args.project, mode), indent=2))
        return 0
    except (ImportErrorSafe, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
