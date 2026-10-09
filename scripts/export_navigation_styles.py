#!/usr/bin/env python3
"""Regenerate repo-local Atlas and Feature Ledger visual CSS without changing diagram graph."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from verify_design_system import ROOT, TokenError, load_tokens
from export_design_tokens import write_atomic

SURFACES = (
    "docs/diagrams/index.html",
    "specs/002-skill-manifest-registry/diagrams.html",
    "specs/003-product-pro-max-design-system/diagrams.html",
)
STYLE = re.compile(r"<style>[\s\S]*?</style>")
REV = re.compile(r'data-ppmax-token-revision="[0-9]+\.[0-9]+\.[0-9]+"')
TARGET_ROLES = ("surface", "surface-elevated", "text-primary", "text-secondary",
                "accent-brand", "focus-ring", "link", "border-strong",
                "node-fill", "node-outline", "edge", "label-muted")


def palette(tokens: dict, theme: str) -> str:
    roles = tokens["themes"][theme]
    declarations = [f"  --ppmax-{name}: {roles[name]};" for name in TARGET_ROLES]
    font = ", ".join('"' + x + '"' if x not in ("sans-serif", "serif", "monospace") else x
                     for x in tokens["typography"]["ui"])
    return "\n".join(["  color-scheme: " + theme + ";", *declarations,
                      f"  --ppmax-font-ui: {font};", ""])


def style(tokens: dict) -> str:
    return """/* ppmax-navigation revision=""" + tokens["revision"] + """ derived from design-system/tokens.json */
:root{
""" + palette(tokens, "light") + """}
@media (prefers-color-scheme: dark){:root{
""" + palette(tokens, "dark") + """}}
body{font:16px/1.6 var(--ppmax-font-ui);background:var(--ppmax-surface);color:var(--ppmax-text-primary);margin:0;padding:28px}
main{max-width:1100px;margin:auto;min-width:0}
nav{display:flex;flex-wrap:wrap;gap:16px;font-size:14px;margin-bottom:22px}
a{color:var(--ppmax-link);text-underline-offset:3px}
a:focus-visible{outline:3px solid var(--ppmax-focus-ring);outline-offset:4px;border-radius:3px}
h1{font-size:28px;line-height:1.2}
p,footer{color:var(--ppmax-text-secondary);line-height:1.5}
strong{color:var(--ppmax-text-primary)}
ul{list-style:none;padding:0}
li{margin:12px 0;padding:10px 14px;border-left:4px solid var(--ppmax-accent-brand);background:var(--ppmax-surface-elevated);border-radius:6px}
svg{display:block;width:100%;height:auto;background:var(--ppmax-node-fill);border:1px solid var(--ppmax-border-strong);border-radius:10px}
svg text{font-family:var(--ppmax-font-ui);fill:var(--ppmax-text-primary)}
svg .node{fill:var(--ppmax-node-fill);stroke:var(--ppmax-node-outline);stroke-width:2}
svg .edge{stroke:var(--ppmax-edge);stroke-width:2;fill:none}
svg .small{font-size:14px;fill:var(--ppmax-label-muted)}
@media(max-width:600px){body{padding:16px}h1{font-size:24px}nav{gap:10px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
"""


def render_html(original: str, tokens: dict) -> str:
    if len(STYLE.findall(original)) != 1:
        raise TokenError("navigation HTML must have exactly one style element")
    result = STYLE.sub(lambda _: "<style>" + style(tokens) + "</style>", original, count=1)
    if REV.search(result):
        result = REV.sub(f'data-ppmax-token-revision="{tokens["revision"]}"', result, count=1)
    else:
        result = result.replace("<html ", f'<html data-ppmax-token-revision="{tokens["revision"]}" ', 1)
    if f'data-ppmax-token-revision="{tokens["revision"]}"' not in result:
        raise TokenError("navigation HTML lacks revision metadata")
    return result


def run(root: Path = ROOT, check: bool = True) -> None:
    tokens = load_tokens(root)
    expected_style = style(tokens)
    for path in SURFACES:
        target = root / path
        raw = target.read_text(encoding="utf-8")
        if check:
            if raw != render_html(raw, tokens):
                raise TokenError(f"{path}: navigation token/style drift (no write)")
        else:
            if "ppmax-navigation revision=" not in raw:
                # First migration is controlled: outside <style> only the machine revision attribute may be added.
                pass
            write_atomic(target, render_html(raw, tokens))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    try:
        run(args.root, args.check)
        print("PASS: three Atlas/Feature Ledger surfaces use repo token themes; read-only" if args.check else "EXPORTED: three navigation token skins")
    except (TokenError, OSError, UnicodeError) as exc:
        p.exit(1, f"FAIL: {exc}\n")


if __name__ == "__main__":
    main()
