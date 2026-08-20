#!/usr/bin/env python3
"""Deterministic bounded test for CAPABILITY_INGEST_TEST_002 task-level routing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "system-zero" / "registry.json"


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def route_task(task_domains: set[str], registry: dict) -> dict:
    active = []
    for skill in registry.get("skills", []):
        if skill.get("status") != "active":
            continue
        overlap = task_domains.intersection(skill.get("domains", []))
        if overlap:
            active.append((len(overlap), skill))

    if not active:
        return {"decision": "NO_ACTIVE_ROUTE"}

    active.sort(key=lambda item: (-item[0], item[1]["id"]))
    skill = active[0][1]
    tier_key = f"T{skill['tier']}"
    permitted_models = registry["tier_defaults"][tier_key]["models"]

    assert skill["model_default"] in permitted_models
    assert skill["model_fallback"] in permitted_models

    return {
        "decision": "ROUTE",
        "skill_id": skill["id"],
        "tier": tier_key,
        "model_default": skill["model_default"],
        "model_fallback": skill["model_fallback"],
    }


def main() -> int:
    registry = load_registry()

    # This exact branch is used only to force a pull-request execution context
    # for the deterministic routing gate; routing behaviour is unchanged.
    security = route_task({"authz", "agentic-permissions"}, registry)
    assert security == {
        "decision": "ROUTE",
        "skill_id": "system-zero-security",
        "tier": "T0",
        "model_default": "claude_opus_4_8",
        "model_fallback": "gpt_5_5",
    }

    # system-zero-style-tokens exists only under planned_skills. Planned work must
    # not be treated as active merely because its domains match the task.
    planned_only = route_task({"design-tokens", "docs"}, registry)
    assert planned_only == {"decision": "NO_ACTIVE_ROUTE"}

    unknown = route_task({"unregistered-domain"}, registry)
    assert unknown == {"decision": "NO_ACTIVE_ROUTE"}

    print("CAPABILITY_INGEST_TEST_002 task-level model routing: PASS")
    print(json.dumps({
        "security_task": security,
        "planned_only_task": planned_only,
        "unknown_task": unknown,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
