"""Spec 004 US2: strict consumers, canonical diffs, dependency safety.

Pure offline fixtures; not released-provider, runtime or publication evidence.
Run: python -m unittest discover -s tests -p 'test_compatibility_consumers.py' -v
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from compatibility_common import (  # noqa: E402
    CompatibilityValidationError, ConsumerDependency, assess_consumer_impact,
    check_consumer_dependencies, enumerate_known_consumers,
    load_consumer_dependencies, semver_in_range
)

ROOT = Path(__file__).resolve().parents[1]


def consumer(cid="skill:reader", provider="skill:provider", *, strict=True,
             version_range="^1.0.0", outputs=()):
    return ConsumerDependency(
        consumer_id=cid, provider_component_id=provider,
        version_range=version_range, required_outputs=tuple(outputs),
        required_features=(), strict_reader=strict,
        declared_by="skills/reader/manifest.yaml", scope="fixture")


class ConsumerImpactTests(unittest.TestCase):
    def check(self, old, new, edges=(), *, kind="skill",
              reader_evidence=frozenset(), external=False):
        return assess_consumer_impact(
            old, new, "skill:provider" if kind != "product_model" else "product-model",
            "skills/provider/manifest.yaml" if kind != "product_model" else "model/product-model.json",
            tuple(edges), component_type=kind,
            reader_evidence=reader_evidence,
            unknown_external_consumers=external)

    def codes(self, outcome):
        return {finding.code for finding in outcome.findings}

    def test_known_tolerant_reader_needs_actual_proof(self):
        before = {"properties": {"a": {"type": "string"}}}
        after = {"properties": {"a": {"type": "string"}, "b": {"type": "string"}}}
        edge = consumer(strict=False)
        result = self.check(before, after, [edge])
        self.assertEqual(result.classification, "unassessed")
        self.assertIn("READER_TOLERANCE_UNVERIFIED", self.codes(result))
        verified = self.check(before, after, [edge], reader_evidence=frozenset({"skill:reader"}))
        self.assertEqual(verified.classification, "compatible")
        self.assertEqual(verified.covered_consumers, ("skill:reader",))

    def test_strict_reader_rejects_enum_and_optional_field(self):
        edge = consumer()
        original = {"properties": {"status": {"enum": ["pass", "fail"]}}}
        candidate = {"properties": {
            "status": {"enum": ["pass", "fail", "warn"]},
            "extra": {"type": "string"}}}
        result = self.check(original, candidate, [edge])
        self.assertEqual(result.classification, "breaking")
        self.assertIn("STRICT_READER_NEW_ENUM", self.codes(result))
        self.assertIn("STRICT_READER_NEW_FIELD", self.codes(result))
        self.assertTrue(all(f.authority_path == "skills/provider/manifest.yaml" for f in result.findings))
        self.assertTrue(all(f.required_action for f in result.findings))
        self.assertTrue(any(f.affected_consumer_ids == ("skill:reader",) for f in result.findings))

    def test_required_field_and_shape_regressions(self):
        old = {"required": ["a"], "properties": {"a": {"type": "string"}}}
        new = {"required": ["a", "b"], "properties": {
            "a": {"type": "integer"}, "b": {"type": "string"}}}
        result = self.check(old, new, [consumer(strict=False)],
                            reader_evidence=frozenset({"skill:reader"}))
        self.assertEqual(result.classification, "breaking")
        self.assertIn("REQUIRED_FIELD_ADDED", self.codes(result))
        self.assertIn("EXPECTED_SHAPE_CHANGED", self.codes(result))

    def test_removed_required_output_identifies_consumer(self):
        before = {"outputs": [{"name": "analysis"}, {"name": "decision"}]}
        after = {"outputs": [{"name": "analysis"}]}
        result = self.check(before, after, [consumer(outputs=("decision",))])
        self.assertIn("REQUIRED_OUTPUT_REMOVED", self.codes(result))
        issue = next(f for f in result.findings if f.code == "REQUIRED_OUTPUT_REMOVED")
        self.assertEqual(issue.affected_consumer_ids, ("skill:reader",))
        self.assertIn("decision", issue.json_pointer)

    def test_product_model_id_and_phase_owner_and_gate_meaning(self):
        old = {"lifecycle": {"cycles": [
            {"id": "a", "phases": [{"id": "p"}]}]},
            "tracks": [], "gates": [{"id": "pass", "meaning": "A"}],
            "decisions": [], "project_statuses": []}
        new = {"lifecycle": {"cycles": [
            {"id": "b", "phases": [{"id": "p"}]}]},
            "tracks": [], "gates": [{"id": "pass", "meaning": "B"}],
            "decisions": [], "project_statuses": []}
        edge = consumer(provider="product-model")
        result = self.check(old, new, [edge], kind="product_model")
        self.assertIn("CANONICAL_ID_REMOVED", self.codes(result))
        self.assertIn("CANONICAL_MEANING_CHANGED", self.codes(result))
        self.assertEqual(result.classification, "breaking")

    def test_closed_model_reader_additive_gate_breaks(self):
        old = {"lifecycle": {"cycles": []}, "gates": [{"id": "pass", "meaning": "yes"}]}
        new = {"lifecycle": {"cycles": []}, "gates": [
            {"id": "pass", "meaning": "yes"}, {"id": "warn", "meaning": "maybe"}]}
        result = self.check(old, new, [consumer(provider="product-model")], kind="product_model")
        self.assertIn("STRICT_READER_NEW_CANONICAL_ID", self.codes(result))

    def test_semantics_require_review_even_same_structure(self):
        before = {"triggers": {"include": ["a"], "exclude": ["b"]},
                  "evidence_rules": "one test", "stop_conditions": ["missing proof"]}
        after = {"triggers": {"include": ["a"], "exclude": ["c"]},
                 "evidence_rules": "none", "stop_conditions": ["ignore"]}
        result = self.check(before, after, [consumer(strict=False)])
        self.assertEqual(result.classification, "review_required")
        self.assertIn("SEMANTIC_CHANGE_REVIEW", self.codes(result))

    def test_unknown_baseline_and_external_readers_never_green(self):
        result = self.check(None, {"outputs": []}, [consumer(strict=False)], external=True)
        self.assertEqual(result.classification, "unassessed")
        self.assertIn("UNKNOWN_BASELINE", self.codes(result))
        self.assertIn("EXTERNAL_READERS_UNASSESSED", self.codes(result))
        self.assertIn("external:unknown", result.unassessed_consumers)

    def test_version_ranges_and_pre_one_caret(self):
        self.assertTrue(semver_in_range("1.4.0", ">=1.2.0 <2.0.0"))
        self.assertFalse(semver_in_range("2.0.0", "^1.0.0"))
        self.assertTrue(semver_in_range("0.2.7", "^0.2.0"))
        self.assertFalse(semver_in_range("0.3.0", "^0.2.0"))
        with self.assertRaises(CompatibilityValidationError):
            semver_in_range("1.0.0", "1.*")

    def test_missing_unsupported_mismatch_conflict_and_cycle(self):
        edges = (
            consumer("skill:a", "skill:b", version_range=">=2.0.0"),
            consumer("skill:b", "skill:a", version_range="^1.0.0"),
            consumer("skill:c", "skill:b", version_range="<2.0.0"),
            consumer("skill:d", "skill:missing"),
        )
        providers = {"skill:a": ("1.1.0", "active"), "skill:b": ("1.4.0", "unsupported")}
        codes = {x.code for x in check_consumer_dependencies(edges, providers)}
        for code in ("UNSUPPORTED_PROVIDER", "VERSION_RANGE_MISMATCH",
                     "CONFLICTING_RANGES", "DEPENDENCY_CYCLE", "MISSING_PROVIDER"):
            self.assertIn(code, codes)

    def test_unknown_versions_and_ranges_are_unassessed(self):
        edges = (consumer("skill:a", "skill:b", version_range=None),)
        codes = {x.code for x in check_consumer_dependencies(
            edges, {"skill:b": (None, "unpublished")})}
        self.assertIn("UNKNOWN_PROVIDER_SUPPORT", codes)
        self.assertIn("UNKNOWN_PROVIDER_VERSION", codes)

    def test_fixture_parser_fails_fast_on_invalid_prerequisites(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "consumers.json"
            valid = {"consumers": [{
                "consumer_id": "skill:reader", "provider_component_id": "skill:provider",
                "range": "^1.0.0", "required_outputs": ["decision"],
                "required_features": [], "strict_reader": True,
                "declared_by": "skills/reader/manifest.yaml", "scope": "fixture"}]}
            path.write_text(json.dumps(valid), encoding="utf-8")
            self.assertEqual(len(load_consumer_dependencies(path)), 1)
            invalids = [
                ("invalid range", {**valid["consumers"][0], "range": "1.*"}),
                ("duplicate output", {**valid["consumers"][0], "required_outputs": ["a", "a"]}),
                ("invalid path", {**valid["consumers"][0], "declared_by": "../secret"}),
                ("missing field", {k: v for k, v in valid["consumers"][0].items() if k != "strict_reader"}),
            ]
            for label, invalid in invalids:
                with self.subTest(label=label):
                    path.write_text(json.dumps({"consumers": [invalid]}), encoding="utf-8")
                    with self.assertRaises(CompatibilityValidationError):
                        load_consumer_dependencies(path)
            path.write_text('{"consumers":[],"consumers":[]}', encoding="utf-8")
            with self.assertRaisesRegex(CompatibilityValidationError, "duplicate"):
                load_consumer_dependencies(path)
            path.unlink()
            with self.assertRaisesRegex(CompatibilityValidationError, "cannot read consumers"):
                load_consumer_dependencies(path)

    def test_local_reader_inventory_does_not_invent_support(self):
        readers = enumerate_known_consumers(ROOT)
        self.assertTrue(any(x.consumer_id == "repo:manifest-parser" for x in readers))
        self.assertTrue(all(x.version_range is None for x in readers))
        self.assertTrue(all((ROOT / x.declared_by).is_file() for x in readers))


if __name__ == "__main__":
    unittest.main()
