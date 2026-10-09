#!/usr/bin/env python3
"""Reversible Spec 002 pilot: CSS-only style substitution; no semantic or Atlas edits."""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path
from verify_design_system import ROOT, TokenError, load_tokens
from export_design_tokens import write_atomic

BACKUP = Path("tests/fixtures/design-system/pilot/original-spec002.html")
PREVIEW = Path("tests/fixtures/design-system/pilot/migrated-spec002.html")
ORIGINAL = Path("specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html")
TEMPLATE = Path("design-system/pilot-style.css.tpl")
ORIGINAL_GIT_BLOB = "6acb098a4e8513d50527bfb615a6561bf3520e16"
STYLE = re.compile(r"<style>[\s\S]*?</style>")

def git_blob(content: bytes) -> str:
    return hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()

def palette_css(data: dict, theme: str) -> str:
    colors = data["themes"][theme]
    fonts = ", ".join(t if t in {"sans-serif", "serif", "monospace"} else f'"{t}"'
                      for t in data["typography"]["ui"])
    lines = [":root {"] + [f"  --ppmax-{k}: {colors[k]};" for k in sorted(colors)]
    return "\n".join([*lines, f"  --ppmax-font-ui: {fonts};", "}", ""])

def replace_css(original: str, css: str) -> str:
    if len(STYLE.findall(original)) != 1:
        raise TokenError("baseline diagram must contain exactly one style element")
    updated = STYLE.sub(lambda _: "<style>" + css + "</style>", original, count=1)
    if STYLE.sub("<style>REPLACED-CSS-ONLY</style>", original) != STYLE.sub("<style>REPLACED-CSS-ONLY</style>", updated):
        raise TokenError("pilot semantic, graph, label or link drift")
    return updated

def build(root: Path = ROOT) -> tuple[str, str]:
    token = load_tokens(root)
    baseline = (root / BACKUP).read_bytes()
    if git_blob(baseline) != ORIGINAL_GIT_BLOB:
        raise TokenError("rollback baseline SHA mismatch")
    old = baseline.decode("utf-8")
    template = (root / TEMPLATE).read_text(encoding="utf-8")
    if template.count("{{THEMES}}") != 1:
        raise TokenError("migration style needs exactly one theme placeholder")
    declarations = palette_css(token, "light") + "@media(prefers-color-scheme:dark){\n" + palette_css(token, "dark") + "}\n"
    return old, replace_css(old, template.replace("{{THEMES}}", declarations))

def run(root: Path, action: str) -> None:
    old, candidate = build(root)
    original = root / ORIGINAL
    preview = root / PREVIEW
    if action == "check":
        if preview.read_bytes() != candidate.encode("utf-8"):
            raise TokenError("migrated pilot copy drift")
        if original.read_text(encoding="utf-8") != candidate:
            raise TokenError("promoted original drift; no write performed")
    elif action == "preview":
        write_atomic(preview, candidate)
    elif action == "promote":
        actual = original.read_text(encoding="utf-8")
        if actual not in (old, candidate):
            raise TokenError("concurrent original modification; refuse unsafe promotion")
        write_atomic(preview, candidate)
        write_atomic(original, candidate)
    elif action == "restore":
        actual = original.read_text(encoding="utf-8")
        if actual not in (old, candidate):
            raise TokenError("concurrent original modification; refuse unsafe restore")
        write_atomic(original, old)
    else:
        raise TokenError("unsupported action")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("action", choices=("preview", "promote", "restore", "check"))
    args = p.parse_args()
    try:
        run(args.root, args.action)
        print(f"PASS Spec 002 pilot {args.action}: CSS-only migration, baseline protected")
    except (OSError, UnicodeError, TokenError) as exc:
        p.exit(1, f"FAIL: {exc}\n")

if __name__ == "__main__":
    main()
