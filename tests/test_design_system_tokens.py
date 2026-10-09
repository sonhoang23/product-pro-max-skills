"""Phase 2 token boundary tests: deterministic export, no-write drift, fail closed."""
from __future__ import annotations

import copy
import hashlib
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
from verify_design_system import TokenError, contrast, load_tokens, resolve, resolve_visual_state, validate
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

    def test_fixture_has_stable_semantic_inventory_and_all_state_roles(self):
        fixture = ROOT / "tests/fixtures/design-system/semantic-sample.json"
        sample = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(sample["provenance"]["truth"], "planned")
        self.assertEqual(sample["provenance"]["scope"], "feature")
        node_ids = [node["id"] for node in sample["nodes"]]
        self.assertEqual(len(set(node_ids)), len(node_ids))
        self.assertEqual({node["visual_state"]["role"] for node in sample["nodes"]},
                         {"success", "warning", "danger", "neutral"})
        for node in sample["nodes"]:
            self.assertTrue(node["label"] and node["visible_type"])
            for theme in ("light", "dark"):
                state = node["visual_state"]
                color = resolve_visual_state(self.data, theme, state["role"], state["label"])
                self.assertRegex(color, r"^#[0-9A-Fa-f]{6}$")
        for edge in sample["edges"]:
            self.assertIn(edge["source"], node_ids)
            self.assertIn(edge["target"], node_ids)
        self.assertNotIn(("gate-result", "decision-selected"),
                         [(edge["source"], edge["target"]) for edge in sample["edges"]])

    def test_unknown_visual_state_rejected_not_guessed(self):
        with self.assertRaisesRegex(TokenError, "unresolved"):
            resolve_visual_state(self.data, "light", "pass", "Passed")
        with self.assertRaisesRegex(TokenError, "unresolved"):
            resolve_visual_state(self.data, "dark", "pending-magic", "Pending")

    def test_missing_visual_state_label_rejected(self):
        for label in ("", "  ", None):
            with self.subTest(label=label), self.assertRaisesRegex(TokenError, "required visible label missing"):
                resolve_visual_state(self.data, "light", "warning", label)

    def test_official_theme_contrast_and_density_font_floors(self):
        self.assertIs(validate(self.data), self.data)
        for theme in ("light", "dark"):
            palette = self.data["themes"][theme]
            for role in ("text-primary", "text-secondary", "link"):
                self.assertGreaterEqual(contrast(palette[role], palette["surface"]), 4.5)
            for role in ("warning", "danger", "success", "focus-ring", "node-outline"):
                bg = "node-fill" if role == "node-outline" else "surface"
                self.assertGreaterEqual(contrast(palette[role], palette[bg]), 3)
        for density, multipliers in self.data["densities"].items():
            for name in ("body", "label", "caption"):
                self.assertGreaterEqual(self.data["typography"]["size_px"][name] * multipliers["type_multiplier"], 14, density)
        for role in ("ui", "mono"):
            self.assertIn(self.data["typography"][role][-1], ("sans-serif", "monospace", "serif"))

    def test_tampered_official_theme_contrast_rejected(self):
        self.data["themes"]["dark"]["text-secondary"] = self.data["themes"]["dark"]["surface"]
        with self.assertRaisesRegex(TokenError, "contrast"):
            validate(self.data)

    def test_preview_is_presentation_only_and_does_not_mutate_semantic_source(self):
        fixture_path = ROOT / "tests/fixtures/design-system/semantic-sample.json"
        canonical_before = json.dumps(self.data, sort_keys=True)
        fixture_before = fixture_path.read_bytes()
        semantic_hash = hashlib.sha256(fixture_before).hexdigest()
        original = render(self.data, surface="diagram", theme="light")
        alternate = render(self.data, surface="diagram", theme="light", accent_preview="#35e2df")
        self.assertNotEqual(original, alternate)
        self.assertIn("--ppmax-accent-brand: #35E2DF;", alternate)
        self.assertNotEqual(original.splitlines()[0], alternate.splitlines()[0])
        self.assertEqual(json.dumps(self.data, sort_keys=True), canonical_before)
        self.assertEqual(hashlib.sha256(fixture_path.read_bytes()).hexdigest(), semantic_hash)
        sample = json.loads(fixture_before)
        self.assertEqual(next(n for n in sample["nodes"] if n["id"] == "gate-result")["value"], "warn")
        self.assertEqual(next(n for n in sample["nodes"] if n["id"] == "decision-selected")["value"], "REPEAT")

    def test_invalid_accent_preview_is_rejected(self):
        with self.assertRaisesRegex(TokenError, "accent-preview"):
            render(self.data, accent_preview="red;display:none")

    def test_all_three_official_snapshots_are_exact_and_readonly(self):
        fixtures = ROOT / "tests/fixtures/design-system/snapshots"
        cases = [
            ("default-dark.css", ["--surface", "readme", "--theme", "dark"]),
            ("light.css", ["--surface", "diagram", "--theme", "light"]),
            ("light-accent-preview.css", ["--surface", "diagram", "--theme", "light", "--accent-preview", "#35E2DF"]),
        ]
        for name, args in cases:
            with self.subTest(snapshot=name):
                file = fixtures / name
                original = file.read_bytes()
                proc = subprocess.run([sys.executable, str(ROOT / "scripts/export_design_tokens.py"),
                                       *args, "--output", str(file), "--check"], capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(file.read_bytes(), original)
                self.assertIn("fingerprint=", original.decode("utf-8").splitlines()[0])


if __name__ == "__main__":
    unittest.main()
