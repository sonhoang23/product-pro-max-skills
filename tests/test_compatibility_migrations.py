"""Spec 004 Phase 5: durable project state schema and safe migration contract."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compatibility_common import inspect_version_owner  # noqa: E402


class ProjectStateContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads((ROOT / "schemas/project-state.schema.json").read_text(encoding="utf-8"))
        self.migration_schema = json.loads((ROOT / "schemas/compatibility-migration.schema.json").read_text(encoding="utf-8"))

    def test_schema_accepts_legacy_unversioned_contract_by_design(self):
        self.assertNotIn("contract_version", self.schema["required"])
        self.assertEqual(self.schema["properties"]["contract_version"]["type"], "string")
        self.assertTrue(self.schema["additionalProperties"])

    def test_new_project_template_has_explicit_contract_version(self):
        template = (ROOT / "templates/project-state/project.yaml").read_text(encoding="utf-8")
        self.assertIn("contract_version: 1.0.0\n", template)
        self.assertNotIn("stage:", template)
        self.assertIn("cycle: opportunity\n", template)

    def test_legacy_and_new_readers_do_not_modify_source(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            old = base / "legacy.yaml"
            new = base / "current.yaml"
            content = "project: demo\ncycle: opportunity\nphase: discovery\nstatus: active\nupdated_at: now\n"
            old.write_text(content, encoding="utf-8")
            new.write_text("contract_version: 1.0.0\n" + content, encoding="utf-8")
            self.assertIsNone(inspect_version_owner(base, "project_data", "legacy.yaml").version)
            self.assertEqual(inspect_version_owner(base, "project_data", "current.yaml").version, "1.0.0")
            self.assertEqual(old.read_text(encoding="utf-8"), content)

    def test_migration_receipt_has_states_and_required_provenance(self):
        props = self.migration_schema["properties"]
        for prop in ("migration_id", "source_version", "target_version", "input_digest",
                     "output_digest", "idempotency_key", "backup_path", "checkpoint",
                     "errors", "recovery_action"):
            self.assertIn(prop, props)
            self.assertIn(prop, self.migration_schema["required"])
        self.assertTrue({"applied", "already_applied", "partially_applied", "failed",
                         "recovered"}.issubset(props["status"]["enum"]))

    def test_mixed_versions_and_unrelated_decision_history_preserved_by_parsing(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            payload = {"project": "x", "contract_version": "1.0.0",
                       "decision_history": [{"id": "d1", "gate": "fail",
                                             "decision": "revise", "origin": "user"}]}
            for filename, version in (("legacy.json", None), ("current.json", "1.0.0")):
                item = copy.deepcopy(payload)
                if version is None:
                    item.pop("contract_version")
                (base / filename).write_text(json.dumps(item), encoding="utf-8")
                ref = inspect_version_owner(base, "project_data", filename)
                self.assertEqual(ref.version, version)
                self.assertEqual(json.loads((base / filename).read_text())["decision_history"],
                                 payload["decision_history"])


if __name__ == "__main__":
    unittest.main()
