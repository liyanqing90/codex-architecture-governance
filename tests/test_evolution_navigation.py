from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "resources" / "scripts" / "architecture_tool.py"
sys.path.insert(0, str(SCRIPT_PATH.parent))
SPEC = importlib.util.spec_from_file_location(
    "architecture_tool_evolution_navigation",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
architecture_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(architecture_tool)


class EvolutionAssessmentContractTests(unittest.TestCase):
    def test_evolution_assessment_is_content_bound_and_adoption_gated(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            assessment_path = root / "assessment.md"
            assessment_path.write_bytes(
                (
                    ROOT / "resources" / "templates" / "evolution-assessment.md"
                ).read_bytes()
            )
            evidence_paths = {}
            for name in ("baseline", "gap", "official", "pilot"):
                evidence_path = root / f"{name}.txt"
                evidence_path.write_text(
                    f"Bound {name} evidence with observed project values.\n",
                    encoding="utf-8",
                )
                evidence_paths[name] = evidence_path

            def evidence(name: str) -> dict[str, str]:
                evidence_path = evidence_paths[name]
                return {
                    "path": evidence_path.name,
                    "sha256": hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
                    "description": f"Bound evidence for {name} observation.",
                }

            data = {
                "decision": {
                    "assessment_kind": "technology-evolution",
                    "status": "proposed",
                },
                "selected_option": "keep-current",
                "evolution_assessment": {
                    "path": "assessment.md",
                    "sha256": hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
                    "disposition": "keep-current",
                    "baseline": {
                        "owner": "runtime-owner",
                        "local_correction": "Tune the current runtime boundary.",
                        "do_nothing_consequence": "Latency remains above target.",
                        "measures": [
                            {
                                "metric": "p95 latency",
                                "value": "420 ms",
                                "method": "Replay the production-shaped fixture.",
                                "evidence": evidence("baseline"),
                            }
                        ],
                    },
                    "gap": {
                        "scenario": "Complete the critical flow within the target.",
                        "current_value": "420 ms",
                        "target": "250 ms",
                        "measurement_method": "Replay the same bounded fixture.",
                        "threshold": "p95 <= 250 ms",
                        "evidence": [evidence("gap")],
                    },
                    "volatile_claims": [
                        {
                            "claim": "Candidate runtime supports the required API.",
                            "publisher": "runtime publisher",
                            "url": "https://example.com/runtime/support",
                            "scope": "Current supported release and API surface.",
                            "accessed_on": "2026-08-06",
                            "freshness": "unknown",
                            "capture": evidence("official"),
                        }
                    ],
                    "compatibility": {
                        "consumers": ["critical-flow caller"],
                        "contracts": ["runtime request contract"],
                        "mixed_version_behavior": "Old and new adapters coexist.",
                        "migration_steps": ["Route one bounded cohort first."],
                        "duration": "two weeks",
                        "cost": "bounded team time",
                    },
                    "operations": {
                        "owner": "runtime-owner",
                        "required_skills": ["runtime operations"],
                        "support_model": "The existing on-call owns the pilot.",
                        "observability": "Compare latency and error dashboards.",
                        "failure_semantics": "Failures route to the old adapter.",
                        "security": "Existing authorization remains authoritative.",
                        "operating_cost": "measured during pilot",
                    },
                    "lock_in_exit": {
                        "proprietary_surfaces": ["candidate adapter API"],
                        "portability": "The owned adapter preserves portability.",
                        "exit_cost": "one sprint",
                        "data_recovery": "No persistent data leaves the owner.",
                    },
                    "rollback": {
                        "rollback_point": "Before contracting the old adapter.",
                        "irreversible_gate": "Removal of the compatibility adapter.",
                        "validation": "Replay the negative and primary paths.",
                        "compatible_state": "Both adapters accept the same contract.",
                    },
                    "pilot": {
                        "status": "not-run",
                        "owner": "runtime-owner",
                        "cohort": "One bounded non-production replay cohort.",
                        "success_criteria": ["p95 latency reaches the target."],
                        "stop_criteria": ["Error rate exceeds the current path."],
                        "observed_measures": [],
                    },
                    "revisit_triggers": [
                        {
                            "metric_or_event": "p95 latency",
                            "threshold": "above 250 ms",
                            "owner": "runtime-owner",
                            "review_on": "2026-09-06",
                            "reopening_evidence": "Repeat the bounded replay report.",
                        }
                    ],
                },
            }
            decision = architecture_tool.load_yaml(
                ROOT / "resources" / "templates" / "architecture-decision.yaml"
            )
            decision["decision"]["assessment_kind"] = "technology-evolution"
            decision["evolution_assessment"] = data["evolution_assessment"]
            architecture_tool.validate_data(
                decision,
                "architecture-decision.schema.json",
                root / "decision.yaml",
            )
            old_status_only_binding = {
                "path": "assessment.md",
                "sha256": data["evolution_assessment"]["sha256"],
                "disposition": "keep-current",
                "evidence_status": "complete",
                "pilot_status": "completed",
            }
            decision["evolution_assessment"] = old_status_only_binding
            with self.assertRaises(architecture_tool.ArchitectureError):
                architecture_tool.validate_data(
                    decision,
                    "architecture-decision.schema.json",
                    root / "decision.yaml",
                )

            architecture_tool.validate_evolution_assessment_binding(
                root / "decision.yaml",
                data,
                root,
            )
            data["evolution_assessment"]["path"] = str(assessment_path)
            with self.assertRaisesRegex(
                architecture_tool.ArchitectureError,
                "project-relative path",
            ):
                architecture_tool.validate_evolution_assessment_binding(
                    root / "decision.yaml",
                    data,
                    root,
                )
            data["evolution_assessment"]["path"] = "assessment.md"

            assessment_path.write_bytes(assessment_path.read_bytes() + b"\nchanged\n")
            with self.assertRaisesRegex(
                architecture_tool.ArchitectureError,
                "hash does not match",
            ):
                architecture_tool.validate_evolution_assessment_binding(
                    root / "decision.yaml",
                    data,
                    root,
                )

            data["selected_option"] = "upgrade-runtime"
            data["evolution_assessment"].update(
                {
                    "sha256": hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
                    "disposition": "adopt",
                }
            )
            with self.assertRaisesRegex(
                architecture_tool.ArchitectureError,
                "current official evidence",
            ):
                architecture_tool.validate_evolution_assessment_binding(
                    root / "decision.yaml",
                    data,
                    root,
                )
            data["evolution_assessment"]["volatile_claims"][0]["freshness"] = "current"
            with self.assertRaisesRegex(
                architecture_tool.ArchitectureError,
                "completed pilot",
            ):
                architecture_tool.validate_evolution_assessment_binding(
                    root / "decision.yaml",
                    data,
                    root,
                )
            data["evolution_assessment"]["pilot"]["status"] = "completed"
            with self.assertRaisesRegex(
                architecture_tool.ArchitectureError,
                "pilot observed measures",
            ):
                architecture_tool.validate_evolution_assessment_binding(
                    root / "decision.yaml",
                    data,
                    root,
                )
            data["evolution_assessment"]["pilot"]["observed_measures"] = [
                {
                    "metric": "p95 latency",
                    "value": "230 ms",
                    "method": "Replay the bounded pilot cohort.",
                    "evidence": evidence("pilot"),
                }
            ]
            architecture_tool.validate_evolution_assessment_binding(
                root / "decision.yaml",
                data,
                root,
            )
            evidence_paths["pilot"].write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(
                architecture_tool.ArchitectureError,
                r"pilot.observed_measures\[0\].evidence hash does not match",
            ):
                architecture_tool.validate_evolution_assessment_binding(
                    root / "decision.yaml",
                    data,
                    root,
                )

    def test_advisor_requires_evidence_before_emerging_replacement(self) -> None:
        advisor = (
            ROOT / "skills" / "architecture-solution-advisor" / "SKILL.md"
        ).read_text(encoding="utf-8")
        workflow = (
            ROOT
            / "skills"
            / "architecture-solution-advisor"
            / "references"
            / "decision-artifact-workflow.md"
        ).read_text(encoding="utf-8")

        for text in (advisor, workflow):
            self.assertIn("keep-current", text)
            self.assertIn("measurable", text)
            self.assertIn("current official", text)
            self.assertIn("compatibility", text)
            self.assertIn("migration", text)
            self.assertIn("operational", text)
            self.assertIn("team", text)
            self.assertIn("lock-in", text)
            self.assertIn("rollback", text)
            self.assertIn("shadow", text)
            self.assertIn("pilot", text)
            self.assertIn("revisit", text)
        self.assertIn("trend recommendations", advisor)
        self.assertIn("unknown", workflow)

    def test_router_status_navigation_is_read_only_and_authority_preserving(
        self,
    ) -> None:
        router = (ROOT / "skills" / "hengmu" / "SKILL.md").read_text(encoding="utf-8")

        normalized = " ".join(router.split())
        self.assertIn("Read-only lifecycle and status navigation", normalized)
        self.assertIn("status", normalized)
        self.assertIn("verification_state: candidates", normalized)
        self.assertIn("status: proposed", normalized)
        self.assertIn("status: accepted", normalized)
        self.assertIn("must not verify findings", normalized)
        self.assertIn("merge audit and decision authority", normalized)
        self.assertIn("mutate state", normalized)
        self.assertIn("gate implicitly", normalized)
        self.assertIn("explicitly requests it", normalized)


if __name__ == "__main__":
    unittest.main()
