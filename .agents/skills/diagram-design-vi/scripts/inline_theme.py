#!/usr/bin/env python3
"""Materialize a standalone diagram HTML by inlining one local theme stylesheet."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

LINK_RE = re.compile(
    r"""<link\b(?=[^>]*\brel=["'][^"']*\bstylesheet\b[^"']*["'])
        (?=[^>]*\bhref=["']([^"']+)["'])[^>]*>""",
    re.IGNORECASE | re.VERBOSE,
)


def is_remote(value: str) -> bool:
    lowered = value.strip().casefold()
    return lowered.startswith(("http://", "https://", "//", "data:"))


def materialize(source_path: Path, output_path: Path | None = None) -> Path:
    source_path = source_path.resolve()
    html = source_path.read_text(encoding="utf-8")

    chosen: tuple[re.Match[str], Path] | None = None
    for match in LINK_RE.finditer(html):
        href = match.group(1).strip()
        if is_remote(href):
            continue
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        css_path = (source_path.parent / parsed.path).resolve()
        if css_path.is_file():
            chosen = (match, css_path)
            break

    if chosen is None:
        raise RuntimeError("No resolvable local stylesheet link found to inline.")

    match, css_path = chosen
    css = css_path.read_text(encoding="utf-8")
    if re.search(r"</style", css, re.IGNORECASE):
        raise RuntimeError("Theme CSS contains a closing </style token and cannot be safely inlined.")

    replacement = f"<style data-inlined-diagram-theme>\n{css}\n</style>"
    standalone = html[: match.start()] + replacement + html[match.end() :]

    if output_path is None:
        output_path = source_path.with_name(f"{source_path.stem}-standalone.html")
    else:
        output_path = output_path.resolve()

    output_path.write_text(standalone, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Living diagram HTML that links a local theme.css")
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    output = materialize(args.source, args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
