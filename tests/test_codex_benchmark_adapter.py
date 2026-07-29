from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "codex_benchmark_adapter.py"
SPEC = importlib.util.spec_from_file_location("codex_benchmark_adapter", SCRIPT_PATH)
assert SPEC and SPEC.loader
codex_benchmark_adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(codex_benchmark_adapter)


class CodexBenchmarkAdapterTests(unittest.TestCase):
    def test_allowed_rules_come_from_machine_rule_packs(self) -> None:
        rule_ids = codex_benchmark_adapter.allowed_rule_ids(ROOT)
        self.assertIn("PROJECT.IDEMPOTENCY.001", rule_ids)
        self.assertIn("AI.TOOL.002", rule_ids)
        self.assertNotIn("pattern.idempotency-key", rule_ids)

    def test_prompt_tradeoff_vocabulary_matches_observation_schema(self) -> None:
        schema = json.loads(
            (
                ROOT / "resources" / "schemas" / "benchmark-observation.schema.json"
            ).read_text(encoding="utf-8")
        )
        schema_tradeoffs = schema["properties"]["observed_decision"]["properties"][
            "compared_tradeoffs"
        ]["items"]["enum"]
        self.assertEqual(
            list(codex_benchmark_adapter.CANONICAL_TRADEOFFS),
            schema_tradeoffs,
        )

    def test_evidence_validation_requires_a_verbatim_contiguous_excerpt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            (fixture / "sample.py").write_text(
                "def run():\n    return True\n",
                encoding="utf-8",
            )
            valid = {
                "observed_findings": [
                    {
                        "rule_id": "PROJECT.TEST.001",
                        "evidence": [
                            {
                                "path": "sample.py",
                                "line_start": 2,
                                "line_end": 2,
                                "excerpt": "    return True",
                            }
                        ],
                    }
                ]
            }
            self.assertEqual(
                codex_benchmark_adapter.evidence_errors(valid, fixture),
                [],
            )
            valid["observed_findings"][0]["evidence"][0]["excerpt"] = "..."
            self.assertTrue(
                codex_benchmark_adapter.evidence_errors(valid, fixture),
            )

    def test_solution_prompt_uses_canonical_option_and_tradeoff_ids(self) -> None:
        prompt = codex_benchmark_adapter.build_prompt(
            skill_path=ROOT / "skills" / "architecture-solution-advisor" / "SKILL.md",
            knowledge_root=ROOT / "resources" / "knowledge",
            fixture=ROOT / "benchmarks" / "fixtures" / "render-job-processing",
            task="Choose a proportional architecture.",
        )
        self.assertIn("style.web-queue-worker becomes web-queue-worker", prompt)
        self.assertIn("delivery-semantics", prompt)
        self.assertIn("never combine dimensions", prompt)

    def test_base_prompt_does_not_disclose_skill_or_knowledge_locations(self) -> None:
        skill_path = ROOT / "skills" / "project-architecture-audit" / "SKILL.md"
        knowledge_root = ROOT / "resources" / "knowledge"
        prompt = codex_benchmark_adapter.build_prompt(
            skill_path=skill_path,
            knowledge_root=knowledge_root,
            fixture=ROOT / "benchmarks" / "fixtures" / "desktop-sqlite-catalog",
            task="Audit only directly proved risks.",
            condition="base",
        )
        self.assertNotIn(str(skill_path), prompt)
        self.assertNotIn(str(knowledge_root), prompt)
        self.assertNotIn("Read and follow the Skill", prompt)

    def test_compressed_treatment_uses_only_manifest_declared_inputs(self) -> None:
        manifest = codex_benchmark_adapter.load_context_manifest(
            ROOT,
            ROOT / "benchmarks" / "ablation" / "context-manifest.yaml",
        )
        treatment = codex_benchmark_adapter.treatment_for(
            manifest,
            condition="compressed",
            skill="architecture-solution-advisor",
        )
        compact = codex_benchmark_adapter.resolve_treatment_paths(
            ROOT,
            treatment,
            "skill_body",
        )
        knowledge = codex_benchmark_adapter.resolve_treatment_paths(
            ROOT,
            treatment,
            "knowledge",
        )
        prompt = codex_benchmark_adapter.build_prompt(
            skill_path=ROOT / "skills" / "architecture-solution-advisor" / "SKILL.md",
            knowledge_root=ROOT / "resources" / "knowledge",
            fixture=ROOT / "benchmarks" / "fixtures" / "render-job-processing",
            task="Select a proportional architecture.",
            condition="compressed",
            compact_skill_paths=compact,
            knowledge_paths=knowledge,
        )
        self.assertIn(str(compact[0]), prompt)
        self.assertIn(str(knowledge[0]), prompt)
        self.assertNotIn(
            str(ROOT / "skills" / "architecture-solution-advisor" / "SKILL.md"),
            prompt,
        )

    def test_full_treatment_uses_declared_references_and_shared_knowledge(self) -> None:
        manifest = codex_benchmark_adapter.load_context_manifest(
            ROOT,
            ROOT / "benchmarks" / "ablation" / "context-manifest.yaml",
        )
        full = codex_benchmark_adapter.treatment_for(
            manifest,
            condition="full",
            skill="architecture-solution-advisor",
        )
        compressed = codex_benchmark_adapter.treatment_for(
            manifest,
            condition="compressed",
            skill="architecture-solution-advisor",
        )
        references = codex_benchmark_adapter.resolve_treatment_paths(
            ROOT,
            full,
            "references",
        )
        knowledge = codex_benchmark_adapter.resolve_treatment_paths(
            ROOT,
            full,
            "knowledge",
        )
        prompt = codex_benchmark_adapter.build_prompt(
            skill_path=ROOT / "skills" / "architecture-solution-advisor" / "SKILL.md",
            knowledge_root=ROOT / "resources" / "knowledge",
            fixture=ROOT / "benchmarks" / "fixtures" / "render-job-processing",
            task="Select a proportional architecture.",
            condition="full",
            reference_paths=references,
            knowledge_paths=knowledge,
        )
        self.assertEqual(full["knowledge"], compressed["knowledge"])
        self.assertIn(str(references[0]), prompt)
        self.assertIn(str(knowledge[0]), prompt)
        self.assertNotIn("The architecture knowledge catalog is read-only at", prompt)


if __name__ == "__main__":
    unittest.main()
