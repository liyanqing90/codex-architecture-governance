from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "run_behavior_benchmark.py"
SPEC = importlib.util.spec_from_file_location("run_behavior_benchmark", SCRIPT_PATH)
assert SPEC and SPEC.loader
run_behavior_benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_behavior_benchmark)


class BehaviorBenchmarkTests(unittest.TestCase):
    def test_runner_executes_every_fixture_without_ground_truth_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run.yaml"
            args = Namespace(
                root=ROOT,
                ground_truth=ROOT / "benchmarks" / "ground-truth.yaml",
                output=output,
                model="test-model",
                surface="pytest",
                skill_version="0.2.0",
                timeout=10,
                command=[
                    sys.executable,
                    "-c",
                    (
                        "import json; "
                        "print(json.dumps({'observed_findings': [], "
                        "'observed_recommendations': []}))"
                    ),
                    "{skill}",
                    "{fixture}",
                    "{prompt}",
                ],
            )
            result = run_behavior_benchmark.run_benchmark(args)
            self.assertEqual(len(result["cases"]), 10)
            self.assertEqual(result["benchmark"]["model"], "test-model")
            self.assertTrue(
                all(case["observed_findings"] == [] for case in result["cases"])
            )

    def test_command_placeholders_are_argument_safe(self) -> None:
        rendered = run_behavior_benchmark.render_command(
            ["agent", "--prompt", "{prompt}", "--repo", "{fixture}"],
            skill="project-architecture-audit",
            fixture=Path("/tmp/fixture with spaces"),
            prompt="Audit; do not execute this punctuation.",
        )
        self.assertEqual(rendered[2], "Audit; do not execute this punctuation.")
        self.assertEqual(rendered[4], "/tmp/fixture with spaces")

    def test_fixture_evidence_is_resolved_not_self_asserted(self) -> None:
        fixture = ROOT / "benchmarks" / "fixtures" / "conflicting-writers"
        valid = [
            {
                "path": "store.py",
                "line_start": 1,
                "line_end": 3,
                "excerpt": "connection.write_balance(account_id, balance + amount)",
            }
        ]
        self.assertTrue(run_behavior_benchmark.evidence_is_valid(fixture, valid))
        invalid = [dict(valid[0], excerpt="a line that is not in the fixture")]
        self.assertFalse(run_behavior_benchmark.evidence_is_valid(fixture, invalid))


if __name__ == "__main__":
    unittest.main()
