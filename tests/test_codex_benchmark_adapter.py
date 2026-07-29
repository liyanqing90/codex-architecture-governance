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


if __name__ == "__main__":
    unittest.main()
