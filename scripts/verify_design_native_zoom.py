#!/usr/bin/env python3
"""Native Chromium UI Ctrl+Plus 200% zoom QA in an ephemeral Xvfb X11 display.

Unlike CSS zoom/CDP pageScaleFactor, Chromium's devicePixelRatio must change
from 1.0 to 2.0 while visualViewport.scale stays 1.0.
"""
from __future__ import annotations
import argparse
import base64
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from Xlib import display, XK, X
from Xlib.ext import xtest

ROOT = Path(__file__).resolve().parents[1]

TARGETS = (
    ("pilot-light", "specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html", "light", 6, 6),
    ("pilot-dark", "specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html", "dark", 6, 6),
    ("specimen-light", "tests/fixtures/design-system/specimen-light.html", "light", 5, 2),
    ("specimen-dark", "tests/fixtures/design-system/specimen-dark.html", "dark", 5, 2),
)

def press(d: display.Display, *symbols: str) -> None:
    keys = [d.keysym_to_keycode(XK.string_to_keysym(name)) for name in symbols]
    if any(key == 0 for key in keys):
        raise RuntimeError(f"missing native key mapping: {symbols}")
    for key in keys:
        xtest.fake_input(d, X.KeyPress, key)
    for key in reversed(keys):
        xtest.fake_input(d, X.KeyRelease, key)
    d.sync()

def measure(page):
    return page.evaluate("""() => ({
        devicePixelRatio: window.devicePixelRatio,
        layoutWidth: window.innerWidth,
        visualScale: window.visualViewport.scale,
        reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
        text: document.body.innerText,
        links: document.querySelectorAll('nav a').length,
        nodes: document.querySelectorAll('svg .node, svg .focus, [data-node-id]').length,
        edges: document.querySelectorAll('svg .edge, [data-edge-id]').length
    })""")

def run(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    evidence = []
    with sync_playwright() as p:
        d = display.Display()
        try:
            for name, rel, scheme, expected_nodes, expected_edges in TARGETS:
                browser = p.chromium.launch(headless=False, args=["--disable-gpu", "--no-sandbox"])
                try:
                    context = browser.new_context(viewport={"width": 1366, "height": 900},
                                                  color_scheme=scheme, reduced_motion="reduce")
                    context.route("http://**/*", lambda route: route.abort())
                    context.route("https://**/*", lambda route: route.abort())
                    page = context.new_page()
                    page.goto((ROOT / rel).resolve().as_uri(), wait_until="load")
                    page.bring_to_front()
                    before = measure(page)
                    if abs(before["devicePixelRatio"] - 1) > .02:
                        raise RuntimeError(f"{name}: unexpected baseline zoom {before}")
                    for _ in range(5):
                        press(d, "Control_L", "Shift_L", "equal")
                        time.sleep(.2)
                    after = measure(page)
                    if abs(after["devicePixelRatio"] - 2) > .02 or abs(after["visualScale"] - 1) > .02:
                        raise RuntimeError(f"{name}: native Ctrl+Plus 200% failed {after}")
                    if after["nodes"] != expected_nodes or after["edges"] != expected_edges:
                        raise RuntimeError(f"{name}: 200% zoom altered semantic inventory {after}")
                    if not after["reducedMotion"] or not after["links"]:
                        raise RuntimeError(f"{name}: reduced motion or navigation inaccessible")
                    for word in ("Skill Registry", "planned truth") if name.startswith("pilot") else ("Gate result", "Decision"):
                        if word not in after["text"]:
                            raise RuntimeError(f"{name}: required visible semantic label missing: {word}")
                    page.keyboard.press("Tab")
                    focus = page.evaluate("() => document.activeElement?.tagName")
                    if focus != "A":
                        raise RuntimeError(f"{name}: keyboard navigation lost at 200%: {focus}")
                    cdp = context.new_cdp_session(page)
                    png = cdp.send("Page.captureScreenshot", {"format": "png",
                                                              "fromSurface": True,
                                                              "captureBeyondViewport": False})
                    (output / f"{name}-native-zoom200.png").write_bytes(base64.b64decode(png["data"]))
                    cdp.detach()
                    evidence.append({
                        "target": name, "source": rel, "browser": browser.version,
                        "before": {k:before[k] for k in ("devicePixelRatio","layoutWidth","visualScale")},
                        "after": {k:after[k] for k in ("devicePixelRatio","layoutWidth","visualScale")},
                        "nodes": after["nodes"], "edges": after["edges"],
                        "reducedMotion": after["reducedMotion"], "keyboardFirstTab": focus,
                        "zoomMethod": "native_x11_XTest_Control_L_Shift_L_equal_five_times",
                        "result": "PASS"
                    })
                finally:
                    browser.close()
        finally:
            d.close()
    (output / "native-zoom-metrics.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: native Chromium Ctrl+Plus 200% X11 browser zoom: {len(evidence)} variants, 4 screenshots")
    return evidence

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".tmp-spec003-native-zoom")
    args = parser.parse_args()
    run(args.output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
