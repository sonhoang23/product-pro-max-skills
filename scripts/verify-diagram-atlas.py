#!/usr/bin/env python3
"""Verify living diagram registry, navigation, and planned/implemented scope."""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs/diagrams/diagram-index.json"
ATLAS = ROOT / "docs/diagrams/index.html"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for key, value in attrs if key == "href" and value)


def check_links(path, errors):
    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    for href in parser.hrefs:
        if re.match(r"^[a-z]+:", href) or href.startswith("//"):
            continue
        dest = href.split("#", 1)[0].split("?", 1)[0]
        if dest and not dest.endswith((".html", ".htm")):
            errors.append(f"{path.relative_to(ROOT)}: non-HTML navigation: {href}")
        elif dest and not (path.parent / dest).resolve().is_file():
            errors.append(f"{path.relative_to(ROOT)}: broken navigation: {href}")
    return parser.hrefs


def main():
    errors = []
    if not INDEX.is_file() or not ATLAS.is_file():
        print("FAIL missing Diagram Atlas/index"); return 1
    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        entries = data["diagrams"]
        assert isinstance(entries, list)
    except (ValueError, KeyError, TypeError, AssertionError) as exc:
        print(f"FAIL malformed registry: {exc}"); return 1
    ids = set()
    paths = set()
    for e in entries:
        if not isinstance(e, dict):
            errors.append("registry entry is not an object"); continue
        ident, rel = e.get("id"), e.get("path")
        if not isinstance(ident, str) or not ident:
            errors.append("registry entry has no ID")
        elif ident in ids:
            errors.append(f"duplicate ID: {ident}")
        ids.add(ident)
        if not isinstance(rel, str) or not rel.startswith(("specs/", "docs/diagrams/")):
            errors.append(f"{ident}: invalid path"); continue
        if rel in paths:
            errors.append(f"duplicate path: {rel}")
        paths.add(rel)
        file = ROOT / rel
        if not file.is_file():
            errors.append(f"{ident}: missing diagram: {rel}"); continue
        if e.get("scope") not in ("feature", "project"):
            errors.append(f"{ident}: invalid scope")
        if e.get("truth") not in ("planned", "implemented"):
            errors.append(f"{ident}: invalid truth")
        if e.get("scope") == "project" and e.get("truth") != "implemented":
            errors.append(f"{ident}: project diagram must be implemented")
        if e.get("phase") in ("spec", "plan", "tasks") and e.get("truth") != "planned":
            errors.append(f"{ident}: feature planning diagram must be planned")
        source = e.get("source")
        if not isinstance(source, str) or not (ROOT / source).is_file():
            errors.append(f"{ident}: missing canonical source: {source}")
        if e.get("scope") == "feature":
            feature = e.get("feature")
            if not isinstance(feature, str) or not (ROOT / "specs" / feature / "diagrams.html").is_file():
                errors.append(f"{ident}: missing feature ledger")
        content = file.read_text(encoding="utf-8")
        if "Diagram Atlas" not in content or "Feature Ledger" not in content and e.get("scope") == "feature":
            errors.append(f"{ident}: missing navigation chrome")
        check_links(file, errors)
    for e in entries:
        if not isinstance(e, dict): continue
        ident = e.get("id", "<unknown>")
        parent = e.get("parent")
        if parent not in ("repo-atlas", f"feature-{str(e.get('feature',''))[:3]}-ledger") and parent not in ids:
            errors.append(f"{ident}: invalid parent {parent}")
        for field in ("related", "children"):
            for other in e.get(field, []):
                if other not in ids:
                    errors.append(f"{ident}: unknown {field} ID {other}")
    atlas_links = check_links(ATLAS, errors)
    for e in entries:
        if isinstance(e, dict) and e.get("scope") == "feature":
            ledger = ROOT / "specs" / e["feature"] / "diagrams.html"
            if ledger.is_file():
                hrefs = check_links(ledger, errors)
                target = (ROOT / e["path"]).resolve()
                if not any((ledger.parent / h.split("#")[0]).resolve() == target for h in hrefs):
                    errors.append(f"{e['id']}: diagram not linked from ledger")
                if not any((ATLAS.parent / h.split("#")[0]).resolve() == ledger.resolve() for h in atlas_links):
                    errors.append(f"{e['id']}: ledger not linked from atlas")
    actual = {str(p.relative_to(ROOT)).replace("\\", "/") for root in (ROOT / "specs", ROOT / "docs/diagrams") if root.exists() for p in root.rglob("*.html") if re.search(r"(?:-diagram/|docs/diagrams/)", str(p).replace("\\", "/")) and p.name != "index.html"}
    for path in sorted(actual - paths):
        errors.append(f"unregistered diagram: {path}")
    for error in errors:
        print("FAIL", error)
    if errors:
        print(f"FAIL {len(errors)} atlas violations"); return 1
    print(f"OK Diagram Atlas: {len(entries)} registered diagrams, links and sources checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
