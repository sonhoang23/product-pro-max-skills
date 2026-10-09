"""Spec 003 release safeguards: brand token source and reversible Spec 002 migration."""
from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export_brand_assets import render_assets
from migrate_design_system_pilot import BACKUP, ORIGINAL, PREVIEW, TEMPLATE, build, run, git_blob, replace_css
from verify_design_system import load_tokens, TokenError


class ReleaseDesignChecks(unittest.TestCase):
    def test_exported_brand_bytes_match_token_backed_source(self):
        expected = render_assets(ROOT)
        self.assertEqual(set(expected), {"signal-path.svg", "wordmark.svg", "hero-light.svg",
                                          "hero-dark.svg", "docs-specimen.svg", "social-cover.svg"})
        revision = load_tokens(ROOT)["revision"]
        for name, svg in expected.items():
            with self.subTest(name=name):
                self.assertEqual((ROOT / "assets/brand" / name).read_bytes(), svg.encode("utf-8"))
                root = ET.fromstring(svg)
                self.assertEqual(root.attrib["data-token-revision"], revision)
                self.assertIn("viewBox", root.attrib)
                self.assertEqual(root.attrib.get("role"), "img")
                self.assertTrue(any(el.tag.endswith("title") and el.text for el in root))
                self.assertTrue(any(el.tag.endswith("desc") and el.text for el in root))
                self.assertNotIn("<script", svg.lower())
                self.assertNotIn("<foreignObject", svg)
                self.assertNotIn("https://", svg)
                self.assertNotIn("@import", svg)
                self.assertNotIn("<image", svg.lower())

    def test_same_signal_path_mark_appears_on_every_brand_asset(self):
        for name, svg in render_assets(ROOT).items():
            with self.subTest(asset=name):
                root = ET.fromstring(svg)
                paths = [e.get("d") for e in root.iter() if e.tag.endswith("path")]
                self.assertIn("M7 47 L22 32 L34 37 L52 12", paths)

    def test_readmes_use_github_picture_variants_and_alt_fallback(self):
        for doc in ("README.md", "README.vi.md"):
            with self.subTest(doc=doc):
                content = (ROOT / doc).read_text(encoding="utf-8")
                self.assertIn("<picture>", content)
                self.assertIn("prefers-color-scheme: dark", content)
                self.assertIn("prefers-color-scheme: light", content)
                self.assertIn("./assets/brand/hero-dark.svg", content)
                self.assertIn("./assets/brand/hero-light.svg", content)
                self.assertIn('<img alt="Product Pro Max Skills', content)

    def test_brand_drift_check_never_writes(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            for rel in ("design-system/tokens.json", "design-system/brand-layouts.json"):
                target = tmp / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, target)
            for name in render_assets(ROOT):
                path = tmp / "assets/brand" / name
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / "assets/brand" / name, path)
            cmd = [sys.executable, str(ROOT / "scripts/export_brand_assets.py"),
                   "--root", str(tmp), "--check"]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            tampered = tmp / "assets/brand/hero-light.svg"
            tampered.write_bytes(b"tamper")
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(tampered.read_bytes(), b"tamper")

    def test_visual_migration_does_not_mutate_any_html_except_css(self):
        original, candidate = build(ROOT)
        self.assertEqual(git_blob(original.encode("utf-8")), "6acb098a4e8513d50527bfb615a6561bf3520e16")
        self.assertEqual((ROOT / PREVIEW).read_text(encoding="utf-8"), candidate)
        self.assertIn("revision=0.1.0 fingerprint=2e8e64f6edc41a3c", candidate)
        self.assertIn("themes=light,dark", candidate)
        import re
        trim = lambda s: re.sub(r"<style>[\s\S]*?</style>", "<style>STYLE</style>", s)
        self.assertEqual(trim(original), trim(candidate))
        for evidence in ('planned truth', 'skill-creator-vi', 'SKILL.md + manifest.yaml',
                         '../../../docs/diagrams/index.html', '../diagrams.html'):
            self.assertIn(evidence, original)
            self.assertIn(evidence, candidate)
        self.assertEqual(original.count('class="edge"'), candidate.count('class="edge"'))
        self.assertEqual(original.count('class="node"'), candidate.count('class="node"'))
        self.assertNotIn("script", candidate.split("<style>", 1)[0].lower())

    def test_migration_fails_closed_without_rewriting_source(self):
        baseline, candidate = build(ROOT)
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            for rel in ("design-system/tokens.json", TEMPLATE, BACKUP, PREVIEW, ORIGINAL):
                dst = temp / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if rel == PREVIEW:
                    dst.write_text(candidate, encoding="utf-8")
                else:
                    shutil.copy2(ROOT / rel, dst)
            target = temp / ORIGINAL
            target.write_text(baseline, encoding="utf-8")
            run(temp, "preview")
            self.assertEqual(target.read_text(encoding="utf-8"), baseline)
            run(temp, "promote")
            self.assertEqual(target.read_text(encoding="utf-8"), candidate)
            run(temp, "check")
            run(temp, "restore")
            self.assertEqual(target.read_text(encoding="utf-8"), baseline)
            target.write_text("concurrent update", encoding="utf-8")
            with self.assertRaises(TokenError):
                run(temp, "promote")
            self.assertEqual(target.read_text(encoding="utf-8"), "concurrent update")

    def test_atlas_semantic_registry_not_promoted_by_visual_skin(self):
        registry = json.loads((ROOT / "docs/diagrams/diagram-index.json").read_text(encoding="utf-8"))
        entries = [entry for entry in registry["diagrams"] if entry["id"] == "feature-002-skill-metadata-relations"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["truth"], "planned")
        self.assertEqual(entries[0]["phase"], "spec")
        self.assertEqual(entries[0]["path"], str(ORIGINAL).replace("\\", "/"))

    def test_navigation_atlas_and_ledgers_derive_light_dark_from_repo_tokens(self):
        from export_navigation_styles import SURFACES, render_html
        tokens = load_tokens(ROOT)
        for rel in SURFACES:
            with self.subTest(surface=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(text, render_html(text, tokens))
                self.assertIn('data-ppmax-token-revision="0.1.0"', text)
                self.assertIn("ppmax-navigation revision=0.1.0", text)
                self.assertIn("prefers-color-scheme: dark", text)
                self.assertIn(f'--ppmax-surface: {tokens["themes"]["light"]["surface"]}', text)
                self.assertIn(f'--ppmax-surface: {tokens["themes"]["dark"]["surface"]}', text)
                self.assertIn('href=', text)
                self.assertIn("planned", text.lower())



if __name__ == "__main__":
    unittest.main()
