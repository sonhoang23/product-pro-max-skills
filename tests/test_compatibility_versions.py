"""Spec 004 US1: version/owner policy regression before a compatibility gate exists."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from compatibility_common import (
    CompatibilityValidationError, compare_semver, inspect_version_owner,
    minimum_version_increment, parse_semver, sufficient_version_increment,
)

ROOT = Path(__file__).resolve().parents[1]


class VersionPolicyTests(unittest.TestCase):
    def test_semver_rejects_malformed_and_leading_zero(self):
        for value in ("1.2", "01.2.3", "1.02.3", "1.2.03", "1.2.3-01",
                      "1.2.3-", "1.2.3+bad..build", "1.2.3.4", "v1.2.3",
                      "1.2.3-rc.01", "1.2.3-α", None, True):
            with self.subTest(value=value), self.assertRaises(CompatibilityValidationError):
                parse_semver(value)

    def test_semver_precedence_and_build_metadata(self):
        ordered = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta",
                   "1.0.0-beta", "1.0.0-beta.2", "1.0.0-beta.11",
                   "1.0.0-rc.1", "1.0.0"]
        for a, b in zip(ordered, ordered[1:]):
            with self.subTest(a=a, b=b):
                self.assertLess(compare_semver(a, b), 0)
                self.assertGreater(compare_semver(b, a), 0)
        self.assertEqual(compare_semver("1.2.3+build.1", "1.2.3+other"), 0)
        self.assertEqual(compare_semver("1.2.3", "1.2.3"), 0)

    def test_bump_matrix_stable_and_pre_one(self):
        cases = [
            ("1.2.3", "1.2.4", "fix", "patch", True),
            ("1.2.3", "1.3.0", "feature", "minor", True),
            ("1.2.3", "1.2.4", "feature", "minor", False),
            ("1.2.3", "2.0.0", "breaking", "major", True),
            ("1.2.3", "1.3.0", "breaking", "major", False),
            ("0.2.4", "0.3.0", "breaking", "minor", True),
            ("0.2.4", "0.2.5", "breaking", "minor", False),
            ("0.2.4", "1.0.0", "breaking", "minor", True),
            ("1.2.3", "1.2.3", "none", "none", True),
            ("1.2.3", "1.2.3+docs.1", "feature", "minor", False),
        ]
        for prior, proposed, impact, expected, allowed in cases:
            with self.subTest(prior=prior, proposed=proposed, impact=impact):
                self.assertEqual(minimum_version_increment(impact, prior), expected)
                self.assertEqual(sufficient_version_increment(prior, proposed, impact), allowed)

    def test_initial_unassessed_not_green(self):
        self.assertIsNone(minimum_version_increment("breaking", None))
        self.assertIsNone(sufficient_version_increment(None, "1.0.0", "feature"))
        with self.assertRaises(CompatibilityValidationError):
            minimum_version_increment("unclassified", "1.0.0")

    def test_model_owner_real_repo_and_no_inferred_publication(self):
        component = inspect_version_owner(ROOT, "product_model", "model/product-model.json")
        self.assertEqual(component.version, "1.0.0")
        self.assertEqual(component.component_id, "product-model")
        self.assertEqual(component.version_owner, "model_version")
        self.assertEqual(component.publication_status, "unknown")

    def test_synthetic_owner_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skills/example").mkdir(parents=True)
            (root / "workflows/example").mkdir(parents=True)
            (root / "schemas").mkdir()
            (root / "project").mkdir()
            manifest = root / "skills/example/manifest.yaml"
            manifest.write_text("id: ppmax-example\n", encoding="utf-8")
            (root / "skills/example/SKILL.md").write_text("# behavior\n", encoding="utf-8")
            (root / "workflows/example/workflow.yaml").write_text(
                "name: example\nversion: 2.3.0\nsteps: []\n", encoding="utf-8")
            (root / "schemas/test.schema.json").write_text(
                json.dumps({"$id": "https://example.test/schema"}), encoding="utf-8")
            (root / "project/state.yaml").write_text(
                "project: test\n", encoding="utf-8")
            legacy = inspect_version_owner(root, "skill", "skills/example/manifest.yaml")
            self.assertIsNone(legacy.version)
            self.assertEqual(legacy.authority_path, "skills/example/SKILL.md")
            manifest.write_text("id: ppmax-example\nversion: 0.2.0\n", encoding="utf-8")
            self.assertEqual(inspect_version_owner(
                root, "skill", "skills/example/manifest.yaml").version, "0.2.0")
            workflow = inspect_version_owner(root, "workflow", "workflows/example/workflow.yaml")
            self.assertEqual(workflow.version, "2.3.0")
            self.assertEqual(workflow.version_owner, "workflow.version")
            schema = inspect_version_owner(root, "machine_schema", "schemas/test.schema.json")
            self.assertIsNone(schema.version)
            self.assertEqual(schema.version_owner, "support-ledger.version")
            self.assertEqual(inspect_version_owner(
                root, "machine_schema", "schemas/test.schema.json",
                declared_schema_version="1.5.0").version, "1.5.0")
            old_project = inspect_version_owner(root, "project_data", "project/state.yaml")
            self.assertIsNone(old_project.version)
            self.assertEqual(old_project.version_owner, "contract_version")
            (root / "project/state.yaml").write_text(
                "project: test\ncontract_version: 1.0.0\n", encoding="utf-8")
            self.assertEqual(inspect_version_owner(
                root, "project_data", "project/state.yaml").version, "1.0.0")

    def test_unrelated_registry_lock_and_docs_are_not_versions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "model").mkdir()
            (root / "model/product-model.json").write_text(
                '{"model_version":"1.0.0"}\n', encoding="utf-8")
            first = inspect_version_owner(root, "product_model", "model/product-model.json")
            (root / "registry").mkdir()
            (root / "registry/skills.json").write_text(
                '{"registry_version":100,"skills":[]}\n', encoding="utf-8")
            (root / "skills-lock.json").write_text('{"version":99}', encoding="utf-8")
            (root / "README.md").write_text("# docs only", encoding="utf-8")
            second = inspect_version_owner(root, "product_model", "model/product-model.json")
            self.assertEqual(first.version, second.version)
            self.assertEqual(first.digest, second.digest)


if __name__ == "__main__":
    unittest.main()
