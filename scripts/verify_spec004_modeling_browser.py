#!/usr/bin/env python3
"""Capture and assert offline browser behavior for the Spec 004 planned diagram.

Automated metrics are not equivalent to human screenshot/semantic review.
"""
from __future__ import annotations
import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM = ROOT / "specs/004-versioning-compatibility/spec-diagram/compatibility-assessment.html"


def run(output: Path) -> list[dict]:
    from playwright.sync_api import sync_playwright

    output.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for scheme in ("light", "dark"):
                for width, height in ((1366, 900), (390, 844)):
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        color_scheme=scheme,
                        reduced_motion="reduce",
                    )
                    context.route("http://**/*", lambda route: route.abort())
                    context.route("https://**/*", lambda route: route.abort())
                    page = context.new_page()
                    try:
                        page.goto(DIAGRAM.resolve().as_uri(), wait_until="load")
                        metric = page.evaluate("""() => {
                          const panel = document.querySelector('.panel');
                          const svg = document.querySelector('svg');
                          return {
                            viewportWidth: window.innerWidth,
                            documentWidth: document.documentElement.scrollWidth,
                            panelWidth: panel?.clientWidth ?? 0,
                            panelScrollWidth: panel?.scrollWidth ?? 0,
                            svgRole: svg?.getAttribute('role'),
                            svgTitle: svg?.querySelector('title')?.textContent ?? '',
                            svgDescription: svg?.querySelector('desc')?.textContent ?? '',
                            nodeCount: svg?.querySelectorAll('rect.node').length ?? 0,
                            edgeCount: svg?.querySelectorAll('path.edge').length ?? 0,
                            sourceLabel: document.body.innerText.includes('planned truth'),
                            hasAllClassifications: ['Tương thích','Breaking','Cần review','Chưa đánh giá']
                              .every(s => [...svg.querySelectorAll('text')].some(t => t.textContent === s)),
                            links: [...document.querySelectorAll('nav a')].map(a => a.getAttribute('href'))
                          };
                        }""")
                        if metric["documentWidth"] > width + 1:
                            raise AssertionError(f"{scheme}@{width}: document overflow: {metric}")
                        if width == 390 and metric["panelScrollWidth"] <= metric["panelWidth"]:
                            raise AssertionError("390px diagram panel must provide intentional horizontal scroll")
                        if not (metric["svgTitle"] and metric["svgDescription"] and metric["svgRole"] == "img"):
                            raise AssertionError(f"{scheme}@{width}: inaccessible SVG")
                        if metric["nodeCount"] != 8 or metric["edgeCount"] != 7:
                            raise AssertionError(f"{scheme}@{width}: unexpected concept/arrow inventory: {metric}")
                        if not metric["sourceLabel"] or not metric["hasAllClassifications"]:
                            raise AssertionError(f"{scheme}@{width}: planned-source/status semantics missing")
                        for href in metric["links"]:
                            if not href or not (DIAGRAM.parent / href.split("#", 1)[0]).resolve().is_file():
                                raise AssertionError(f"{scheme}@{width}: broken local navigation {href!r}")
                        # Readable keyboard access and real navigation, independent from SVG shape.
                        page.keyboard.press("Tab")
                        first_tag = page.evaluate("() => document.activeElement?.tagName")
                        if first_tag != "A":
                            raise AssertionError(f"{scheme}@{width}: first Tab focus is {first_tag}")
                        page.locator("nav a").first.click()
                        if "Diagram Atlas" not in page.title():
                            raise AssertionError(f"{scheme}@{width}: Atlas navigation did not open")
                        page.go_back(wait_until="load")
                        page.locator(".panel").focus()
                        focus_tag = page.evaluate("() => document.activeElement?.className")
                        if "panel" not in str(focus_tag):
                            raise AssertionError(f"{scheme}@{width}: scroll region cannot be focused")
                        screenshot = context.new_cdp_session(page)
                        capture = screenshot.send("Page.captureScreenshot",
                            {"format": "png", "fromSurface": True, "captureBeyondViewport": False})
                        (output / f"spec004-{scheme}-{width}.png").write_bytes(
                            base64.b64decode(capture["data"]))
                        screenshot.detach()
                        results.append({
                            "variant": scheme, "viewport": [width, height],
                            "metrics": metric, "browser": browser.version,
                            "static_render": "PASS",
                            "navigation": "PASS",
                            "keyboard_focus": "PASS",
                            "manual_visual_review": "NOT_PERFORMED",
                            "published_release": "NOT_PERFORMED",
                        })
                    finally:
                        context.close()
        finally:
            browser.close()
    (output / "metrics.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = run(args.output)
    print(f"Spec 004 browser automated assertions: PASS ({len(results)} captures); manual screenshot review NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
