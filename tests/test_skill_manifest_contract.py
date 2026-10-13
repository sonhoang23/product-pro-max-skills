"""Spec 002 US2: discoverability independent of skill prose."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from skill_registry_common import RegistryValidationError, validate_discovery_metadata, validate_cycle_association, product_vocabulary
from generate_skill_registry import build_registry


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
        import json
        import shutil
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            model_path = root / "model" / "product-model.json"
            model_path.parent.mkdir(parents=True)
            shutil.copyfile(Path(__file__).resolve().parents[1] / "model" / "product-model.json", model_path)
            wrong = root / "skills" / "delivery" / "ppmax-example"
            wrong.mkdir(parents=True)
            (wrong / "SKILL.md").write_text("---\\nname: ppmax-example\\n---\\n", encoding="utf-8")
            manifest = {
                "id": "ppmax-example", "namespace": "product-pro-max",
                "slug": "example", "description": "Tests folder-cycle mismatch.",
                "primary_cycle": "opportunity",
                "lifecycle": [{"cycle": "opportunity", "phase": "discovery"}],
                "tracks": ["product"],
                "triggers": {"include": ["When testing."], "exclude": ["Otherwise."]},
                "inputs": [{"name": "context", "description": "Input.", "required": True}],
                "outputs": [{"name": "evidence", "description": "Output."}],
                "related_skills": [], "workflows": [],
            }
            (wrong / "manifest.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(RegistryValidationError, "primary_cycle mismatch"):
                build_registry(root)

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


class ManifestVersionRolloutTests(unittest.TestCase):
    """Exercise strict existing readers with legacy and versioned synthetic skills."""

    def setUp(self):
        import test_skill_registry
        test_skill_registry.RegistryTest.setUp(self)

    def test_unversioned_legacy_is_detected_without_inventing_version(self):
        from skill_registry_common import parse_yaml, validate_optional_manifest_version
        data = parse_yaml(self.manifest)
        self.assertIsNone(validate_optional_manifest_version(data, self.manifest))
        self.assertNotIn("version", build_registry(self.root).decode("utf-8"))

    def test_versioned_manifest_accepted_and_registry_stays_derived(self):
        from skill_registry_common import parse_yaml, validate_optional_manifest_version
        self.manifest.write_text(self.manifest.read_text(encoding="utf-8") + "version: 0.2.0\n", encoding="utf-8")
        self.assertEqual(validate_optional_manifest_version(parse_yaml(self.manifest), self.manifest), "0.2.0")
        import json
        skill = json.loads(build_registry(self.root))["skills"][0]
        self.assertEqual(skill["version"], "0.2.0")

    def test_invalid_version_and_unknown_field_fail_closed(self):
        for extra in ("version: 1.02.0\n", "version: true\n",
                      "version: 1.0.0\nversion: 2.0.0\n",
                      "random_unreviewed_field: yes\n",
                      "version: !!python/object/apply:os.system ['echo bad']\n"):
            with self.subTest(extra=extra):
                original = self.manifest.read_text(encoding="utf-8")
                self.manifest.write_text(original + extra, encoding="utf-8")
                with self.assertRaises(RegistryValidationError):
                    build_registry(self.root)
                self.manifest.write_text(original, encoding="utf-8")
