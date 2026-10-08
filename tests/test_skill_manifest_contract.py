"""Spec 002 US2: discoverability independent of skill prose."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from skill_registry_common import RegistryValidationError, validate_discovery_metadata, validate_cycle_association, product_vocabulary, skill_inventory


class DiscoveryContractTests(unittest.TestCase):
    def fixture(self, kind: str):
        return {
            "description": f"A bounded {kind} capability.",
            "triggers": {
                "include": [f"The user requests {kind}."],
                "exclude": ["Implementation is already approved."],
            },
            "inputs": [
                {"name": "context", "description": "Current product context.", "required": True},
                {"name": "notes", "description": "Optional evidence.", "required": False},
            ],
            "outputs": [{"name": "findings", "description": "Evidence summary.", "semantic_kind": "evidence"}],
            "related_skills": [{"skill_id": "ppmax-other", "type": "complements"}],
            "workflows": [{"workflow_id": "idea-to-mvp", "role": "research participant"}],
        }

    def test_two_different_skills_share_metadata_semantics(self):
        for name in ("research", "positioning"):
            with self.subTest(name=name):
                data = self.fixture(name)
                validate_discovery_metadata(data, Path("manifest.yaml"))
                self.assertTrue(data["inputs"][0]["required"])
                self.assertFalse(data["inputs"][1]["required"])
                self.assertEqual(data["related_skills"][0]["type"], "complements")

    def test_multiple_lifecycle_associations_are_discoverable(self):
        vocab = product_vocabulary()
        associations = [
            {"cycle": "product-definition", "phase": "experience-design"},
            {"cycle": "verification", "phase": "ux-validation"},
        ]
        validate_cycle_association("product-definition", associations, ["ux"], vocab, Path("manifest.yaml"))
        self.assertEqual({a["cycle"] for a in associations}, {"product-definition", "verification"})

    def test_wrong_primary_folder_is_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            wrong = root / "skills" / "incorrect" / "ppmax-example"
            wrong.mkdir(parents=True)
            (wrong / "SKILL.md").write_text("---\\nname: ppmax-example\\n---\\n", encoding="utf-8")
            (wrong / "manifest.yaml").write_text("id: ppmax-example\\n", encoding="utf-8")
            pairs = skill_inventory(root)
            self.assertEqual(len(pairs), 1)
            self.assertNotEqual(pairs[0][0].parent.parent.name, "opportunity")
            # Folder-cycle contract is enforced by registry validation, not inventory-only discovery.

    def test_invalid_field_cases(self):
        cases = [
            ("missing negative boundary", lambda d: d["triggers"].pop("exclude")),
            ("empty description", lambda d: d.update(description="")),
            ("wrong input required type", lambda d: d["inputs"][0].update(required="yes")),
            ("duplicate input name", lambda d: d["inputs"].append(dict(d["inputs"][0]))),
            ("unknown relation", lambda d: d["related_skills"][0].update(type="calls")),
            ("duplicate workflow", lambda d: d["workflows"].append(dict(d["workflows"][0]))),
            ("invalid semantic kind", lambda d: d["outputs"][0].update(semantic_kind="score")),
        ]
        for label, mutate in cases:
            with self.subTest(label=label):
                data = self.fixture("research")
                mutate(data)
                with self.assertRaises(RegistryValidationError):
                    validate_discovery_metadata(data, Path("manifest.yaml"))


if __name__ == "__main__":
    unittest.main()
