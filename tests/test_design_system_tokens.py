"""Phase 2 token boundary tests: deterministic export, no-write drift, fail closed."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_design_system import TokenError, contrast, load_tokens, resolve, validate
from export_design_tokens import render


class DesignTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = load_tokens(ROOT)

    def setUp(self):
        self.data = copy.deepcopy(self.canonical)

    def test_complete_light_dark_role_contract(self):
        for surface in ("diagram", "docs", "readme", "brand"):
            theme, roles, density = resolve(self.data, surface, None, "default")
            self.assertEqual(theme, self.data["surfaces"][surface])
            self.assertIn("accent-brand", roles)
            self.assertEqual(density["type_multiplier"], 1)

    def test_revision_determinism_and_format(self):
        first = render(self.data)
        self.assertEqual(first, render(json.loads(json.dumps(self.data))))
        self.assertIn("revision=0.1.0", first)
        self.assertIn("fingerprint=", first)
        self.assertIn("--ppmax-accent-brand: #A3FF47;", first)
        self.assertIn("svg.ppmax-design-system", render(self.data, format="svg-css"))
        self.data["themes"]["dark"]["accent-brand"] = "#B3FF55"
        changed = render(self.data)
        self.assertNotEqual(first, changed)
        self.assertNotEqual(first.splitlines()[0], changed.splitlines()[0])

    def test_no_write_check_and_drift_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "design-system" / "tokens.json"
            path.parent.mkdir()
            path.write_text(json.dumps(self.data), encoding="utf-8")
            target = root / "render.css"
            cmd = [sys.executable, str(ROOT / "scripts/export_design_tokens.py"), "--root", str(root), "--output", str(target)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            before = target.read_bytes()
            self.assertEqual(subprocess.run(cmd + ["--check"], capture_output=True).returncode, 0)
            self.assertEqual(before, target.read_bytes())
            target.write_bytes(b"tampered")
            bad = subprocess.run(cmd + ["--check"], capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("drift", bad.stderr)
            self.assertEqual(target.read_bytes(), b"tampered")
            self.assertEqual(subprocess.run([sys.executable, str(ROOT / "scripts/export_design_tokens.py"),
                                             "--root", str(root), "--check"], capture_output=True).returncode, 0)

    def test_fails_closed_for_missing_repo_tokens_even_if_global_profile_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            (home / ".diagram-design").write_text("VibeToolPro user skin", encoding="utf-8")
            with patch.dict(os.environ, {"HOME": str(home)}):
                with self.assertRaisesRegex(TokenError, "repository-local tokens required"):
                    load_tokens(root)

    def test_global_profile_cannot_override_repo_theme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "design-system" / "tokens.json"
            path.parent.mkdir()
            path.write_text(json.dumps(self.data), encoding="utf-8")
            home = root / "home"
            home.mkdir()
            profile = home / ".diagram-design"
            profile.write_text("accent: #FF00FF", encoding="utf-8")
            with patch.dict(os.environ, {"HOME": str(home)}):
                resolved = load_tokens(root)
                self.assertEqual(resolved["themes"]["light"]["accent-brand"], "#A3FF47")
                self.assertEqual(profile.read_text(encoding="utf-8"), "accent: #FF00FF")

    def test_missing_and_unknown_role_rejected(self):
        self.data["themes"]["light"].pop("edge")
        with self.assertRaisesRegex(TokenError, "missing.*edge"):
            validate(self.data)
        self.data = copy.deepcopy(self.canonical)
        self.data["themes"]["dark"]["workflow-decision"] = "#000000"
        with self.assertRaisesRegex(TokenError, "unknown.*workflow-decision"):
            validate(self.data)

    def test_malformed_schema_and_color_rejected(self):
        for key, bad in (("revision", "v0.1.0"), ("schema_version", True)):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.data)
                candidate[key] = bad
                with self.assertRaises(TokenError):
                    validate(candidate)
        for color in ("red", "#GG0000", "url(https://attacker)", "#ffffff;display:none"):
            with self.subTest(color=color):
                candidate = copy.deepcopy(self.data)
                candidate["themes"]["dark"]["link"] = color
                with self.assertRaisesRegex(TokenError, "invalid CSS hex color"):
                    validate(candidate)

    def test_invalid_theme_density_and_surface_rejected(self):
        for values in (("diagram", "sepia", "default"), ("diagram", "light", "micro"),
                       ("unknown", "light", "default")):
            with self.subTest(values=values):
                with self.assertRaisesRegex(TokenError, "unsupported"):
                    resolve(self.data, *values)

    def test_contrast_and_small_font_fail(self):
        self.data["themes"]["light"]["text-primary"] = "#DDEEDD"
        with self.assertRaisesRegex(TokenError, "contrast"):
            validate(self.data)
        self.data = copy.deepcopy(self.canonical)
        self.data["densities"]["compact"]["type_multiplier"] = 0.5
        with self.assertRaisesRegex(TokenError, "below 14px floor"):
            validate(self.data)

    def test_font_css_injection_rejected(self):
        self.data["typography"]["ui"][0] = "Arial); color: red"
        with self.assertRaisesRegex(TokenError, "fallback fonts"):
            validate(self.data)

    def test_brand_accent_not_an_accessible_light_text_color(self):
        roles = self.data["themes"]["light"]
        self.assertLess(contrast(roles["accent-brand"], roles["surface"]), 4.5)
        self.assertGreaterEqual(contrast(roles["text-primary"], roles["surface"]), 4.5)


if __name__ == "__main__":
    unittest.main()
