#!/usr/bin/env python3
"""Validate Product Pro Max repository invariants using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
WORKFLOWS = ROOT / "workflows"
PRODUCT_MODEL = ROOT / "model" / "product-model.json"

REQUIRED_DOCS = [
    "README.md",
    "README.vi.md",
    "CONSTITUTION.md",
    "PRODUCT-POSITIONING.md",
    "PRODUCT-MODEL.md",
    "SKILL-CONTRACT.md",
    "EVIDENCE-MODEL.md",
    "QUALITY-GATES.md",
    "CONTRIBUTING.md",
    "LICENSE",
]

REQUIRED_SECTIONS = [
    "Purpose",
    "Trigger",
    "Inputs",
    "Workflow",
    "Evidence rules",
    "Output contract",
    "Quality gate",
    "Stop conditions",
    "Anti-patterns",
    "Example",
]

EXPECTED_SKILLS = {
    "ppmax-idea-pressure-test",
    "ppmax-problem-validation",
    "ppmax-customer-research",
    "ppmax-market-landscape",
    "ppmax-icp-positioning",
    "ppmax-mvp-scope",
    "ppmax-ux-flow",
    "ppmax-architecture-plan",
    "ppmax-engineering-readiness",
    "ppmax-runtime-verification",
    "ppmax-launch-readiness",
    "ppmax-distribution-plan",
    "ppmax-pricing-experiment",
}

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: top-level value must be an object")
        return {}
    return value


def ids(items: object, label: str, errors: list[str]) -> list[str]:
    if not isinstance(items, list) or not items:
        errors.append(f"Product Model: {label} must be a non-empty list")
        return []
    result: list[str] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append(f"Product Model: every {label} item must have a string id")
            continue
        item_id = item["id"]
        if ID_PATTERN.fullmatch(item_id) is None:
            errors.append(f"Product Model: invalid {label} id '{item_id}'")
        result.append(item_id)
    duplicates = sorted({item for item in result if result.count(item) > 1})
    if duplicates:
        errors.append(f"Product Model: duplicate {label} ids: {', '.join(duplicates)}")
    return result


def validate_product_model(errors: list[str]) -> dict[str, object]:
    model = load_json(PRODUCT_MODEL, errors)
    if not model:
        return {}

    lifecycle = model.get("lifecycle")
    if not isinstance(lifecycle, dict) or lifecycle.get("ordered") is not True:
        errors.append("Product Model: lifecycle.ordered must be true")
        return {}

    cycles = lifecycle.get("cycles")
    cycle_ids = ids(cycles, "cycle", errors)
    phase_ids: list[str] = []
    phase_map: dict[str, list[str]] = {}

    if isinstance(cycles, list):
        for cycle in cycles:
            if not isinstance(cycle, dict) or not isinstance(cycle.get("id"), str):
                continue
            phases = cycle.get("phases")
            current = ids(phases, f"phase in cycle '{cycle['id']}'", errors)
            phase_map[cycle["id"]] = current
            phase_ids.extend(current)

    duplicate_phases = sorted({item for item in phase_ids if phase_ids.count(item) > 1})
    if duplicate_phases:
        errors.append(
            "Product Model: phase ids must be globally unique: "
            + ", ".join(duplicate_phases)
        )

    track_ids = ids(model.get("tracks"), "track", errors)
    loop_ids = ids(model.get("loops"), "loop", errors)
    gate_ids = ids(model.get("gates"), "gate", errors)
    decision_ids = ids(model.get("decisions"), "decision", errors)
    status_ids = ids(model.get("project_statuses"), "project status", errors)

    if gate_ids != ["pass", "warn", "fail"]:
        errors.append("Product Model: gates must be exactly pass, warn, fail in canonical order")

    return {
        "cycles": cycle_ids,
        "phases": phase_ids,
        "phase_map": phase_map,
        "tracks": track_ids,
        "loops": loop_ids,
        "gates": gate_ids,
        "decisions": decision_ids,
        "statuses": status_ids,
    }


def validate_dependent_contracts(model: dict[str, object], errors: list[str]) -> None:
    if not model:
        return

    skill_output = load_json(ROOT / "schemas" / "skill-output.schema.json", errors)
    props = skill_output.get("properties", {}) if isinstance(skill_output, dict) else {}
    gate_enum = props.get("gate", {}).get("enum") if isinstance(props, dict) else None
    decision_enum = props.get("decision", {}).get("enum") if isinstance(props, dict) else None
    if gate_enum != model["gates"]:
        errors.append("schemas/skill-output.schema.json: gate enum drift from Product Model")
    if decision_enum != model["decisions"]:
        errors.append("schemas/skill-output.schema.json: decision enum drift from Product Model")

    project_state = load_json(ROOT / "schemas" / "project-state.schema.json", errors)
    state_props = project_state.get("properties", {}) if isinstance(project_state, dict) else {}
    expected = {
        "cycle": model["cycles"],
        "phase": model["phases"],
        "status": model["statuses"],
    }
    for key, values in expected.items():
        enum = state_props.get(key, {}).get("enum") if isinstance(state_props, dict) else None
        if enum != values:
            errors.append(
                f"schemas/project-state.schema.json: {key} enum drift from Product Model"
            )

    actual_map: dict[str, list[str]] = {}
    for clause in project_state.get("allOf", []) if isinstance(project_state, dict) else []:
        if not isinstance(clause, dict):
            continue
        cycle = (
            clause.get("if", {})
            .get("properties", {})
            .get("cycle", {})
            .get("const")
        )
        phases = (
            clause.get("then", {})
            .get("properties", {})
            .get("phase", {})
            .get("enum")
        )
        if isinstance(cycle, str) and isinstance(phases, list):
            actual_map[cycle] = phases
    if actual_map != model["phase_map"]:
        errors.append(
            "schemas/project-state.schema.json: cycle/phase ownership drift from Product Model"
        )

    template_path = ROOT / "templates" / "project-state" / "project.yaml"
    if not template_path.exists():
        errors.append("Missing required file: templates/project-state/project.yaml")
    else:
        template = template_path.read_text(encoding="utf-8")
        values: dict[str, str] = {}
        for line in template.splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                key, value = line.split(":", 1)
                values[key.strip()] = value.strip()
        if "stage" in values:
            errors.append("templates/project-state/project.yaml: legacy 'stage' field is not canonical")
        for key in ("cycle", "phase", "status"):
            if key not in values:
                errors.append(f"templates/project-state/project.yaml: missing '{key}'")
        if values.get("cycle") not in model["cycles"]:
            errors.append("templates/project-state/project.yaml: invalid default cycle")
        if values.get("phase") not in model["phases"]:
            errors.append("templates/project-state/project.yaml: invalid default phase")
        if values.get("status") not in model["statuses"]:
            errors.append("templates/project-state/project.yaml: invalid default status")
        if (
            values.get("cycle") in model["phase_map"]
            and values.get("phase") not in model["phase_map"][values["cycle"]]
        ):
            errors.append("templates/project-state/project.yaml: default cycle/phase pair is invalid")


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    skill_paths = sorted(SKILLS.glob("*/ppmax-*/SKILL.md")) if SKILLS.exists() else []
    actual_skills = {p.parent.name for p in skill_paths}
    if len(skill_paths) != len(actual_skills):
        errors.append("Duplicate canonical skill directory names across primary cycles")

    missing = EXPECTED_SKILLS - actual_skills
    if missing:
        errors.append(f"Missing MVP skills: {', '.join(sorted(missing))}")

    for path in skill_paths:
        name = path.parent.name
        if not (path.parent / "manifest.yaml").is_file():
            errors.append(f"{path.parent}: missing sibling manifest.yaml")
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)

        if frontmatter.get("name") != name:
            errors.append(f"{path}: frontmatter name must equal directory name")
        if len(frontmatter.get("description", "")) < 40:
            errors.append(f"{path}: description is missing or too weak")

        for section in REQUIRED_SECTIONS:
            pattern = rf"^## {re.escape(section)}\s*$"
            if re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE) is None:
                errors.append(f"{path}: missing section '{section}'")

    schemas = sorted((ROOT / "schemas").glob("*.json"))
    if not schemas:
        errors.append("No JSON schemas found")
    for schema in schemas:
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{schema}: invalid JSON: {exc}")

    product_model = validate_product_model(errors)
    validate_dependent_contracts(product_model, errors)

    workflow_files = sorted(WORKFLOWS.glob("*/workflow.yaml")) if WORKFLOWS.exists() else []
    if len(workflow_files) < 3:
        errors.append("Expected at least three MVP workflows")

    for workflow_file in workflow_files:
        text = workflow_file.read_text(encoding="utf-8")
        refs = re.findall(r"^\s+skill:\s+([a-z0-9-]+)\s*$", text, flags=re.MULTILINE)
        if not refs:
            errors.append(f"{workflow_file}: no skill references found")
        for ref in refs:
            if ref not in actual_skills:
                errors.append(f"{workflow_file}: unknown skill '{ref}'")

    readme_path = ROOT / "README.md"
    if readme_path.exists():
        readme = readme_path.read_text(encoding="utf-8")
        if "Product Pro Max Skills" not in readme:
            errors.append("README.md: brand missing")
        if "From vibe to viable." not in readme:
            errors.append("README.md: tagline missing")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validation passed: {len(actual_skills)} canonical skills, "
        f"{len(workflow_files)} workflows, {len(schemas)} schemas, "
        f"{len(product_model.get('cycles', []))} cycles, "
        f"{len(product_model.get('phases', []))} phases."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
