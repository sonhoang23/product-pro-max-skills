#!/usr/bin/env python3
"""Dependency-free installer for Product Pro Max Skills."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def available_skills() -> list[str]:
    return sorted(
        p.name
        for p in SKILLS_DIR.glob("*/ppmax-*")
        if p.is_dir() and (p / "SKILL.md").is_file() and (p / "manifest.yaml").is_file()
    )


def source_path(name: str) -> Path:
    matches = list(SKILLS_DIR.glob(f"*/{name}"))
    if len(matches) != 1:
        raise SystemExit(f"Expected one canonical skill directory for {name}, found {len(matches)}")
    return matches[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Product Pro Max skills into an Agent Skills directory."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Destination skills directory, e.g. .agents/skills",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Install all canonical skills")
    group.add_argument("--skills", help="Comma-separated skill names")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing")
    parser.add_argument("--force", action="store_true", help="Replace existing skill directories")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    known = set(available_skills())
    names = sorted(known) if args.all else [s.strip() for s in args.skills.split(",") if s.strip()]
    unknown = [name for name in names if name not in known]
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}")

    target = Path(args.target).expanduser().resolve()

    for name in names:
        src = source_path(name)
        dst = target / name
        prefix = "[dry-run] " if args.dry_run else ""
        print(f"{prefix}{src} -> {dst}")

        if args.dry_run:
            continue

        target.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            if not args.force:
                raise SystemExit(f"Destination exists: {dst}. Use --force to replace it.")
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print(f"Selected {len(names)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
