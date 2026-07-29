from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import yaml

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
            python_version = subprocess.run(
                [sys.executable, "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            python_surface = (
                python_version.stdout.strip() or python_version.stderr.strip()
            )
            args = Namespace(
                root=ROOT,
                ground_truth=ROOT / "benchmarks" / "ground-truth.yaml",
                output=output,
                model="test-model",
                surface=python_surface,
                skill_version="0.4.0",
                runtime_executables=[sys.executable],
                timeout=10,
                command=[
                    sys.executable,
                    "-c",
                    (
                        "import json; "
                        "print(json.dumps({'observed_findings': [], "
                        "'observed_recommendations': [], "
                        "'observed_decision': {"
                        "'selected_option': 'test-option', "
                        "'compared_tradeoffs': [], "
                        "'knowledge_ids': [], "
                        "'rejected_options': [], "
                        "'migration_slices': []}}))"
                    ),
                    str(ROOT / "scripts" / "codex_benchmark_adapter.py"),
                    "{skill}",
                    "{fixture}",
                    "{prompt}",
                ],
            )
            result = run_behavior_benchmark.run_benchmark(args)
            log_path = output.with_suffix(".log.jsonl")
            self.assertEqual(len(result["cases"]), 10)
            self.assertEqual(result["schema_version"], "1.4")
            self.assertEqual(result["benchmark"]["model"], "test-model")
            provenance = result["benchmark"]["provenance"]
            self.assertEqual(provenance["command_template"], args.command)
            self.assertEqual(provenance["model_request"], "test-model")
            self.assertEqual(
                {item["role"] for item in provenance["runtime_executables"]},
                {"command", "model"},
            )
            self.assertIn(
                "plugin-manifest",
                {item["role"] for item in provenance["inputs"]},
            )
            self.assertEqual(provenance["execution_log"]["records"], 10)
            self.assertEqual(
                provenance["execution_log"]["sha256"],
                hashlib.sha256(log_path.read_bytes()).hexdigest(),
            )
            log_records = [
                json.loads(line)
                for line in log_path.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(log_records), 10)
            self.assertTrue(
                all(
                    "execution" in trial and trial["execution"]["command"]
                    for case in result["cases"]
                    for trial in case["trials"]
                )
            )
            self.assertTrue(
                all(case["observed_findings"] == [] for case in result["cases"])
            )
            output.write_text(
                yaml.safe_dump(result, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            score = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "resources" / "scripts" / "architecture_tool.py"),
                    "benchmark-score",
                    "--ground-truth",
                    str(ROOT / "benchmarks" / "ground-truth.yaml"),
                    "--run",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(score.returncode, 0, score.stderr)
            score_payload = json.loads(score.stdout)
            self.assertTrue(score_payload["provenance"]["valid"])
            self.assertTrue(
                score_payload["provenance"]["runtime_verification"][
                    "current_host_match"
                ]
            )

            original_version = provenance["runtime_executables"][0]["version_output"]
            provenance["runtime_executables"][0]["version_output"] = "tampered"
            output.write_text(
                yaml.safe_dump(result, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            runtime_tampered = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "resources" / "scripts" / "architecture_tool.py"),
                    "benchmark-score",
                    "--ground-truth",
                    str(ROOT / "benchmarks" / "ground-truth.yaml"),
                    "--run",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(runtime_tampered.returncode, 2)
            self.assertIn(
                "recorded runtime version hash mismatch",
                runtime_tampered.stderr,
            )
            provenance["runtime_executables"][0]["version_output"] = original_version
            output.write_text(
                yaml.safe_dump(result, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )

            log_path.write_text(
                log_path.read_text(encoding="utf-8") + "{}\n",
                encoding="utf-8",
            )
            tampered = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "resources" / "scripts" / "architecture_tool.py"),
                    "benchmark-score",
                    "--ground-truth",
                    str(ROOT / "benchmarks" / "ground-truth.yaml"),
                    "--run",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(tampered.returncode, 2)
            self.assertIn("execution log hash mismatch", tampered.stderr)

    def test_archived_runtime_verification_binds_git_artifacts(self) -> None:
        head = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        run_path = ROOT / "benchmarks" / "results" / "gpt-5.6-terra.yaml"
        process = subprocess.run(
            [
                sys.executable,
                str(ROOT / "resources" / "scripts" / "architecture_tool.py"),
                "benchmark-score",
                "--ground-truth",
                str(ROOT / "benchmarks" / "ground-truth.yaml"),
                "--run",
                str(run_path),
                "--runtime-verification",
                "archived",
                "--artifact-commit",
                head,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        score = json.loads(process.stdout)
        provenance = score["provenance"]
        self.assertTrue(provenance["valid"])
        self.assertEqual(
            provenance["archive_binding"]["run_path"],
            "benchmarks/results/gpt-5.6-terra.yaml",
        )
        self.assertEqual(
            provenance["archive_binding"]["execution_log_path"],
            "benchmarks/results/gpt-5.6-terra.log.jsonl",
        )

        with tempfile.TemporaryDirectory() as temporary:
            tampered = Path(temporary) / run_path.name
            tampered.write_bytes(run_path.read_bytes() + b"\n")
            rejected = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "resources" / "scripts" / "architecture_tool.py"),
                    "benchmark-score",
                    "--ground-truth",
                    str(ROOT / "benchmarks" / "ground-truth.yaml"),
                    "--run",
                    str(tampered),
                    "--runtime-verification",
                    "archived",
                    "--artifact-commit",
                    head,
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(rejected.returncode, 2)
            self.assertIn(
                "Archived benchmark run must be inside the repository",
                rejected.stderr,
            )

    def test_failed_trial_preserves_a_hash_only_execution_log(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "failed.yaml"
            python_version = subprocess.run(
                [sys.executable, "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            args = Namespace(
                root=ROOT,
                ground_truth=ROOT / "benchmarks" / "ground-truth.yaml",
                output=output,
                model="test-model",
                surface=(
                    python_version.stdout.strip() or python_version.stderr.strip()
                ),
                skill_version="0.4.0",
                runtime_executables=[sys.executable],
                timeout=10,
                repetitions=1,
                command=[sys.executable, "-c", "raise SystemExit(7)"],
            )
            with self.assertRaisesRegex(RuntimeError, "trial 1 failed"):
                run_behavior_benchmark.run_benchmark(args)
            record = json.loads(
                output.with_suffix(".log.jsonl").read_text(encoding="utf-8")
            )
            self.assertEqual(record["exit_code"], 7)
            self.assertIsNone(record["observation"])
            self.assertEqual(
                set(record),
                {
                    "schema_version",
                    "case_id",
                    "trial_index",
                    "duration_seconds",
                    "exit_code",
                    "command",
                    "command_sha256",
                    "stdout_sha256",
                    "stderr_sha256",
                    "observation",
                },
            )

    def test_command_placeholders_are_argument_safe(self) -> None:
        fixture = Path("/tmp/fixture with spaces")
        rendered = run_behavior_benchmark.render_command(
            ["agent", "--prompt", "{prompt}", "--repo", "{fixture}"],
            skill="project-architecture-audit",
            fixture=fixture,
            prompt="Audit; do not execute this punctuation.",
        )
        self.assertEqual(rendered[2], "Audit; do not execute this punctuation.")
        self.assertEqual(rendered[4], str(fixture))

    def test_fixture_evidence_is_resolved_not_self_asserted(self) -> None:
        fixture = ROOT / "benchmarks" / "fixtures" / "account-balance-updates"
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

    def test_fixture_inputs_do_not_disclose_expected_outcomes(self) -> None:
        corpus = run_behavior_benchmark.load_yaml(
            ROOT / "benchmarks" / "ground-truth.yaml"
        )
        banned_path_terms = {
            "benign",
            "conflict",
            "healthy",
            "injected",
            "missing",
            "sufficient",
        }
        banned_content = {
            "expected behavior:",
            "expected decision:",
            "do not recommend",
        }
        for case in corpus["cases"]:
            fixture = ROOT / case["fixture"]
            self.assertTrue(fixture.is_dir(), case["id"])
            self.assertTrue(
                banned_path_terms.isdisjoint(fixture.name.split("-")),
                fixture.name,
            )
            for path in fixture.rglob("*"):
                if not path.is_file():
                    continue
                content = path.read_text(encoding="utf-8").lower()
                for phrase in banned_content:
                    self.assertNotIn(phrase, content, str(path))


if __name__ == "__main__":
    unittest.main()
