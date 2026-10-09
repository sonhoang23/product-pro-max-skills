#!/usr/bin/env python3
"""Resolve Product Pro Max style mapping from the active repository, never user HOME."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from verify_design_system import ROOT, TokenError, load_tokens, resolve

ROLE_MAP = {
    "paper": "surface", "paper-2": "surface-elevated", "ink": "text-primary", "muted": "text-secondary", "soft": "label-muted",
    "rule": "rule", "rule-solid": "border-strong", "accent": "accent-brand", "link": "link",
    "node-fill": "node-fill", "node-stroke": "node-outline", "edge": "edge", "focus": "focus-ring",
}

def resolve_repo_style(root: Path = ROOT, theme: str = "light", density: str = "default") -> dict:
    data = load_tokens(root)
    selected, palette, multipliers = resolve(data, "diagram", theme, density)
    return {
        "source": "design-system/tokens.json", "revision": data["revision"], "theme": selected,
        "density": density, "roles": {name: palette[role] for name, role in ROLE_MAP.items()},
        "geometry": multipliers, "brand_accent_use": "decoration-only",
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--theme", default="light")
    parser.add_argument("--density", default="default")
    args = parser.parse_args()
    try:
        print(json.dumps(resolve_repo_style(args.root, args.theme, args.density),
                         ensure_ascii=False, sort_keys=True, indent=2))
    except TokenError as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
