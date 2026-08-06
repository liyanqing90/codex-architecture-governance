from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_ROOT = ROOT / "resources" / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from select_knowledge import knowledge_context  # noqa: E402


class ContextExecutionTests(unittest.TestCase):
    def schema(self, relative_path: str) -> dict:
        return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))

    def assert_valid(self, schema: dict, value: dict) -> None:
        errors = list(
            Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            ).iter_errors(value)
        )
        self.assertEqual(errors, [], errors[0].message if errors else None)

    def assert_invalid(self, schema: dict, value: dict) -> None:
        errors = list(
            Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            ).iter_errors(value)
        )
        self.assertTrue(errors)

    def test_context_is_compact_but_keeps_selection_locks(self) -> None:
        selection = {
            "schema_version": "1.4",
            "selection": [
                {
                    "id": "foundation.evidence-reasoning",
                    "path": "foundations/evidence-reasoning.md",
                    "sha256": "a" * 64,
                    "priority": "required",
                    "reasons": ["Required for evidence discipline."],
                }
            ],
        }
        context = knowledge_context(selection, selection_lock_sha256="b" * 64)

        self.assertEqual(context["schema_version"], "1.1")
        self.assertEqual(context["selection_lock_sha256"], "b" * 64)
        self.assertEqual(
            context["disclosure"]["order"],
            [
                "operational-kernel",
                "project-context",
                "run-context",
                "source-evidence",
            ],
        )
        self.assertEqual(
            set(context),
            {
                "schema_version",
                "selection_lock_sha256",
                "selection_result_sha256",
                "disclosure",
                "selected",
            },
        )
        self.assert_valid(
            self.schema("resources/schemas/knowledge-context.schema.json"),
            context,
        )
        incomplete = copy.deepcopy(context)
        incomplete.pop("disclosure")
        self.assert_invalid(
            self.schema("resources/schemas/knowledge-context.schema.json"),
            incomplete,
        )

    def test_schema_keeps_legacy_context_and_manifest_readable(self) -> None:
        context = yaml.safe_load(
            (ROOT / "resources/templates/knowledge-context.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assert_valid(
            self.schema("resources/schemas/knowledge-context.schema.json"),
            context,
        )

        manifest = yaml.safe_load(
            (ROOT / "resources/templates/governance-run-manifest.yaml").read_text(
                encoding="utf-8"
            )
        )
        legacy = copy.deepcopy(manifest)
        legacy["run"].pop("telemetry", None)
        self.assert_valid(
            self.schema("resources/schemas/governance-run-manifest.schema.json"),
            legacy,
        )

    def test_telemetry_allows_unavailable_observations_without_gate_shape(
        self,
    ) -> None:
        manifest = yaml.safe_load(
            (ROOT / "resources/templates/governance-run-manifest.yaml").read_text(
                encoding="utf-8"
            )
        )
        manifest["run"]["telemetry"] = {
            "trust": "informational-only",
            "input_tokens": None,
            "output_tokens": None,
            "tool_calls": None,
            "cache": {"read": None, "write": None, "hit": None},
            "stages": [
                {
                    "id": "source-evidence",
                    "duration_ms": None,
                    "declared_context": {
                        "characters": None,
                        "sha256": None,
                        "hashes": [],
                    },
                    "input_tokens": None,
                    "output_tokens": None,
                    "cache": {"read": None, "write": None, "hit": None},
                    "tool_calls": None,
                    "source": {"paths": [], "bytes": None},
                }
            ],
            "source": {"paths": [], "bytes": None},
        }
        self.assert_valid(
            self.schema("resources/schemas/governance-run-manifest.schema.json"),
            manifest,
        )
        manifest["run"]["telemetry"].pop("trust")
        self.assert_invalid(
            self.schema("resources/schemas/governance-run-manifest.schema.json"),
            manifest,
        )


if __name__ == "__main__":
    unittest.main()
