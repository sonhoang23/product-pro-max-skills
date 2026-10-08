"""Negative fixtures for the canonical registry integrity boundary (T021/T022).

These tests intentionally use temporary repositories and do not mutate main.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_skill_registry import build_registry, run
from skill_registry_common import RegistryValidationError
import test_skill_registry as fixture_module


class InvalidRegistryTests(unittest.TestCase):
    # Reuse fixture setup without inheriting and rerunning positive test methods.
    setUp = fixture_module.RegistryTest.setUp
    def test_bad_id(self):
        self.manifest.write_text(self.manifest.read_text().replace("id: ppmax-example", "id: wrong"), encoding="utf-8")
        with self.assertRaisesRegex(RegistryValidationError, "canonical skill ID"):
            build_registry(self.root)

    def test_bad_primary_cycle_and_path(self):
        self.manifest.write_text(self.manifest.read_text().replace("primary_cycle: opportunity", "primary_cycle: delivery"), encoding="utf-8")
        with self.assertRaises(RegistryValidationError):
            build_registry(self.root)

    def test_wrong_phase_ownership(self):
        self.manifest.write_text(self.manifest.read_text().replace("phase: discovery", "phase: not-owned"), encoding="utf-8")
        with self.assertRaisesRegex(RegistryValidationError, "does not belong"):
            build_registry(self.root)

    def test_unknown_track(self):
        self.manifest.write_text(self.manifest.read_text().replace("  - research", "  - invented"), encoding="utf-8")
        with self.assertRaisesRegex(RegistryValidationError, "unknown track"):
            build_registry(self.root)

    def test_broken_workflow(self):
        self.manifest.write_text(self.manifest.read_text().replace("workflow_id: discovery", "workflow_id: missing"), encoding="utf-8")
        with self.assertRaisesRegex(RegistryValidationError, "unknown workflow"):
            build_registry(self.root)

    def test_broken_related_skill(self):
        self.manifest.write_text(self.manifest.read_text().replace("related_skills: []", "related_skills:\n  - skill_id: ppmax-missing\n    type: prerequisite"), encoding="utf-8")
        with self.assertRaisesRegex(RegistryValidationError, "unresolved skill"):
            build_registry(self.root)

    def test_missing_manifest(self):
        self.manifest.unlink()
        with self.assertRaisesRegex(RegistryValidationError, "missing sibling manifest"):
            build_registry(self.root)

    def test_malformed_yaml_does_not_replace_registry(self):
        run("generate", self.root)
        target = self.root / "registry" / "skills.json"
        before = target.read_bytes()
        self.manifest.write_text("id: [unfinished\n", encoding="utf-8")
        with self.assertRaises(RegistryValidationError):
            run("generate", self.root)
        self.assertEqual(target.read_bytes(), before)

    def test_optional_semantic_kind(self):
        self.manifest.write_text(self.manifest.read_text().replace("    semantic_kind: evidence\n", ""), encoding="utf-8")
        self.assertEqual(json.loads(build_registry(self.root))["skills"][0]["outputs"][0]["name"], "findings")

    def test_check_drift_without_write(self):
        run("generate", self.root)
        target = self.root / "registry" / "skills.json"
        target.write_bytes(b"not-json")
        with self.assertRaisesRegex(RegistryValidationError, "drift"):
            run("check", self.root)
        self.assertEqual(target.read_bytes(), b"not-json")


if __name__ == "__main__":
    unittest.main()
