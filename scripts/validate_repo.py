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

REQUIRED_DOCS = [
    "README.md",
    "README.vi.md",
    "CONSTITUTION.md",
    "PRODUCT-POSITIONING.md",
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
    "idea-pressure-test",
    "problem-validation",
    "customer-research",
    "market-landscape",
    "icp-positioning",
    "mvp-scope",
    "ux-flow",
    "architecture-plan",
    "engineering-readiness",
    "runtime-verification",
    "launch-readiness",
    "distribution-plan",
    "pricing-experiment",
}


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


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    actual_skills = {
        p.name
        for p in SKILLS.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    } if SKILLS.exists() else set()

    missing = EXPECTED_SKILLS - actual_skills
    if missing:
        errors.append(f"Missing MVP skills: {', '.join(sorted(missing))}")

    for name in sorted(actual_skills):
        path = SKILLS / name / "SKILL.md"
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
        f"{len(workflow_files)} workflows, {len(schemas)} schemas."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
