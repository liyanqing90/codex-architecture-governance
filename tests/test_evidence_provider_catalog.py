from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "resources" / "evidence-providers" / "catalog.yaml"
CATALOG_SCHEMA_PATH = ROOT / "resources" / "schemas" / "evidence-provider.schema.json"
TEMPLATE_PATH = ROOT / "resources" / "templates" / "evidence-providers.yaml"
CONFIG_SCHEMA_PATH = (
    ROOT / "resources" / "schemas" / "evidence-provider-config.schema.json"
)


class EvidenceProviderCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
        self.template = yaml.safe_load(TEMPLATE_PATH.read_text(encoding="utf-8"))

    def test_catalog_and_template_validate_as_schema_1_1(self) -> None:
        self.assertEqual(self.catalog["schema_version"], "1.1")
        self.assertEqual(self.template["schema_version"], "1.1")
        self._assert_valid(self.catalog, CATALOG_SCHEMA_PATH)
        self._assert_valid(self.template, CONFIG_SCHEMA_PATH)

    def test_quality_catalog_is_cross_language_and_advisory_only(self) -> None:
        providers = {provider["id"]: provider for provider in self.catalog["providers"]}
        expected = {
            "ruff": "python",
            "eslint": "javascript-typescript",
            "clippy": "rust",
            "golangci-lint": "go",
            "swiftlint": "swift",
            "detekt": "jvm",
        }
        self.assertEqual(
            {
                provider_id: providers[provider_id]["ecosystem"]
                for provider_id in expected
            },
            expected,
        )
        for provider_id in expected:
            provider = providers[provider_id]
            self.assertEqual(provider["category"], "quality")
            self.assertTrue(provider["documentation"].startswith("https://"))
            self.assertIn("explicit", provider["missing_tool_guidance"])
            self.assertNotIn("install_command", provider)

    def test_quality_commands_do_not_embed_installers(self) -> None:
        providers = {provider["id"]: provider for provider in self.catalog["providers"]}
        forbidden_actions = (
            "npx",
            "pip install",
            "npm install",
            "npm i ",
            "brew install",
            "cargo install",
            "go install",
            "curl ",
            "wget ",
        )
        for provider_id in providers:
            command = " ".join(providers[provider_id]["command"]).lower()
            self.assertFalse(
                any(action in command for action in forbidden_actions),
                f"{provider_id} embeds an installation action: {command}",
            )
        self.assertIn("--offline", providers["clippy"]["command"])
        self.assertIn("--offline", providers["detekt"]["command"])

        project_config = yaml.safe_load(
            (ROOT / ".architecture" / "evidence-providers.yaml").read_text(
                encoding="utf-8"
            )
        )
        for provider in project_config["providers"]:
            command = " ".join(provider["command"]).lower()
            self.assertFalse(
                any(action in command for action in forbidden_actions),
                f"project provider {provider['id']} embeds an installation action",
            )
        archunit = next(
            item for item in project_config["providers"] if item["id"] == "archunit"
        )
        self.assertEqual(archunit["command"][0], "mvn")
        self.assertIn("--offline", archunit["command"])

    def test_template_covers_every_catalog_provider_and_keeps_quality_disabled(
        self,
    ) -> None:
        catalog_ids = {provider["id"] for provider in self.catalog["providers"]}
        template_providers = {
            provider["id"]: provider for provider in self.template["providers"]
        }
        self.assertEqual(set(template_providers), catalog_ids)
        for provider_id in (
            "ruff",
            "eslint",
            "clippy",
            "golangci-lint",
            "swiftlint",
            "detekt",
        ):
            self.assertFalse(template_providers[provider_id]["enabled"])
            self.assertFalse(template_providers[provider_id]["allow_without_detection"])

    @staticmethod
    def _assert_valid(payload: dict, schema_path: Path) -> None:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
                payload
            ),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            raise AssertionError("\n".join(error.message for error in errors))


if __name__ == "__main__":
    unittest.main()
