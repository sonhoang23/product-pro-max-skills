#!/usr/bin/env python3
"""Spec 003 full-checkout Chromium QA. Keeps browser/native zoom and GitHub UI claims separate."""
from __future__ import annotations
import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "tests/fixtures/design-system/pilot/migrated-spec002.html"
ORIGINAL = ROOT / "specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html"
SPECIMEN = ROOT / "tests/fixtures/design-system"
ASSETS = ROOT / "assets/brand"


def run(output: Path, source: Path = CANDIDATE) -> list[dict]:
    from playwright.sync_api import sync_playwright
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for name, target, scheme in (
                ("pilot-light", source, "light"),
                ("pilot-dark", source, "dark"),
                ("specimen-light", SPECIMEN / "specimen-light.html", "light"),
                ("specimen-dark", SPECIMEN / "specimen-dark.html", "dark"),
                ("hero-light", ASSETS / "hero-light.svg", "light"),
                ("hero-dark", ASSETS / "hero-dark.svg", "dark"),
            ):
                for width, height in ((1366, 900), (390, 844)):
                    context = browser.new_context(viewport={"width": width, "height": height},
                                                  color_scheme=scheme, reduced_motion="reduce")
                    # local-file assets only: network usage must not silently make the page render.
                    context.route("http://**/*", lambda route: route.abort())
                    context.route("https://**/*", lambda route: route.abort())
                    page = context.new_page()
                    page.goto(target.resolve().as_uri(), wait_until="load")
                    # DevTools capture avoids Playwright's font-stability wait on file:// SVG.
                    session = context.new_cdp_session(page)
                    captured = session.send("Page.captureScreenshot", {"format": "png", "fromSurface": True, "captureBeyondViewport": False})
                    (output / f"{name}-{width}.png").write_bytes(base64.b64decode(captured["data"]))
                    session.detach()
                    metric = page.evaluate("""() => ({
                        width: window.innerWidth,
                        scrollWidth: document.documentElement.scrollWidth,
                        visibleText: document.body ? document.body.innerText : document.documentElement.textContent,
                        links: [...document.querySelectorAll('nav a')].map(a => ({href:a.getAttribute('href'), text:a.innerText})),
                        nodes: document.querySelectorAll('svg .node, svg .focus, [data-node-id]').length,
                        edges: document.querySelectorAll('svg .edge, [data-edge-id]').length,
                        ariaSvg: [...document.querySelectorAll('svg')].map(x=>({role:x.getAttribute('role'), title:x.querySelector('title')?.textContent, desc:x.querySelector('desc')?.textContent})),
                        colors: [...document.querySelectorAll('svg .node, svg .focus')].slice(0,1).map(x=>getComputedStyle(x).fill)
                    })""")
                    if metric["scrollWidth"] > width + 1:
                        raise RuntimeError(f"{name}@{width}: document overflow {metric['scrollWidth']}>{width}")
                    if metric["ariaSvg"] and any(not x["title"] or not x["desc"] for x in metric["ariaSvg"]):
                        raise RuntimeError(f"{name}@{width}: missing SVG accessible title/desc")
                    if name.startswith("pilot"):
                        if metric["nodes"] != 6 or metric["edges"] != 6:
                            raise RuntimeError(f"{name}@{width}: unexpected node/edge count")
                        if "planned truth" not in metric["visibleText"] or "Skill Registry" not in metric["visibleText"]:
                            raise RuntimeError(f"{name}@{width}: missing planned provenance or source label")
                        if name == "pilot-light" and width == 1366:
                            page.keyboard.press("Tab")
                            focused = page.evaluate("() => document.activeElement?.tagName")
                            if focused != "A":
                                raise RuntimeError(f"keyboard Tab did not focus navigation link: {focused}")
                            metric["keyboardFirstTab"] = focused
                            if source == ORIGINAL:
                                from urllib.parse import unquote
                                for link in metric["links"]:
                                    href = link["href"].split("#", 1)[0]
                                    if not (target.parent / unquote(href)).resolve().is_file():
                                        raise RuntimeError(f"missing promoted navigation target: {href}")
                                page.locator("nav a").first.click()
                                if "Diagram Atlas" not in page.title():
                                    raise RuntimeError("promoted Atlas navigation did not open")
                                page.go_back(wait_until="load")
                                metric["actualFileNavigation"] = "PASS"
                        # Fixture links remain based on the promoted original path, not this preview folder.
                        metric["linksArePreviewRelative"] = (source != ORIGINAL)
                    if name.startswith("specimen") and metric["nodes"] != 5:
                        raise RuntimeError(f"{name}@{width}: semantic specimen node count changed")
                    if name in ("pilot-light", "pilot-dark", "specimen-light", "specimen-dark") and width == 1366:
                        zoom = context.new_cdp_session(page)
                        zoom.send("Emulation.setPageScaleFactor", {"pageScaleFactor": 2.0})
                        scale = page.evaluate("() => window.visualViewport.scale")
                        if abs(scale - 2.0) > 0.05:
                            raise RuntimeError(f"{name}: 200% compositor zoom did not apply: {scale}")
                        enlarged = zoom.send("Page.captureScreenshot",
                                             {"format":"png","fromSurface":True,"captureBeyondViewport":False})
                        (output / f"{name}-cdp-zoom200.png").write_bytes(base64.b64decode(enlarged["data"]))
                        metric["compositorPinchZoom200"] = {"visualViewportScale": scale,
                                                            "nativeBrowserCtrlPlus": "NOT_TESTED"}
                        zoom.detach()
                    results.append({"variant": name, "viewport": [width, height],
                                    "page": str(target.relative_to(ROOT)), "metrics": metric,
                                    "browser": browser.version,
                                    "visual_review": "unreviewed_screenshot_captured",
                                    "native_zoom_200": "not_tested",
                                    "github_markdown_render": "not_tested"})
                    context.close()
            github_checks = []
            # Test *actual GitHub README rendering* separately from offline assets.
            # This intentionally does not turn a network failure into a false PASS.
            for scheme in ("light", "dark"):
                public = browser.new_context(viewport={"width": 1366, "height": 900},
                                             color_scheme=scheme, reduced_motion="reduce")
                try:
                    tab = public.new_page()
                    tab.goto("https://github.com/sonhoang23/product-pro-max-skills",
                             wait_until="domcontentloaded", timeout=20000)
                    img = tab.locator('img[alt*="Product Pro Max Skills"]').first
                    img.wait_for(state="visible", timeout=12000)
                    img.scroll_into_view_if_needed()
                    img.evaluate("""node => new Promise((resolve,reject) => {
                      if(node.complete) return node.naturalWidth ? resolve() : reject(Error('image failed'));
                      node.addEventListener('load', resolve, {once:true});
                      node.addEventListener('error', () => reject(Error('image failed')), {once:true});
                    })""", timeout=18000)
                    info = img.evaluate("node=>({url:node.currentSrc,width:node.naturalWidth,alt:node.alt})")
                    if f"hero-{scheme}.svg" not in info["url"] or not info["width"]:
                        raise RuntimeError(f"GitHub hero wrong skin/asset: {info}")
                    ss = public.new_cdp_session(tab)
                    saved = ss.send("Page.captureScreenshot",
                                    {"format":"png","fromSurface":True,"captureBeyondViewport":False})
                    (output / f"github-{scheme}.png").write_bytes(base64.b64decode(saved["data"]))
                    ss.detach()
                    github_checks.append({"scheme":scheme,"status":"PASS","image":info})
                except Exception as exc:
                    github_checks.append({"scheme":scheme,"status":"NOT_VERIFIED",
                                          "detail":str(exc)[:400]})
                finally:
                    public.close()
            (output / "github-render.json").write_text(
                json.dumps(github_checks, ensure_ascii=False, indent=2), encoding="utf-8")
        finally:
            browser.close()
    (output / "metrics.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results


def main() -> int:
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("--output", type=Path, default=ROOT / ".tmp-spec003-browser")
    arg.add_argument("--promoted", action="store_true", help="Use migrated original after approval")
    args = arg.parse_args()
    records = run(args.output, ORIGINAL if args.promoted else CANDIDATE)
    print(f"PASS: Chromium {records[0]['browser']} captured {len(records)} static surfaces; "
          "native 200% zoom and GitHub site rendering NOT tested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
