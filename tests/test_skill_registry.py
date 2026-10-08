"""US1 deterministic registry and non-mutating validation tests.

Run: python -m unittest discover -s tests -p 'test_skill_registry.py' -v
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_skill_registry import build_registry, run
from skill_registry_common import RegistryValidationError


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "model").mkdir()
        (self.root / "skills" / "opportunity" / "ppmax-example").mkdir(parents=True)
        (self.root / "workflows" / "discovery").mkdir(parents=True)
        (self.root / "model" / "product-model.json").write_text(json.dumps({
            "lifecycle": {"cycles": [{"id": "opportunity", "phases": [{"id": "discovery"}]}]},
            "tracks": [{"id": "research"}],
            "gates": [{"id": "pass"}],
            "decisions": [{"id": "continue"}]
        }), encoding="utf-8")
        (self.root / "workflows" / "discovery" / "workflow.yaml").write_text("name: discovery\nsteps: []\n", encoding="utf-8")
        self.skill = self.root / "skills" / "opportunity" / "ppmax-example"
        (self.skill / "SKILL.md").write_text("---\nname: ppmax-example\ndescription: Example\n---\n\n# Example\n", encoding="utf-8")
        self.manifest = self.skill / "manifest.yaml"
        self.manifest.write_text("""id: ppmax-example
namespace: product-pro-max
slug: example
description: A bounded research capability.
primary_cycle: opportunity
lifecycle:
  - cycle: opportunity
    phase: discovery
tracks:
  - research
triggers:
  include: [Research a question.]
  exclude: [Do not implement.]
inputs:
  - name: question
    description: User question.
    required: true
outputs:
  - name: findings
    description: Supported findings.
    semantic_kind: evidence
related_skills: []
workflows:
  - workflow_id: discovery
    role: participant
""", encoding="utf-8")

    def test_generate_twice_identical_and_check_read_only(self):
        self.assertEqual(run("generate", self.root), 0)
        path = self.root / "registry" / "skills.json"
        before = path.read_bytes()
        self.assertEqual(run("generate", self.root), 0)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(run("check", self.root), 0)
        self.assertEqual(path.read_bytes(), before)
        payload = json.loads(before)
        self.assertEqual(payload["registry_version"], 1)
        self.assertEqual(payload["skills"][0]["id"], "ppmax-example")
        self.assertEqual(payload["skills"][0]["path"], "skills/opportunity/ppmax-example")

    def test_tampered_registry_rejected_without_modification(self):
        run("generate", self.root)
        path = self.root / "registry" / "skills.json"
        path.write_bytes(b"{}\n")
        with self.assertRaisesRegex(RegistryValidationError, "drift"):
            run("check", self.root)
        self.assertEqual(path.read_bytes(), b"{}\n")

    def test_duplicate_yaml_key_never_overwrites_registry(self):
        run("generate", self.root)
        path = self.root / "registry" / "skills.json"
        before = path.read_bytes()
        with self.manifest.open("a", encoding="utf-8") as stream:
            stream.write("id: ppmax-overwrite\n")
        with self.assertRaisesRegex(RegistryValidationError, "duplicate YAML key"):
            run("generate", self.root)
        self.assertEqual(path.read_bytes(), before)

    def test_legacy_path_blocks_empty_registry(self):
        (self.root / "skills" / "old-skill").mkdir()
        (self.root / "skills" / "old-skill" / "SKILL.md").write_text("---\nname: old-skill\n---\n", encoding="utf-8")
        with self.assertRaisesRegex(RegistryValidationError, "noncanonical"):
            build_registry(self.root)

    def test_development_skills_excluded(self):
        path = self.root / ".agents" / "skills" / "ppmax-lookalike"
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("not distributable", encoding="utf-8")
        payload = json.loads(build_registry(self.root))
        self.assertEqual(len(payload["skills"]), 1)


if __name__ == "__main__":
    unittest.main()
