#!/usr/bin/env python3
"""Validate only repo-owned Signal Protocol presentation tokens (standard library)."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN_REL = Path("design-system/tokens.json")
COLOR = re.compile(r"#[0-9A-Fa-f]{6}\Z")
IDENT = re.compile(r"[a-z][a-z0-9-]*\Z")
REVISION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")
FONT = re.compile(r"[A-Za-z][A-Za-z0-9 -]*\Z")
ROLES = frozenset("""surface surface-elevated text-primary text-secondary rule border-strong
accent-brand focus-ring link node-fill node-outline edge edge-emphasis boundary
label-muted gate-result-emphasis decision-emphasis evidence-emphasis feedback-path
success warning danger neutral""".split())
THEMES = ("light", "dark")
DENSITIES = ("compact", "default", "spacious")
SURFACES = {"readme": "dark", "brand": "dark", "diagram": "light", "docs": "light"}
VISUAL_STATES = frozenset({"success", "warning", "danger", "neutral"})


class TokenError(ValueError):
    """Invalid or unavailable repository-local token contract."""


def require(condition: bool, explanation: str) -> None:
    if not condition:
        raise TokenError(explanation)


def keys(obj: object, expected: set[str], where: str) -> None:
    require(isinstance(obj, dict), f"{where}: expected object")
    absent, extra = expected - obj.keys(), obj.keys() - expected
    require(not absent and not extra, f"{where}: missing {sorted(absent)}; unknown {sorted(extra)}")


def positive_number(number: object, where: str, minimum: float = 0) -> None:
    require(type(number) in (int, float) and math.isfinite(number) and number > minimum,
            f"{where}: expected finite number > {minimum}")


def luminance(hex_color: str) -> float:
    values = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]


def contrast(a: str, b: str) -> float:
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + .05) / (dark + .05)


def validate(data: object) -> dict:
    keys(data, {"schema_version", "revision", "brand", "brand_accent_role", "surfaces", "themes", "typography", "geometry", "densities"}, "tokens")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "schema_version: expected 1")
    require(isinstance(data["revision"], str) and REVISION.fullmatch(data["revision"]), "revision: expected semver digits")
    require(data["brand"] == "signal-protocol" and data["brand_accent_role"] == "accent-brand", "brand: identity/alias mismatch")
    require(data["surfaces"] == SURFACES, "surfaces: invalid default theme mapping")
    keys(data["themes"], set(THEMES), "themes")
    for theme in THEMES:
        palette = data["themes"][theme]
        keys(palette, set(ROLES), f"themes.{theme}")
        for role, color in palette.items():
            require(isinstance(color, str) and COLOR.fullmatch(color), f"themes.{theme}.{role}: invalid CSS hex color")
        # WCAG text 4.5:1 and essential non-text marks 3:1, each against its real surface.
        for foreground, background, minimum in (
            ("text-primary", "surface", 4.5), ("text-secondary", "surface", 4.5),
            ("link", "surface", 4.5), ("text-primary", "node-fill", 4.5),
            ("label-muted", "node-fill", 4.5), ("focus-ring", "surface", 3),
            ("node-outline", "node-fill", 3), ("edge", "surface", 3),
            ("edge-emphasis", "surface", 3), ("boundary", "surface", 3),
            ("border-strong", "surface", 3), ("gate-result-emphasis", "surface", 3),
            ("decision-emphasis", "surface", 3), ("evidence-emphasis", "surface", 3),
            ("feedback-path", "surface", 3),
            ("success", "surface", 3), ("warning", "surface", 3),
            ("danger", "surface", 3), ("neutral", "surface", 3)
        ):
            ratio = contrast(palette[foreground], palette[background])
            require(ratio + 1e-9 >= minimum,
                    f"themes.{theme}.{foreground}/{background}: contrast {ratio:.2f}:1 below {minimum}:1")
    keys(data["typography"], {"ui", "mono", "size_px"}, "typography")
    for family in ("ui", "mono"):
        fonts = data["typography"][family]
        require(isinstance(fonts, list) and len(fonts) >= 2 and all(isinstance(f, str) and FONT.fullmatch(f) for f in fonts),
                f"typography.{family}: invalid local fallback fonts")
        require(fonts[-1] in ("sans-serif", "serif", "monospace"), f"typography.{family}: missing generic fallback")
    sizes = data["typography"]["size_px"]
    keys(sizes, {"body", "label", "caption", "title"}, "typography.size_px")
    for role, size in sizes.items():
        positive_number(size, f"typography.size_px.{role}", 13.999 if role in ("body", "label", "caption") else 0)
    keys(data["geometry"], {"spacing_px", "radius_px", "stroke_px"}, "geometry")
    for key, expected in (("spacing_px", {"xs", "sm", "md", "lg", "xl", "xxl"}),
                          ("radius_px", {"small", "medium", "large"}),
                          ("stroke_px", {"standard", "emphasis"})):
        values = data["geometry"][key]
        keys(values, expected, f"geometry.{key}")
        for name, value in values.items():
            positive_number(value, f"geometry.{key}.{name}")
    keys(data["densities"], set(DENSITIES), "densities")
    for density, spec in data["densities"].items():
        keys(spec, {"spacing_multiplier", "type_multiplier", "stroke_multiplier"}, f"densities.{density}")
        for name, value in spec.items():
            positive_number(value, f"densities.{density}.{name}")
        require(min(sizes[x] * spec["type_multiplier"] for x in ("body", "label", "caption")) >= 14,
                f"densities.{density}: font below 14px floor")
    return data


def load_tokens(root: Path = ROOT) -> dict:
    path = root / TOKEN_REL
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TokenError(f"repository-local tokens required at {path}: {exc}") from exc
    try:
        data = json.loads(content)
    except (ValueError, UnicodeError) as exc:
        raise TokenError(f"malformed tokens at {path}: {exc}") from exc
    return validate(data)


def resolve(data: dict, surface: str, theme: str | None, density: str) -> tuple[str, dict, dict]:
    require(surface in SURFACES, f"surface {surface!r} unsupported; allowed: {', '.join(SURFACES)}")
    selected = theme if theme is not None else data["surfaces"][surface]
    require(selected in THEMES, f"theme {selected!r} unsupported; allowed: {', '.join(THEMES)}")
    require(density in DENSITIES, f"density {density!r} unsupported; allowed: {', '.join(DENSITIES)}")
    return selected, data["themes"][selected], data["densities"][density]


def resolve_visual_state(data: dict, theme: str, role: str, visible_label: str) -> str:
    """Resolve only a *presentation* state; never derive a workflow decision."""
    require(theme in THEMES, f"theme {theme!r} unsupported")
    require(role in VISUAL_STATES, f"visual state role {role!r} unresolved")
    require(isinstance(visible_label, str) and bool(visible_label.strip()),
            f"visual state {role!r}: required visible label missing")
    try:
        return data["themes"][theme][role]
    except KeyError as exc:
        raise TokenError(f"themes.{theme}.{role}: visual state role missing") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check-tokens", action="store_true")
    parser.add_argument("--surface", default="diagram")
    parser.add_argument("--theme")
    parser.add_argument("--density", default="default")
    args = parser.parse_args()
    try:
        data = load_tokens(args.root)
        theme, _, _ = resolve(data, args.surface, args.theme, args.density)
    except TokenError as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    print(f"PASS: repo-local tokens validated (revision={data['revision']}, theme={theme}, density={args.density}); browser QA not performed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
