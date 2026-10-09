"""Spec 003 final convergence gate: verify source/gate freshness and traceability.

This file intentionally does not replace browser, GitHub, or screen-reader QA.
Those dimensions are tracked independently in qa-evidence.md and workflow jobs.
"""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE = ROOT / "specs/003-product-pro-max-design-system"


def blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + bytes([0])
    return hashlib.sha1(header + data).hexdigest()


class Spec003Convergence(unittest.TestCase):
    def test_canonical_requirements_and_task_completion(self):
        spec = (FEATURE / "spec.md").read_text(encoding="utf-8")
        tasks = (FEATURE / "tasks.md").read_text(encoding="utf-8")
        fr = {int(i) for i in re.findall(r"\*\*FR-(\d{3})\*\*", spec)}
        sc = {int(i) for i in re.findall(r"\*\*SC-(\d{3})\*\*", spec)}
        checked = [int(i) for i in re.findall(r"^- \[x\] T(\d{3})\b", tasks, flags=re.M)]
        unchecked = re.findall(r"^- \[ \] T(\d{3})\b", tasks, flags=re.M)
        self.assertEqual(fr, set(range(1, 28)))
        self.assertEqual(sc, set(range(1, 8)))
        self.assertEqual(checked, list(range(1, 56)))
        self.assertFalse(unchecked, f"tasks not completed: {unchecked}")
        self.assertEqual({f"DS-R{i:02d}" for i in range(1, 10)},
                         set(re.findall(r"^\| (DS-R\d{2})\b", tasks, flags=re.M)))

    def test_modeling_gates_exist_and_all_recorded_sources_are_fresh(self):
        data = json.loads((FEATURE / ".modeling-state.json").read_text(encoding="utf-8"))
        gates = data["gates"]
        expected = ("spec", "plan", "tasks", "implementation:phase-02",
                    "implementation:phase-03", "implementation:phase-04",
                    "implementation:phase-05", "implementation:phase-06",
                    "implementation:phase-07", "converge")
        for key in expected:
            with self.subTest(gate=key):
                self.assertIn(key, gates)
                gate = gates[key]
                self.assertIn(gate["status"], ("modeled", "no-diagram-needed"))
                self.assertTrue(gate["source_hashes"])
                for path, expected_sha in gate["source_hashes"].items():
                    source = ROOT / path if (ROOT / path).is_file() else FEATURE / path
                    self.assertTrue(source.is_file(), f"{key}: source missing: {path}")
                    self.assertEqual(blob_sha(source.read_bytes()), expected_sha,
                                     f"{key}: stale source: {path}")
                for output in gate.get("outputs", []):
                    self.assertTrue((FEATURE / output).is_file(), f"{key}: missing diagram {output}")
        self.assertEqual(gates["converge"].get("outputs"), [])
        self.assertEqual(gates["converge"]["status"], "no-diagram-needed")

    def test_project_authority_and_presentation_revision_boundaries(self):
        feature = json.loads((ROOT / ".specify/feature.json").read_text(encoding="utf-8"))
        self.assertEqual(feature["feature_directory"],
                         "specs/003-product-pro-max-design-system")
        registry = json.loads((ROOT / "docs/diagrams/diagram-index.json").read_text(encoding="utf-8"))
        entry = next(x for x in registry["diagrams"]
                     if x["id"] == "feature-002-skill-metadata-relations")
        self.assertEqual((entry["truth"], entry["phase"]), ("planned", "spec"))
        tokens = json.loads((ROOT / "design-system/tokens.json").read_text(encoding="utf-8"))
        rev = tokens["revision"]
        for path in (
            "docs/diagrams/index.html",
            "specs/002-skill-manifest-registry/diagrams.html",
            "specs/003-product-pro-max-design-system/diagrams.html",
        ):
            with self.subTest(surface=path):
                value = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn(f'data-ppmax-token-revision="{rev}"', value)
                self.assertIn("prefers-color-scheme: dark", value)
        pilot = (ROOT / "specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html").read_text(encoding="utf-8")
        self.assertIn(f"revision={rev}", pilot)
        self.assertIn("fingerprint=", pilot)
        original = (ROOT / "tests/fixtures/design-system/pilot/original-spec002.html").read_text(encoding="utf-8")
        without_css = lambda s: re.sub(r"<style>[\s\S]*?</style>", "<style>unchanged</style>", s)
        self.assertEqual(without_css(pilot), without_css(original))


if __name__ == "__main__":
    unittest.main()
