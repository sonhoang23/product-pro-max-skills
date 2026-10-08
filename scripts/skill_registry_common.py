#!/usr/bin/env python3
"""Shared fail-closed parsing, inventory and reference primitives for Spec 002.

This module does not write generated registry files. Full manifest integrity checks
and registry generation are completed in later user-story phases.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_ID_RE = re.compile(r"^ppmax-[a-z0-9]+(?:-[a-z0-9]+)*$")


class RegistryValidationError(ValueError):
    """Source-specific registry validation error."""


class UniqueSafeLoader(yaml.SafeLoader):
    """Safe YAML loader additionally rejecting duplicate mapping keys."""


def _unique_mapping(loader: UniqueSafeLoader, node: yaml.MappingNode) -> dict:
    result: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "mapping", node.start_mark, "unhashable YAML key", key_node.start_mark
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "mapping", node.start_mark,
                f"duplicate YAML key {key!r}", key_node.start_mark
            )
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


def parse_yaml(path: Path) -> dict[str, Any]:
    """Load only safe, mapping-root YAML, including readable source diagnostics."""
    try:
        with path.open("r", encoding="utf-8") as stream:
            data = yaml.load(stream, Loader=UniqueSafeLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise RegistryValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise RegistryValidationError(f"{path}: YAML root must be a mapping")
    return data


def load_product_model(root: Path = ROOT) -> dict[str, Any]:
    path = root / "model/product-model.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RegistryValidationError(f"{path}: invalid Product Model: {exc}") from exc
    if not isinstance(data, dict):
        raise RegistryValidationError(f"{path}: Product Model must be an object")
    cycles = data.get("lifecycle", {}).get("cycles")
    if not isinstance(cycles, list):
        raise RegistryValidationError(f"{path}: lifecycle.cycles must be an array")
    return data


def product_vocabulary(root: Path = ROOT) -> dict[str, Any]:
    """Use Product Model identifiers and phase ownership; never hard-code enums."""
    model = load_product_model(root)
    ownership: dict[str, set[str]] = {}
    for cycle in model["lifecycle"]["cycles"]:
        if not isinstance(cycle, dict) or not isinstance(cycle.get("id"), str):
            raise RegistryValidationError("Product Model: malformed cycle")
        cid = cycle["id"]
        if cid in ownership:
            raise RegistryValidationError(f"Product Model: duplicate cycle {cid}")
        phases = cycle.get("phases", [])
        if not isinstance(phases, list):
            raise RegistryValidationError(f"Product Model: invalid phases in {cid}")
        ownership[cid] = set()
        for phase in phases:
            if not isinstance(phase, dict) or not isinstance(phase.get("id"), str):
                raise RegistryValidationError(f"Product Model: invalid phase in {cid}")
            pid = phase["id"]
            if pid in ownership[cid]:
                raise RegistryValidationError(f"Product Model: duplicate phase {pid}")
            ownership[cid].add(pid)
    result: dict[str, Any] = {"phase_map": ownership, "cycles": set(ownership)}
    for key in ("tracks", "gates", "decisions"):
        entries = model.get(key)
        if not isinstance(entries, list):
            raise RegistryValidationError(f"Product Model: missing {key}")
        ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
        if len(ids) != len(entries) or any(not isinstance(i, str) for i in ids):
            raise RegistryValidationError(f"Product Model: invalid {key}")
        if len(ids) != len(set(ids)):
            raise RegistryValidationError(f"Product Model: duplicate {key} ID")
        result[key] = set(ids)
    return result


def workflow_inventory(root: Path = ROOT) -> dict[str, Path]:
    """Discover authoritative workflow IDs without interpreting execution steps."""
    folder = root / "workflows"
    inventory: dict[str, Path] = {}
    if not folder.is_dir():
        return inventory
    for path in sorted(folder.glob("*/workflow.yaml")):
        data = parse_yaml(path)
        workflow_id = data.get("name")
        if not isinstance(workflow_id, str) or not ID_RE.fullmatch(workflow_id):
            raise RegistryValidationError(f"{path}: invalid workflow name")
        if path.parent.name != workflow_id:
            raise RegistryValidationError(f"{path}: workflow name/path mismatch")
        if workflow_id in inventory:
            raise RegistryValidationError(f"{path}: duplicate workflow ID {workflow_id}")
        inventory[workflow_id] = path
    return inventory


def skill_inventory(root: Path = ROOT, *, allow_legacy: bool = False) -> list[tuple[Path, Path]]:
    """Enumerate all canonical pairs, rejecting partial, legacy or nested paths.

    Only the root skills/ subtree participates; .agents/ is never traversed.
    allow_legacy is an explicit migration diagnostic, not a bypass for validation.
    """
    folder = root / "skills"
    if not folder.is_dir():
        raise RegistryValidationError(f"{folder}: skills directory missing")
    pairs: list[tuple[Path, Path]] = []
    for skill_file in sorted(folder.rglob("SKILL.md")):
        rel = skill_file.relative_to(folder)
        if len(rel.parts) != 3:
            if allow_legacy and len(rel.parts) == 2:
                continue
            raise RegistryValidationError(f"{skill_file}: noncanonical skill path")
        cycle, skill_id, _ = rel.parts
        if not ID_RE.fullmatch(cycle) or not SKILL_ID_RE.fullmatch(skill_id):
            raise RegistryValidationError(f"{skill_file}: invalid cycle or skill directory")
        manifest = skill_file.with_name("manifest.yaml")
        if not manifest.is_file():
            raise RegistryValidationError(f"{manifest}: missing sibling manifest")
        pairs.append((skill_file, manifest))
    for manifest in sorted(folder.rglob("manifest.yaml")):
        if not manifest.with_name("SKILL.md").is_file():
            raise RegistryValidationError(f"{manifest}: manifest without SKILL.md")
    return pairs


def validate_cycle_association(
    primary_cycle: str, lifecycle: list[dict[str, str]], tracks: list[str],
    vocabulary: dict[str, Any], source: Path
) -> None:
    """Validate model references and primary-cycle membership."""
    if primary_cycle not in vocabulary["cycles"]:
        raise RegistryValidationError(f"{source}: unknown primary_cycle {primary_cycle}")
    if not isinstance(lifecycle, list) or not lifecycle:
        raise RegistryValidationError(f"{source}: lifecycle must be nonempty")
    seen: set[tuple[str, str | None]] = set()
    for item in lifecycle:
        if not isinstance(item, dict) or set(item) - {"cycle", "phase"} or "cycle" not in item:
            raise RegistryValidationError(f"{source}: invalid lifecycle association")
        cycle, phase = item["cycle"], item.get("phase")
        if not isinstance(cycle, str) or (phase is not None and not isinstance(phase, str)):
            raise RegistryValidationError(f"{source}: lifecycle cycle/phase must be strings")
        if cycle not in vocabulary["cycles"]:
            raise RegistryValidationError(f"{source}: unknown lifecycle cycle {cycle}")
        if phase is not None and phase not in vocabulary["phase_map"][cycle]:
            raise RegistryValidationError(f"{source}: phase {phase!r} does not belong to {cycle}")
        entry = (cycle, phase)
        if entry in seen:
            raise RegistryValidationError(f"{source}: duplicate lifecycle association {entry}")
        seen.add(entry)
    if not any(cycle == primary_cycle for cycle, _ in seen):
        raise RegistryValidationError(f"{source}: primary_cycle missing from lifecycle")
    if not isinstance(tracks, list) or any(not isinstance(t, str) for t in tracks) or len(tracks) != len(set(tracks)):
        raise RegistryValidationError(f"{source}: tracks must be a unique list")
    for track in tracks:
        if track not in vocabulary["tracks"]:
            raise RegistryValidationError(f"{source}: unknown track {track}")


def validate_discovery_metadata(data: dict[str, Any], source: Path) -> None:
    """Validate semantic discovery fields without influencing skill execution."""
    def fail(reason: str) -> None:
        raise RegistryValidationError(f"{source}: {reason}")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        fail("description must be nonempty")
    triggers = data.get("triggers")
    if not isinstance(triggers, dict) or set(triggers) != {"include", "exclude"}:
        fail("triggers must contain include and exclude")
    for name in ("include", "exclude"):
        values = triggers[name]
        if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
            fail(f"triggers.{name} must be nonempty descriptions")
    required = {
        "inputs": {"name", "description", "required"},
        "outputs": {"name", "description"},
        "related_skills": {"skill_id", "type"},
        "workflows": {"workflow_id", "role"},
    }
    extras = {"outputs": {"semantic_kind"}}
    identities = {"inputs": "name", "outputs": "name", "related_skills": "skill_id", "workflows": "workflow_id"}
    for field, keys in required.items():
        items = data.get(field)
        if not isinstance(items, list):
            fail(f"{field} must be a list")
        seen = set()
        for item in items:
            if not isinstance(item, dict) or not keys <= set(item) or set(item) - (keys | extras.get(field, set())):
                fail(f"invalid {field} item")
            for key in keys:
                value = item[key]
                if key == "required":
                    if type(value) is not bool:
                        fail("inputs.required must be boolean")
                elif not isinstance(value, str) or not value.strip():
                    fail(f"{field}.{key} must be nonempty")
            identity = item[identities[field]]
            if identity in seen:
                fail(f"duplicate {field} reference: {identity}")
            seen.add(identity)
            if field == "outputs" and "semantic_kind" in item and item["semantic_kind"] not in {"evidence", "gate", "decision"}:
                fail("invalid outputs.semantic_kind")
            if field == "related_skills" and item["type"] not in {"prerequisite", "complements", "produces-input-for"}:
                fail("invalid related_skills.type")
