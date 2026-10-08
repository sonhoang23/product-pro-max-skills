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
    workflow_inventory, validate_discovery_metadata,
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
        validate_discovery_metadata(data, path)
        for relation in data["related_skills"]:
            if relation["skill_id"] == sid:
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
