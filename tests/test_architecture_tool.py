from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from datetime import date
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "resources" / "scripts" / "architecture_tool.py"
SPEC = importlib.util.spec_from_file_location("architecture_tool", SCRIPT_PATH)
assert SPEC and SPEC.loader
architecture_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(architecture_tool)


class ArchitectureToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def project_args(self) -> Namespace:
        return Namespace(
            repo=str(self.root),
            name="Test Project",
            project_id="test-project",
            types=["service"],
            lifecycle="active",
            criticality="high",
            owners=["test-owner"],
            qualities=["recoverability"],
            reviews=["project-architecture"],
            rule_packs=["project-core"],
            data_classification="internal",
        )

    def portfolio_args(self) -> Namespace:
        return Namespace(
            root=str(self.root),
            name="Test Portfolio",
            portfolio_id="test-portfolio",
            owners=["test-owner"],
            review_horizon_months=12,
        )

    def finding(
        self,
        verification: str = "confirmed",
        status: str = "open",
    ) -> dict:
        rationale = (
            "Direct source and caller evidence confirm the path."
            if verification == "confirmed"
            else "The candidate cannot yet be confirmed from current evidence."
        )
        return {
            "id": "TEST-DATA-001",
            "kind": "risk",
            "rule_id": "PROJECT.DATA.001",
            "title": "Conflicting authoritative writers",
            "invariant": "One component owns authoritative writes for this record.",
            "severity": "high",
            "confidence": 0.9,
            "verification": {
                "status": verification,
                "rationale": rationale,
                "verified_by": "test-verifier",
                "verified_at": "2026-07-28T10:00:00+00:00",
            },
            "status": status,
            "evidence": [
                {
                    "type": "source",
                    "location": "src/store.py:42",
                    "symbol": "save",
                    "observation": "Two independent writers update the same record.",
                    "source_commit": "deadbeef",
                }
            ],
            "impact": {
                "affected_components": ["store", "worker"],
                "failure_mode": "Concurrent updates can silently overwrite state.",
                "blast_radius": "All records processed by both writers.",
            },
            "counter_evidence": [],
            "first_seen": "2026-07-28",
            "last_seen": "2026-07-28",
            "found_by": ["test-auditor"],
            "tags": ["data-ownership"],
        }

    def review(self, verification: str = "confirmed") -> dict:
        finding_status = "rejected" if verification == "rejected" else "open"
        finding = self.finding(verification=verification, status=finding_status)
        counts = {
            "confirmed": int(verification == "confirmed"),
            "rejected": int(verification == "rejected"),
            "needs_evidence": int(verification == "needs-evidence"),
        }
        return {
            "schema_version": "1.0",
            "review": {
                "id": "2026-07-28-test-project",
                "kind": "project",
                "subject": {
                    "id": "test-project",
                    "name": "Test Project",
                    "repository": str(self.root),
                },
                "performed_at": "2026-07-28T10:00:00+00:00",
                "commit": "deadbeef",
                "scope": ["."],
                "verification_state": "verified",
                "reviewers": ["test-verifier"],
                "profile": ".architecture/profile.yaml",
            },
            "summary": {
                "architecture": "A test service with two writers.",
                "raw_findings": 1,
                **counts,
            },
            "coverage": [
                {
                    "rule_id": "PROJECT.DATA.001",
                    "status": "assessed",
                    "finding_ids": ["TEST-DATA-001"],
                }
            ],
            "findings": [finding],
            "evidence_sources": ["src/store.py"],
            "limitations": [],
        }

    def write_yaml(self, path: Path, value: dict) -> None:
        path.write_text(
            yaml.safe_dump(value, sort_keys=False),
            encoding="utf-8",
        )

    def init_project(self) -> Path:
        return architecture_tool.init_project(self.project_args())

    def write_review(self, review: dict | None = None) -> Path:
        reviews = self.root / ".architecture" / "reviews"
        path = reviews / "2026-07-28-project-verified.yaml"
        self.write_yaml(path, review or self.review())
        return path

    def test_init_and_validate_project(self) -> None:
        target = self.init_project()
        self.assertEqual(target, self.root / ".architecture")
        validated = architecture_tool.validate_project(self.root)
        self.assertEqual(len(validated), 5)
        with self.assertRaises(architecture_tool.ArchitectureError):
            architecture_tool.init_project(self.project_args())

    def test_repository_dogfood_configuration_is_valid(self) -> None:
        validated = architecture_tool.validate_project(ROOT)
        self.assertEqual(len(validated), 5)

    def test_init_and_validate_empty_portfolio(self) -> None:
        target = architecture_tool.init_portfolio(self.portfolio_args())
        self.assertEqual(target, self.root / ".architecture-portfolio")
        validated = architecture_tool.validate_portfolio(self.root)
        self.assertEqual(len(validated), 6)

    def test_portfolio_gate_blocks_confirmed_high_finding(self) -> None:
        architecture_tool.init_portfolio(self.portfolio_args())
        review = self.review()
        review["review"].update(
            {
                "id": "2026-07-28-test-portfolio",
                "kind": "portfolio",
                "subject": {
                    "id": "test-portfolio",
                    "name": "Test Portfolio",
                },
                "commits": {
                    "project-a": "deadbeef",
                    "project-b": "cafebabe",
                },
            }
        )
        review["review"].pop("commit")
        review["findings"][0]["rule_id"] = "PORTFOLIO.DATA.001"
        review["coverage"][0]["rule_id"] = "PORTFOLIO.DATA.001"
        review_path = (
            self.root
            / ".architecture-portfolio"
            / "reviews"
            / "2026-07-28-portfolio-verified.yaml"
        )
        self.write_yaml(review_path, review)
        result = architecture_tool.gate_portfolio(
            self.root,
            review_path,
            today=date(2026, 7, 28),
        )
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["blocking"][0]["id"], "TEST-DATA-001")

    def test_review_rejects_candidate_in_verified_bundle(self) -> None:
        self.init_project()
        review = self.review()
        review["findings"][0]["verification"]["status"] = "candidate"
        review["findings"][0]["verification"]["rationale"] = "Awaiting verification."
        review["summary"]["confirmed"] = 0
        path = self.write_review(review)
        with self.assertRaisesRegex(
            architecture_tool.ArchitectureError,
            "still has candidate IDs",
        ):
            architecture_tool.validate_review(path)

    def test_validate_remediation_plan(self) -> None:
        plan_path = self.root / "plan.yaml"
        self.write_yaml(
            plan_path,
            {
                "schema_version": "1.0",
                "plan": {
                    "id": "2026-07-28-test-remediation",
                    "source_review": "2026-07-28-test-project",
                    "generated_at": "2026-07-28T11:00:00+00:00",
                    "scope": ["store"],
                    "status": "draft",
                },
                "items": [
                    {
                        "id": "PLAN-DATA-001",
                        "finding_ids": ["TEST-DATA-001"],
                        "desired_invariant": "One owner performs authoritative writes.",
                        "owner": "test-owner",
                        "recommended_option": {
                            "title": "Route writes through the owner",
                            "rationale": (
                                "It restores one authoritative write boundary."
                            ),
                            "tradeoffs": ["Requires caller migration."],
                        },
                        "alternatives": [],
                        "do_nothing": "Conflicting writes remain possible.",
                        "effort": {
                            "size": "m",
                            "uncertainty": "medium",
                            "assumptions": ["Both callers can migrate."],
                        },
                        "change_risk": "medium",
                        "governed_change": False,
                        "dependencies": [],
                        "sequence": ["Protect current write behavior with tests."],
                        "test_protection": [
                            "Exercise concurrent writes at the owning boundary."
                        ],
                        "rollback": "Keep the previous adapter until acceptance.",
                        "acceptance_criteria": [
                            "All writes pass through the authoritative owner."
                        ],
                    }
                ],
            },
        )
        validated = architecture_tool.validate_plan(plan_path)
        self.assertEqual(validated["items"][0]["id"], "PLAN-DATA-001")

    def test_confirmed_high_finding_blocks(self) -> None:
        self.init_project()
        review_path = self.write_review()
        result = architecture_tool.gate_project(
            self.root,
            review_path,
            today=date(2026, 7, 28),
        )
        self.assertEqual(result["status"], "fail")
        self.assertEqual(
            [finding["id"] for finding in result["blocking"]],
            ["TEST-DATA-001"],
        )

    def test_active_baseline_suppresses_confirmed_finding(self) -> None:
        self.init_project()
        review_path = self.write_review()
        baseline_path = self.root / ".architecture" / "baseline.yaml"
        self.write_yaml(
            baseline_path,
            {
                "schema_version": "1.0",
                "findings": [
                    {
                        "id": "TEST-DATA-001",
                        "reason": "Accepted migration baseline.",
                        "owner": "test-owner",
                        "recorded_on": "2026-07-28",
                        "expires_on": "2026-08-28",
                    }
                ],
            },
        )
        result = architecture_tool.gate_project(
            self.root,
            review_path,
            today=date(2026, 7, 28),
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["baselined"], ["TEST-DATA-001"])

    def test_needs_evidence_warns_but_does_not_block(self) -> None:
        self.init_project()
        review_path = self.write_review(self.review("needs-evidence"))
        result = architecture_tool.gate_project(
            self.root,
            review_path,
            today=date(2026, 7, 28),
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["unverified"], ["TEST-DATA-001"])
        self.assertTrue(result["warnings"])

    def test_expired_waiver_does_not_suppress(self) -> None:
        self.init_project()
        review_path = self.write_review()
        policy_path = self.root / ".architecture" / "gate-policy.yaml"
        policy = architecture_tool.load_yaml(policy_path)
        policy["waivers"] = [
            {
                "finding_id": "TEST-DATA-001",
                "reason": "Temporary migration exception.",
                "owner": "test-owner",
                "expires_on": "2026-07-27",
            }
        ]
        self.write_yaml(policy_path, policy)
        result = architecture_tool.gate_project(
            self.root,
            review_path,
            today=date(2026, 7, 28),
        )
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["expired_waivers"], ["TEST-DATA-001"])

    def test_cli_json_preserves_policy_exit_code(self) -> None:
        self.init_project()
        review_path = self.write_review()
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "gate",
                "--project",
                str(self.root),
                "--review",
                str(review_path),
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 1, process.stderr)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["status"], "fail")

    def test_cli_reports_version(self) -> None:
        process = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--version"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout.strip(), "architecture_tool.py 0.1.0")


if __name__ == "__main__":
    unittest.main()
