#!/usr/bin/env python3
"""Deterministic, offline CSS/SVG token export; --check never writes files."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from pathlib import Path

from verify_design_system import ROOT, COLOR, TokenError, load_tokens, resolve


def canonical(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def css_font(fonts: list[str]) -> str:
    return ", ".join(font if font in ("sans-serif", "serif", "monospace") else f'"{font}"' for font in fonts)


def render(data: dict, *, surface: str = "diagram", theme: str | None = None,
           density: str = "default", format: str = "css", accent_preview: str | None = None) -> str:
    # Alternate accent is an ephemeral *visual preview*, not an official brand or
    # mutation of the canonical repository tokens.
    if accent_preview is not None:
        if not COLOR.fullmatch(accent_preview):
            raise TokenError(f"accent-preview {accent_preview!r}: expected #RRGGBB")
        data = copy.deepcopy(data)
        for values in data["themes"].values():
            values["accent-brand"] = accent_preview.upper()
    selected, roles, multipliers = resolve(data, surface, theme, density)
    if format not in ("css", "svg-css"):
        raise TokenError("format must be css or svg-css")
    revision = hashlib.sha256(canonical(data)).hexdigest()[:16]
    selector = ":root" if format == "css" else "svg.ppmax-design-system"
    lines = [f"/* ppmax-design-system revision={data['revision']} fingerprint={revision} surface={surface} theme={selected} density={density}; generated; do not edit */", f"{selector} {{"]
    for role in sorted(roles):
        lines.append(f"  --ppmax-{role}: {roles[role]};")
    for family in ("ui", "mono"):
        lines.append(f"  --ppmax-font-{family}: {css_font(data['typography'][family])};")
    for name, px in sorted(data["typography"]["size_px"].items()):
        lines.append(f"  --ppmax-type-{name}: {px * multipliers['type_multiplier']:g}px;")
    for name, px in sorted(data["geometry"]["spacing_px"].items()):
        lines.append(f"  --ppmax-space-{name}: {px * multipliers['spacing_multiplier']:g}px;")
    for name, px in sorted(data["geometry"]["radius_px"].items()):
        lines.append(f"  --ppmax-radius-{name}: {px:g}px;")
    for name, px in sorted(data["geometry"]["stroke_px"].items()):
        lines.append(f"  --ppmax-stroke-{name}: {px * multipliers['stroke_multiplier']:g}px;")
    return "\n".join([*lines, "}", ""])


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent,
                                         prefix=".ppmax-", delete=False) as output:
            staging = Path(output.name)
            output.write(content)
        os.replace(staging, path)
    finally:
        if staging is not None:
            staging.unlink(missing_ok=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--surface", default="diagram")
    p.add_argument("--theme")
    p.add_argument("--density", default="default")
    p.add_argument("--format", default="css", choices=("css", "svg-css"))
    p.add_argument("--accent-preview", help="decorative #RRGGBB preview only; never changes repo tokens")
    p.add_argument("--output", type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    try:
        data = load_tokens(args.root)
        generated = render(data, surface=args.surface, theme=args.theme, density=args.density,
                           format=args.format, accent_preview=args.accent_preview)
        if args.check:
            if args.output is not None:
                try:
                    actual = args.output.read_bytes()
                except OSError as exc:
                    raise TokenError(f"output missing for no-write check: {args.output}: {exc}") from exc
                if actual != generated.encode("utf-8"):
                    raise TokenError(f"visual token snapshot drift: {args.output}; regenerate explicitly")
            print("PASS: read-only token export check; no files modified")
        elif args.output is not None:
            write_atomic(args.output, generated)
            print(f"EXPORTED: {args.output} (revision={data['revision']})")
        else:
            print(generated, end="")
    except TokenError as exc:
        p.exit(1, f"FAIL: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
