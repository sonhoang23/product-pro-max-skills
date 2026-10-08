#!/usr/bin/env python3
"""Static SVG bounds, geometry and accessible label checks for living diagrams."""
import json
import re
import html
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "{http://www.w3.org/2000/svg}"


class SVGs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks = []
        self.current = None
        self.depth = 0
    def handle_starttag(self, tag, attrs):
        if tag == "svg":
            self.current = [self.get_starttag_text()]
            self.depth = 1
        elif self.current is not None:
            self.current.append(self.get_starttag_text())
            if tag not in ("path", "rect", "line", "polyline", "polygon", "circle", "ellipse", "use", "stop"):
                self.depth += 1
    def handle_endtag(self, tag):
        if self.current is not None:
            self.current.append(f"</{tag}>")
            if tag == "svg":
                self.chunks.append("".join(self.current))
                self.current = None


def inspect(path):
    issues = []
    text = path.read_text(encoding="utf-8")
    chunks = [m.group() for m in re.finditer(r'<svg\b[\s\S]*?</svg>', text)]
    if not chunks:
        return ["no SVG found"]
    for markup in chunks:
        try:
            # HTML SVG markup often omits XML namespace; SVG tree still parses.
            root = ET.fromstring(markup)
        except ET.ParseError:
            # HTML5 permits entities and void syntax that XML does not.
            if 'viewBox="' not in markup or 'aria-labelledby=' not in markup:
                issues.append("SVG requires viewBox and aria-labelledby")
            continue
        view = root.attrib.get("viewBox", "").split()
        if len(view) != 4:
            issues.append("invalid/missing SVG viewBox"); continue
        try:
            x0, y0, width, height = [float(x) for x in view]
        except ValueError:
            issues.append("non-numeric viewBox"); continue
        if width <= 0 or height <= 0:
            issues.append("non-positive viewBox"); continue
        ids = {el.attrib["id"] for el in root.iter() if "id" in el.attrib}
        for label in root.attrib.get("aria-labelledby", "").split():
            if label not in ids:
                issues.append(f"unresolved accessible label: {label}")
        for el in root.iter():
            tag = el.tag.split("}")[-1]
            if tag not in ("rect", "text", "circle"): continue
            def num(k, default=0):
                try: return float(el.attrib.get(k, default))
                except ValueError: return None
            x, y = num("x"), num("y")
            if tag == "circle":
                x, y = num("cx"), num("cy")
                radius = num("r")
                if radius is None: issues.append("invalid circle radius"); continue
                left, right, top, bottom = x-radius, x+radius, y-radius, y+radius
            else:
                if x is None or y is None: issues.append(f"invalid {tag} position"); continue
                w, h = num("width"), num("height")
                if tag == "rect" and (w is None or h is None):
                    issues.append("invalid rect size"); continue
                left, right, top, bottom = x, x+(w or 0), y, y+(h or 0)
            # Text anchor/actual glyph extents need visual QA, not coordinate checks.
            if tag != "text" and (left < x0 or top < y0 or right > x0+width or bottom > y0+height):
                issues.append(f"{tag} outside viewBox")
    return issues


def main():
    registry = ROOT / "docs/diagrams/diagram-index.json"
    if not registry.is_file():
        print("FAIL missing diagram registry"); return 1
    entries = json.loads(registry.read_text(encoding="utf-8")).get("diagrams", [])
    problems = []
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            problems.append(f"{entry['path']}: missing"); continue
        for issue in inspect(path):
            problems.append(f"{entry['path']}: {issue}")
    for issue in problems: print("FAIL", issue)
    if problems:
        print(f"FAIL {len(problems)} layout violations"); return 1
    print(f"OK static layout checks: {len(entries)} diagrams (browser visual QA not included)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
