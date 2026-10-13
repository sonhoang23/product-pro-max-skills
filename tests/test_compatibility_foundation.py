"""Spec 004 Phase 2: fail-closed supported baseline foundation.

Run: python -m unittest discover -s tests -p 'test_compatibility_foundation.py' -v
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from compatibility_common import (  # noqa: E402
    CompatibilityValidationError, ImmutableSource, SupportedBaseline,
    load_supported_baselines, normalized_relative_path, verify_local_baseline_source
)

ROOT = Path(__file__).resolve().parents[1]


class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ledger = self.root / "ledger.json"

    def write_ledger(self, entries=None, **overrides):
        payload = {"ledger_version": 1, "policy_ref": "VERSIONING.md",
                   "baselines": entries if entries is not None else []}
        payload.update(overrides)
        self.ledger.write_text(json.dumps(payload), encoding="utf-8")
        return self.ledger

    def valid_entry(self):
        return {
            "baseline_id": "model-v1", "component_id": "product-model",
            "version": "1.0.0", "source": {
                "ref": "fixture-base", "commit_sha": "a" * 40,
                "authority_path": "model/product-model.json",
                "sha256": "b" * 64,
            },
            "support_status": "active", "support_scope": ["fixture:strict-reader"],
            "support_policy_ref": "VERSIONING.md", "release_evidence": None
        }

    def test_empty_real_repo_ledger_is_not_published_evidence(self):
        parsed = load_supported_baselines(ROOT / "compatibility" / "supported-baselines.json")
        self.assertEqual(parsed.ledger_version, 1)
        self.assertEqual(parsed.baselines, ())
        self.assertEqual(parsed.policy_ref, "VERSIONING.md")

    def test_missing_and_invalid_json_fail_closed(self):
        with self.assertRaisesRegex(CompatibilityValidationError, "cannot read ledger"):
            load_supported_baselines(self.ledger)
        self.ledger.write_text("{not-json", encoding="utf-8")
        with self.assertRaisesRegex(CompatibilityValidationError, "cannot read ledger"):
            load_supported_baselines(self.ledger)

    def test_duplicate_json_keys_rejected(self):
        self.ledger.write_text(
            '{"ledger_version":1,"policy_ref":"VERSIONING.md","baselines":[],"baselines":[]}',
            encoding="utf-8")
        with self.assertRaisesRegex(CompatibilityValidationError, "duplicate key"):
            load_supported_baselines(self.ledger)

    def test_unknown_root_and_baseline_keys_rejected(self):
        self.write_ledger(unexpected="silent-drift")
        with self.assertRaisesRegex(CompatibilityValidationError, "unknown keys"):
            load_supported_baselines(self.ledger)
        entry = self.valid_entry()
        entry["unsupported_magic"] = True
        self.write_ledger([entry])
        with self.assertRaisesRegex(CompatibilityValidationError, "unknown keys"):
            load_supported_baselines(self.ledger)

    def test_duplicate_baselines_rejected(self):
        row = self.valid_entry()
        self.write_ledger([row, dict(row)])
        with self.assertRaisesRegex(CompatibilityValidationError, "duplicate baseline_id"):
            load_supported_baselines(self.ledger)

    def test_wrong_sha_and_semver_rejected(self):
        row = self.valid_entry()
        row["source"]["sha256"] = "invalid"
        self.write_ledger([row])
        with self.assertRaisesRegex(CompatibilityValidationError, "SHA-256"):
            load_supported_baselines(self.ledger)
        row = self.valid_entry()
        row["version"] = "1.0"
        self.write_ledger([row])
        with self.assertRaisesRegex(CompatibilityValidationError, "SemVer"):
            load_supported_baselines(self.ledger)

    def test_paths_normalized_and_traversal_denied(self):
        self.assertEqual(normalized_relative_path(r"model\product-model.json"),
                         "model/product-model.json")
        for bad in ("../secret", "models/../other.json", "/etc/passwd",
                    r"C:\Windows\system.ini", r"\\server\share", "a//b", "./a"):
            with self.subTest(path=bad), self.assertRaises(CompatibilityValidationError):
                normalized_relative_path(bad)

    def test_source_path_traversal_rejected_when_loading(self):
        row = self.valid_entry()
        row["source"]["authority_path"] = "model/../../outside.json"
        self.write_ledger([row])
        with self.assertRaisesRegex(CompatibilityValidationError, "parent path segment"):
            load_supported_baselines(self.ledger)

    def test_source_missing_ref_is_not_verified(self):
        row = self.valid_entry()
        self.write_ledger([row])
        parsed = load_supported_baselines(self.ledger)
        with self.assertRaisesRegex(CompatibilityValidationError, "git local source lookup failed"):
            verify_local_baseline_source(parsed.baselines[0], self.root)

    def test_pinned_git_ref_and_blob_are_verified_offline(self):
        git = lambda *args: subprocess.run(
            ["git", "-C", str(self.root), *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        ).stdout.decode("utf-8").strip()
        git("init", "-q")
        git("config", "user.email", "fixture@invalid.example")
        git("config", "user.name", "Fixture")
        (self.root / "model").mkdir()
        path = self.root / "model" / "product-model.json"
        content = b'{"model_version":"1.0.0"}\n'
        path.write_bytes(content)
        git("add", "model/product-model.json")
        git("commit", "-qm", "fixture")
        sha = git("rev-parse", "HEAD")
        git("tag", "fixture-base")
        row = self.valid_entry()
        row["source"]["commit_sha"] = sha
        row["source"]["sha256"] = hashlib.sha256(content).hexdigest()
        self.write_ledger([row])
        source = load_supported_baselines(self.ledger).baselines[0]
        self.assertEqual(verify_local_baseline_source(source, self.root), row["source"]["sha256"])

        # A mutable ref moved to another commit cannot retain a stale PASS.
        path.write_text('{"model_version":"2.0.0"}\n', encoding="utf-8")
        git("add", "model/product-model.json")
        git("commit", "-qm", "next")
        git("tag", "-f", "fixture-base")
        with self.assertRaisesRegex(CompatibilityValidationError, "stale ref"):
            verify_local_baseline_source(source, self.root)


if __name__ == "__main__":
    unittest.main()
