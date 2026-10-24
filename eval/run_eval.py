#!/usr/bin/env python3
"""Run the frozen AI Brain Trust v3 fixtures through one local GGUF model."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PROMPT_BY_KIND = {
    "business": "The World-Class Advisor Blueprint",
    "career": "The Second Brain Career Accelerator",
    "finance": "The Wealth Architecture Strategist",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def render_prompt(template: str, variables: dict[str, str]) -> str:
    rendered = template
    for key, value in variables.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([^{}]+)\}\}", rendered)))
    if unresolved:
        raise ValueError(f"Unresolved variables: {unresolved}")
    return rendered


def clean_stdout(text: str) -> str:
    text = text.replace("\r\n", "\n").strip()
    # Defensive removal of common llama-cli terminal artefacts only.
    text = re.sub(r"^>\s*", "", text)
    text = re.sub(r"\n>\s*$", "", text)
    return text.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--llama-cli", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--context", type=int, default=8192)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--threads", type=int, default=max(1, min(4, os.cpu_count() or 2)))
    args = parser.parse_args()

    prompts_path = Path(args.prompts)
    cases_path = Path(args.cases)
    model_path = Path(args.model_path)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt_export: dict[str, Any] = json.loads(prompts_path.read_text(encoding="utf-8"))
    case_export: dict[str, Any] = json.loads(cases_path.read_text(encoding="utf-8"))
    prompts = {p["title"]: p for p in prompt_export["prompts"]}

    expected_ids = {
        "The World-Class Advisor Blueprint": "a3f2e1b4-7c09-4d82-b5f6-1e8d3a0c9247",
        "The Second Brain Career Accelerator": "b7d4c2e5-1f30-4a96-c8e1-2f9b5d1e4738",
        "The Wealth Architecture Strategist": "c9e6d3f7-2a41-4b07-d9f2-3g0c6e2f5849",
    }
    for title, expected_id in expected_ids.items():
        if prompts.get(title, {}).get("id") != expected_id:
            raise RuntimeError(f"Prompt identity mismatch for {title}")
    if len(case_export.get("cases", [])) != 9:
        raise RuntimeError("Frozen fixture count must remain exactly nine")

    run_started = time.time()
    results: list[dict[str, Any]] = []
    transcript_parts = [
        f"# Cross-model transcript — {args.model_name}",
        "",
        f"- Prompt export SHA-256: `{sha256(prompts_path)}`",
        f"- Fixture export SHA-256: `{sha256(cases_path)}`",
        f"- Model file SHA-256: `{sha256(model_path)}`",
        "- Sampling: temperature 0, seed 42",
        f"- Context: {args.context}; maximum generated tokens: {args.max_tokens}",
        "",
    ]

    for case in case_export["cases"]:
        case_id = case["id"]
        kind = case["prompt"]
        title = PROMPT_BY_KIND[kind]
        prompt = prompts[title]
        rendered = render_prompt(prompt["content"], case["variables"])
        prompt_hash = hashlib.sha256(rendered.encode("utf-8")).hexdigest()

        cmd = [
            args.llama_cli,
            "-m", str(model_path),
            "-p", rendered,
            "-n", str(args.max_tokens),
            "-c", str(args.context),
            "--threads", str(args.threads),
            "--temp", "0",
            "--seed", "42",
            "--no-display-prompt",
            "--single-turn",
            "--log-disable",
        ]
        started = time.time()
        proc = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            timeout=1800,
            check=False,
        )
        elapsed = round(time.time() - started, 3)
        output = clean_stdout(proc.stdout)
        record = {
            "case_id": case_id,
            "case_name": case["name"],
            "prompt_kind": kind,
            "prompt_id": prompt["id"],
            "prompt_title": title,
            "rendered_prompt_sha256": prompt_hash,
            "return_code": proc.returncode,
            "elapsed_seconds": elapsed,
            "output": output,
            "stderr_tail": proc.stderr[-4000:] if proc.returncode else "",
        }
        results.append(record)

        transcript_parts.extend([
            f"## {case_id} — {case['name']}",
            "",
            f"- Prompt: `{title}`",
            f"- Rendered prompt SHA-256: `{prompt_hash}`",
            f"- Return code: `{proc.returncode}`",
            f"- Elapsed seconds: `{elapsed}`",
            "",
            output if output else "[NO MODEL OUTPUT]",
            "",
        ])
        print(f"completed {case_id}: rc={proc.returncode}, chars={len(output)}, seconds={elapsed}", flush=True)

    payload = {
        "schema_version": "0.1",
        "model_name": args.model_name,
        "model_file": model_path.name,
        "model_sha256": sha256(model_path),
        "prompt_export_file": prompts_path.name,
        "prompt_export_sha256": sha256(prompts_path),
        "fixture_file": cases_path.name,
        "fixture_sha256": sha256(cases_path),
        "fixture_count": len(results),
        "sampling": {"temperature": 0, "seed": 42, "context": args.context, "max_tokens": args.max_tokens},
        "started_unix": run_started,
        "elapsed_seconds": round(time.time() - run_started, 3),
        "results": results,
    }
    safe_name = re.sub(r"[^a-z0-9]+", "-", args.model_name.lower()).strip("-")
    (out_dir / f"{safe_name}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / f"{safe_name}.md").write_text("\n".join(transcript_parts), encoding="utf-8")

    failures = [r for r in results if r["return_code"] != 0 or not r["output"]]
    if failures:
        print(f"inference failures: {[r['case_id'] for r in failures]}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
