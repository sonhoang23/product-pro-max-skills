#!/usr/bin/env python3
"""Deterministic derived registry generation/checking for Product Pro Max.

Usage: python scripts/generate_skill_registry.py {generate|check} [--root PATH]
The canonical manifests are always authoritative; check mode never writes.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from skill_registry_common import (
    ROOT, SKILL_ID_RE, RegistryValidationError, parse_yaml,
    product_vocabulary, skill_inventory, validate_cycle_association,
    workflow_inventory,
)

FIELDS = (
    "id", "namespace", "slug", "description", "primary_cycle",
    "lifecycle", "tracks", "triggers", "inputs", "outputs",
    "related_skills", "workflows",
)
RELATION_TYPES = {"prerequisite", "complements", "produces-input-for"}
KINDS = {"evidence", "gate", "decision"}


def _fail(source: Path, message: str) -> None:
    raise RegistryValidationError(f"{source}: {message}")


def _named_items(value: object, source: Path, field: str, keys: set[str],
                 required: set[str]) -> None:
    if not isinstance(value, list):
        _fail(source, f"{field} must be a list")
    seen = set()
    for item in value:
        if not isinstance(item, dict) or not required <= item.keys() or set(item) - keys:
            _fail(source, f"invalid {field} entry")
        for key in required:
            if key == "required":
                if not isinstance(item[key], bool):
                    _fail(source, f"{field}.required must be boolean")
            elif not isinstance(item[key], str) or not item[key].strip():
                _fail(source, f"{field}.{key} must be a nonempty string")
        if "description" in item and (not isinstance(item["description"], str) or not item["description"].strip()):
            _fail(source, f"{field}.description must be nonempty")
        if "semantic_kind" in item and item["semantic_kind"] not in KINDS:
            _fail(source, f"{field}: unknown semantic_kind")
        identity = item.get("name", item.get("skill_id", item.get("workflow_id")))
        if identity in seen:
            _fail(source, f"{field}: duplicate {identity}")
        seen.add(identity)


def _frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        _fail(path, "missing SKILL.md frontmatter")
    header = text.split("\n---\n", 1)[0].splitlines()[1:]
    names = [line.split(":", 1)[1].strip().strip('"\'') for line in header if line.startswith("name:")]
    if len(names) != 1:
        _fail(path, "expected exactly one frontmatter name")
    return names[0]


def build_registry(root: Path) -> bytes:
    """Validate entire canonical catalog before serialization; never write."""
    vocabulary = product_vocabulary(root)
    workflow_ids = workflow_inventory(root)
    entries = []
    seen_ids = set()
    seen_slugs = set()
    for skill_path, path in skill_inventory(root):
        data = parse_yaml(path)
        if set(data) != set(FIELDS):
            _fail(path, f"manifest keys mismatch: missing {sorted(set(FIELDS)-set(data))}; unexpected {sorted(set(data)-set(FIELDS))}")
        sid, slug, cycle = data["id"], data["slug"], data["primary_cycle"]
        if not isinstance(sid, str) or not SKILL_ID_RE.fullmatch(sid):
            _fail(path, "invalid canonical skill ID")
        if not isinstance(slug, str) or sid != f"ppmax-{slug}":
            _fail(path, "slug/id mismatch")
        if sid in seen_ids or slug in seen_slugs:
            _fail(path, "duplicate skill identity")
        seen_ids.add(sid)
        seen_slugs.add(slug)
        if data["namespace"] != "product-pro-max":
            _fail(path, "namespace mismatch")
        if not isinstance(data["description"], str) or not data["description"].strip():
            _fail(path, "description must be nonempty")
        if not isinstance(cycle, str) or skill_path.parent.name != sid or skill_path.parent.parent.name != cycle:
            _fail(path, "manifest/path/primary_cycle mismatch")
        if _frontmatter_name(skill_path) != sid:
            _fail(skill_path, "SKILL.md name mismatch")
        validate_cycle_association(cycle, data["lifecycle"], data["tracks"], vocabulary, path)
        triggers = data["triggers"]
        if not isinstance(triggers, dict) or set(triggers) != {"include", "exclude"}:
            _fail(path, "invalid triggers")
        for key in ("include", "exclude"):
            if not isinstance(triggers[key], list) or any(not isinstance(v, str) or not v.strip() for v in triggers[key]):
                _fail(path, f"triggers.{key} must contain descriptions")
        _named_items(data["inputs"], path, "inputs", {"name", "description", "required"}, {"name", "description", "required"})
        _named_items(data["outputs"], path, "outputs", {"name", "description", "semantic_kind"}, {"name", "description"})
        _named_items(data["related_skills"], path, "related_skills", {"skill_id", "type"}, {"skill_id", "type"})
        _named_items(data["workflows"], path, "workflows", {"workflow_id", "role"}, {"workflow_id", "role"})
        for relation in data["related_skills"]:
            if relation["type"] not in RELATION_TYPES or relation["skill_id"] == sid:
                _fail(path, "unknown or self-referential relation")
        for relation in data["workflows"]:
            if relation["workflow_id"] not in workflow_ids:
                _fail(path, f"unknown workflow {relation['workflow_id']}")
        entries.append({"path": skill_path.parent.relative_to(root).as_posix(), **data})
    for entry in entries:
        for relation in entry["related_skills"]:
            if relation["skill_id"] not in seen_ids:
                _fail(root / entry["path"] / "manifest.yaml", f"unresolved skill {relation['skill_id']}")
    payload = {"registry_version": 1, "skills": sorted(entries, key=lambda item: item["id"])}
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def run(mode: str, root: Path) -> int:
    expected = build_registry(root)
    target = root / "registry" / "skills.json"
    if mode == "check":
        try:
            actual = target.read_bytes()
        except OSError as exc:
            raise RegistryValidationError(f"{target}: registry missing or unreadable: {exc}") from exc
        if actual != expected:
            raise RegistryValidationError(f"{target}: registry drift; regenerate from canonical manifests")
        print(f"Registry check OK: {target}")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=".skills-", suffix=".tmp", delete=False) as stream:
            tmp = Path(stream.name)
            stream.write(expected)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, target)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    print(f"Registry generated: {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "check"))
    parser.add_argument("--root", type=Path, default=ROOT, help="repository fixture root")
    args = parser.parse_args(argv)
    try:
        return run(args.mode, args.root.resolve())
    except (RegistryValidationError, OSError, UnicodeError, TypeError, ValueError) as exc:
        print(f"Registry validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
