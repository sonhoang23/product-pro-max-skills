"""Spec 002: repository skill authoring contract guardrails (static)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CREATOR = ROOT / ".agents/skills/skill-creator-vi/SKILL.md"


class SkillCreatorContractTests(unittest.TestCase):
    def test_creator_consumes_authoritative_contract(self):
        text = CREATOR.read_text(encoding="utf-8")
        for item in ("SKILL-MODEL.md", "SKILL-CONTRACT.md", "model/product-model.json"):
            with self.subTest(item=item):
                self.assertIn(item, text)

    def test_authoring_requires_canonical_paired_identity(self):
        text = CREATOR.read_text(encoding="utf-8")
        for item in ("ppmax-<slug>", "skills/<primary-cycle>/ppmax-<slug>/",
                     "manifest.yaml", "SKILL.md.name", "primary_cycle",
                     "triggers.include/exclude", "related_skills", "workflows"):
            with self.subTest(item=item):
                self.assertIn(item, text)

    def test_new_and_existing_skill_validation_guidance(self):
        text = CREATOR.read_text(encoding="utf-8")
        self.assertIn("Skill đang có", text)
        self.assertIn("generate_skill_registry.py generate", text)
        self.assertIn("generate_skill_registry.py check", text)
        self.assertIn("test_skill*.py", text)
        self.assertIn("không tuyên bố runtime PASS", text)

    def test_development_skills_excluded(self):
        text = CREATOR.read_text(encoding="utf-8")
        self.assertIn(".agents/skills/", text)
        self.assertIn("không đưa skill nội bộ vào registry", text)


if __name__ == "__main__":
    unittest.main()
