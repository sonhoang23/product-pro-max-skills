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


class MigrationCLIIntegrationTests(unittest.TestCase):
    def setUp(self):
        import migrate_project_contract as migration
        self.migration = migration
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "project.yaml"
        self.output = self.root / "new.yaml"
        self.backup = self.root / "project.backup"
        self.receipt = self.root / "receipt.json"
        self.legacy = (
            "project: demo\ncycle: opportunity\nphase: discovery\nstatus: active\n"
            "updated_at: now\ncritical_assumptions:\n  - needs-validation\n"
            "evidence:\n  - id: e1\n    origin: user\n    confirmed: false\n"
            "decision_history:\n  - id: d1\n    gate: warn\n    decision: research\n"
            "provenance:\n  source: user\n"
        )
        self.source.write_text(self.legacy, encoding="utf-8")

    def details(self, *, in_place=False):
        return self.migration.preflight(
            self.source, self.source if in_place else self.output,
            action="apply", backup_path=self.backup, receipt_path=self.receipt,
            accept_legacy=True, in_place=in_place)

    def test_default_dry_run_and_assess_do_not_write(self):
        from contextlib import redirect_stdout
        from io import StringIO
        before = self.source.read_bytes()
        for action in ("dry-run", "assess"):
            with self.subTest(action=action):
                buffer = StringIO()
                argv = ["--input", str(self.source), "--output", str(self.output)]
                if action == "assess":
                    argv.insert(0, action)
                with redirect_stdout(buffer):
                    self.assertEqual(self.migration.main(argv), 0)
                result = json.loads(buffer.getvalue())
                self.assertFalse(result["write_performed"])
                self.assertEqual(result["status"], "review_required")
                self.assertEqual(self.source.read_bytes(), before)
                self.assertFalse(self.output.exists())
                self.assertFalse(self.backup.exists())
                self.assertFalse(self.receipt.exists())

    def test_apply_requires_explicit_legacy_acceptance_and_distinct_output(self):
        details = self.migration.preflight(
            self.source, self.output, action="apply", backup_path=self.backup,
            receipt_path=self.receipt, accept_legacy=False, in_place=False)
        with self.assertRaisesRegex(ValueError, "accept-legacy"):
            self.migration.apply(details)
        with self.assertRaisesRegex(ValueError, "in-place"):
            self.migration.preflight(
                self.source, self.source, action="apply", backup_path=self.backup,
                receipt_path=self.receipt, accept_legacy=True, in_place=False)
        with self.assertRaisesRegex(ValueError, "requires explicit"):
            self.migration.preflight(
                self.source, self.output, action="apply", backup_path=None,
                receipt_path=None, accept_legacy=True, in_place=False)
        self.assertEqual(self.source.read_text(), self.legacy)

    def test_transaction_retains_history_and_rerun_does_not_duplicate(self):
        details = self.details()
        applied = self.migration.apply(details)
        self.assertEqual(applied["status"], "applied")
        self.assertEqual(applied["checkpoint"], "receipt_saved")
        self.assertEqual(self.backup.read_text(), self.legacy)
        self.assertEqual(self.source.read_text(), self.legacy)
        self.assertEqual(self.migration.digest(self.output.read_bytes()), applied["output_digest"])
        import yaml
        original = yaml.safe_load(self.legacy)
        migrated = yaml.safe_load(self.output.read_text(encoding="utf-8"))
        self.assertEqual(migrated["contract_version"], "1.0.0")
        for key in original:
            self.assertEqual(migrated[key], original[key])
        self.assertEqual(set(migrated) - set(original), {"contract_version"})
        before_output, before_receipt = self.output.read_bytes(), self.receipt.read_bytes()
        retried = self.migration.apply(self.details())
        self.assertEqual(retried["status"], "already_applied")
        self.assertEqual(self.output.read_bytes(), before_output)
        self.assertEqual(self.receipt.read_bytes(), before_receipt)

    def test_in_place_requires_flag_and_restores_history_on_explicit_recovery(self):
        from unittest.mock import patch
        details = self.details(in_place=True)
        normal_load = self.migration._load_source
        def interrupted(path):
            if Path(path) == self.source and self.source.read_text().startswith("project:") and \
                    "contract_version" in self.source.read_text():
                raise RuntimeError("injected post-replace crash")
            return normal_load(path)
        with patch.object(self.migration, "_load_source", side_effect=interrupted):
            with self.assertRaisesRegex(ValueError, "output_replaced"):
                self.migration.apply(details)
        failure = json.loads(self.receipt.read_text())
        self.assertEqual(failure["status"], "partially_applied")
        self.assertEqual(failure["checkpoint"], "output_replaced")
        self.assertEqual(self.backup.read_text(), self.legacy)
        current_sha = self.migration.digest(self.source.read_bytes())
        with self.assertRaisesRegex(ValueError, "restore target changed"):
            self.migration.restore(self.source, self.receipt, self.backup, "a" * 64)
        restored = self.migration.restore(self.source, self.receipt, self.backup, current_sha)
        self.assertEqual(restored["status"], "recovered")
        self.assertEqual(self.source.read_text(), self.legacy)
        self.assertEqual(json.loads(self.receipt.read_text())["status"], "recovered")

    def test_failed_backup_or_atomic_output_write_preserves_source(self):
        from unittest.mock import patch
        details = self.details()
        original_atomic = self.migration._atomic_new
        def fail_before_output(path, payload, **kw):
            if Path(path) == self.output:
                raise OSError("injected interrupted output")
            return original_atomic(path, payload, **kw)
        with patch.object(self.migration, "_atomic_new", side_effect=fail_before_output):
            with self.assertRaisesRegex(ValueError, "backup_saved"):
                self.migration.apply(details)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.source.read_text(), self.legacy)
        self.assertEqual(self.backup.read_text(), self.legacy)
        self.assertEqual(json.loads(self.receipt.read_text())["status"], "failed")
        with self.assertRaisesRegex(ValueError, "recover manually"):
            self.migration.apply(details)

    def test_detect_changed_source_and_output_and_already_versioned_without_receipt(self):
        details = self.details()
        self.source.write_text(self.legacy + "open_risks:\n  - unexpected\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed after preflight"):
            self.migration.apply(details)
        self.assertFalse(self.backup.exists())
        self.source.write_text(self.legacy, encoding="utf-8")
        applied = self.migration.apply(self.details())
        self.output.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "output/backup changed"):
            self.migration.apply(self.details())
        self.assertEqual(applied["status"], "applied")

    def test_unsupported_malformed_missing_and_out_of_order_fail_closed(self):
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "missing migration input"):
            self.details()
        self.source.write_text(self.legacy + "contract_version: 0.9.0\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsupported source contract_version"):
            self.details()
        self.source.write_text(self.legacy + "project: duplicated\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.details()
        self.source.write_text(self.legacy.replace("phase: discovery", "phase: invalid"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "noncanonical cycle/phase"):
            self.details()

    def test_json_input_preserves_original_records_and_rejects_duplicate_keys(self):
        self.source = self.root / "project.json"
        data = {"project": "demo", "cycle": "opportunity", "phase": "discovery",
                "status": "active", "updated_at": "now",
                "evidence": [{"source": "user", "type": "assumption"}],
                "decision_history": [{"gate": "fail", "decision": "revise"}]}
        self.source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.output = self.root / "out.json"
        receipt = self.migration.apply(self.details())
        updated = json.loads(self.output.read_text())
        self.assertEqual(receipt["status"], "applied")
        self.assertEqual(updated["decision_history"], data["decision_history"])
        self.assertEqual(updated["evidence"], data["evidence"])
        self.source.write_text('{"project":"one","project":"two"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.details()

    def test_prevents_symlink_redirect_and_output_collision(self):
        self.output.write_text("external", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.migration.apply(self.details())
        self.output.unlink()
        if hasattr(self.source, "symlink_to"):
            link = self.root / "link.yaml"
            try:
                link.symlink_to(self.source)
            except (NotImplementedError, OSError):
                return
            with self.assertRaisesRegex(ValueError, "symlink"):
                self.migration.preflight(
                    link, self.output, action="apply", backup_path=self.backup,
                    receipt_path=self.receipt, accept_legacy=True, in_place=False)


if __name__ == "__main__":
    unittest.main()
