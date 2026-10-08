#!/usr/bin/env python3
"""Spec 002 read-only release verification; one command for Windows and Ubuntu."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    print("COMMAND:", sys.executable, *args, flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main() -> int:
    print("Python:", platform.python_version(), flush=True)
    print("PyYAML:", yaml.__version__, flush=True)
    registry_path = ROOT / "registry/skills.json"
    before = registry_path.read_bytes()
    registry = json.loads(before)
    names = [entry["id"] for entry in registry["skills"]]
    if len(names) != 13 or len(set(names)) != 13:
        raise SystemExit("Catalog cardinality/uniqueness mismatch: expected 13 canonical skills")
    if not all(name.startswith("ppmax-") for name in names):
        raise SystemExit("Unexpected noncanonical skill ID")
    if any(".agents" in entry["path"] for entry in registry["skills"]):
        raise SystemExit("Development tooling leaked into catalog")
    print("Canonical skill inventory:", len(names), flush=True)
    print("Registry SHA-256:", hashlib.sha256(before).hexdigest(), flush=True)
    workflows = sorted((ROOT / "workflows").glob("*/workflow.yaml"))
    print("Workflow inventory:", len(workflows), flush=True)
    if len(workflows) != 3:
        raise SystemExit("Workflow cardinality mismatch: expected 3")
    run("scripts/validate_repo.py")
    run("scripts/generate_skill_registry.py", "check")
    if registry_path.read_bytes() != before:
        raise SystemExit("Read-only check unexpectedly changed registry")
    run("-m", "unittest", "discover", "-s", "tests", "-p", "test_skill*.py", "-v")
    run("scripts/install.py", "--target", ".tmp-skills", "--all", "--dry-run")
    if registry_path.read_bytes() != before:
        raise SystemExit("Verification unexpectedly changed registry")
    print("RELEASE VERIFICATION PASS (read-only, no runtime skill invocation)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
