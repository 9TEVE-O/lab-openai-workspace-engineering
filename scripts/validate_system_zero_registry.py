#!/usr/bin/env python3
"""Validate System Zero registry consistency using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "system-zero" / "registry.json"
PLUGIN_PATH = ROOT / "01-lab-ai-skill-pack" / ".codex-plugin" / "plugin.json"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    """Load a JSON object and append actionable errors instead of raising."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(
            f"Invalid JSON in {path.relative_to(ROOT)} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )
        return {}

    if not isinstance(data, dict):
        errors.append(f"Expected a JSON object in {path.relative_to(ROOT)}")
        return {}
    return data


def valid_date(value: Any) -> bool:
    """Return True only for real calendar dates in strict YYYY-MM-DD form."""
    if not isinstance(value, str) or DATE_PATTERN.fullmatch(value) is None:
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_threshold(skill_id: str, field: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
        errors.append(f"Skill '{skill_id}' field '{field}' must be a number between 0 and 1")


def validate() -> list[str]:
    errors: list[str] = []
    registry = load_json(REGISTRY_PATH, errors)
    plugin = load_json(PLUGIN_PATH, errors)
    if errors:
        return errors

    tier_defaults = registry.get("tier_defaults")
    if not isinstance(tier_defaults, dict):
        errors.append("Registry field 'tier_defaults' must be an object")
        tier_defaults = {}

    plugin_skills = plugin.get("skills")
    if not isinstance(plugin_skills, list) or not all(
        isinstance(item, str) and item for item in plugin_skills
    ):
        errors.append("Plugin field 'skills' must be a list of non-empty strings")
        plugin_skill_ids: set[str] = set()
    else:
        plugin_skill_ids = set(plugin_skills)
        if len(plugin_skill_ids) != len(plugin_skills):
            errors.append("Plugin field 'skills' contains duplicate entries")

    if not valid_date(registry.get("last_updated")):
        errors.append("Registry field 'last_updated' must be a valid YYYY-MM-DD date")

    skills = registry.get("skills")
    if not isinstance(skills, list):
        errors.append("Registry field 'skills' must be a list")
        return errors

    active_ids: set[str] = set()
    active_count = 0

    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            errors.append(f"Registry skills[{index}] must be an object")
            continue
        if skill.get("status") != "active":
            continue

        active_count += 1
        skill_id = skill.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            errors.append(f"Active skills[{index}] must have a non-empty string 'id'")
            skill_id = f"skills[{index}]"
        elif skill_id in active_ids:
            errors.append(f"Duplicate active skill id: '{skill_id}'")
        else:
            active_ids.add(skill_id)

        if skill_id not in plugin_skill_ids:
            errors.append(f"Active skill '{skill_id}' is missing from the plugin manifest")

        tier = skill.get("tier")
        if not isinstance(tier, int) or isinstance(tier, bool) or tier < 0:
            errors.append(f"Skill '{skill_id}' field 'tier' must be a non-negative integer")
            tier_key = None
        else:
            tier_key = f"T{tier}"

        defaults = tier_defaults.get(tier_key) if tier_key is not None else None
        if not isinstance(defaults, dict):
            if tier_key is not None:
                errors.append(f"Skill '{skill_id}' references undefined tier '{tier_key}'")
            defaults = {}

        allowed_models = defaults.get("models")
        if not isinstance(allowed_models, list) or not all(
            isinstance(model, str) and model for model in allowed_models
        ):
            if tier_key is not None:
                errors.append(f"Tier '{tier_key}' field 'models' must be a list of non-empty strings")
            allowed_model_ids: set[str] = set()
        else:
            allowed_model_ids = set(allowed_models)

        for field in ("model_default", "model_fallback"):
            model = skill.get(field)
            if not isinstance(model, str) or model not in allowed_model_ids:
                errors.append(
                    f"Skill '{skill_id}' field '{field}' must name a model permitted by tier '{tier_key}'"
                )

        for field in ("token_budget_in", "token_budget_out"):
            value = skill.get(field)
            limit = defaults.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"Skill '{skill_id}' field '{field}' must be a non-negative integer")
            elif not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
                if tier_key is not None:
                    errors.append(f"Tier '{tier_key}' field '{field}' must be a non-negative integer")
            elif value > limit:
                errors.append(
                    f"Skill '{skill_id}' field '{field}' ({value}) exceeds tier '{tier_key}' limit ({limit})"
                )

        validate_threshold(skill_id, "rollback_threshold", skill.get("rollback_threshold"), errors)
        validate_threshold(
            skill_id,
            "human_review_on_confidence_below",
            skill.get("human_review_on_confidence_below"),
            errors,
        )

        if not valid_date(skill.get("last_updated")):
            errors.append(f"Skill '{skill_id}' field 'last_updated' must be a valid YYYY-MM-DD date")

        skill_file = skill.get("skill_file")
        if not isinstance(skill_file, str) or not skill_file:
            errors.append(f"Skill '{skill_id}' field 'skill_file' must be a non-empty string")
        else:
            candidate = (ROOT / skill_file).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"Skill '{skill_id}' field 'skill_file' escapes the repository root")
            else:
                if not candidate.is_file():
                    errors.append(f"Skill '{skill_id}' references missing file: {skill_file}")

    if active_count == 0:
        errors.append("Registry must contain at least one active skill")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("System Zero registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("System Zero registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
