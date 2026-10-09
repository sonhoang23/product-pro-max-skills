#!/usr/bin/env python3
"""Render standalone, offline Signal Protocol SVG assets deterministically from repo-local tokens."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from verify_design_system import ROOT, load_tokens, TokenError
from export_design_tokens import write_atomic

LAYOUTS = Path("design-system/brand-layouts.json")
ASSET_PATH = Path("assets/brand")

def render_assets(root: Path = ROOT) -> dict[str, str]:
    t = load_tokens(root)
    layouts = json.loads((root / LAYOUTS).read_text(encoding="utf-8"))
    if layouts.get("schema_version") != 1 or not isinstance(layouts.get("templates"), dict):
        raise TokenError("invalid brand layouts")
    result = {}
    for name, entry in sorted(layouts["templates"].items()):
        if name not in {"signal-path.svg", "wordmark.svg", "hero-dark.svg", "hero-light.svg", "docs-specimen.svg", "social-cover.svg"}:
            raise TokenError(f"unknown asset: {name}")
        palette = t["themes"][entry["theme"]]
        values = {"surface": palette["surface"], "elevated": palette["surface-elevated"],
                  "accent": palette["accent-brand"], "text": palette["text-primary"],
                  "muted": palette["text-secondary"], "stroke": palette["border-strong"],
                  "evidence": palette["evidence-emphasis"], "gate": palette["gate-result-emphasis"],
                  "decision": palette["decision-emphasis"], "font": ", ".join(t["typography"]["ui"])}
        try:
            result[name] = entry["body"].format_map(values)
        except KeyError as exc:
            raise TokenError(f"{name}: unresolved visual role {exc}") from exc
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true", help="Compare read-only; never write")
    args = parser.parse_args()
    try:
        rendered = render_assets(args.root)
        for name, output in rendered.items():
            path = args.root / ASSET_PATH / name
            if args.check:
                try:
                    existing = path.read_bytes()
                except OSError as exc:
                    raise TokenError(f"{name}: missing generated SVG: {exc}") from exc
                if existing != output.encode("utf-8"):
                    raise TokenError(f"{name}: asset drift; regenerate explicitly")
            else:
                write_atomic(path, output)
        print(f"PASS: {len(rendered)} brand assets {'read-only verified' if args.check else 'exported'}")
        return 0
    except (TokenError, ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")

if __name__ == "__main__":
    sys.exit(main())
