from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", SCRIPT_PATH)
assert SPEC and SPEC.loader
validate_repository = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_repository)


class RepositoryContractTests(unittest.TestCase):
    def test_repository_contract(self) -> None:
        errors = validate_repository.validate_repository(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_floating_github_action_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow_root = root / ".github" / "workflows"
            workflow_root.mkdir(parents=True)
            (workflow_root / "ci.yml").write_text(
                "steps:\n  - uses: actions/checkout@v6\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            validate_repository.validate_github_action_pins(root, errors)
            self.assertEqual(len(errors), 1)
            self.assertIn("40-character commit SHA", errors[0])

    def test_duplicate_json_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "duplicate.json"
            path.write_text('{"schema_version": "1.0", "schema_version": "1.1"}')
            errors: list[str] = []
            self.assertIsNone(validate_repository.load_json(path, errors))
            self.assertEqual(len(errors), 1)
            self.assertIn("duplicate JSON key 'schema_version'", errors[0])

    def test_plugin_identity_is_independent_of_checkout_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "custom-checkout-name"
            shutil.copytree(ROOT / ".codex-plugin", root / ".codex-plugin")
            errors: list[str] = []
            manifest = validate_repository.validate_manifest(root, errors)
            self.assertIsNotNone(manifest)
            self.assertEqual(errors, [])

    def test_hengmu_entry_routes_every_focused_skill(self) -> None:
        entry = (ROOT / "skills" / "hengmu" / "SKILL.md").read_text(encoding="utf-8")
        focused_skills = set(validate_repository.EXPECTED_SKILLS) - {"hengmu"}
        for skill in focused_skills:
            self.assertIn(f"../{skill}/SKILL.md", entry)

    def test_hengmu_entry_preserves_direct_focused_invocation(self) -> None:
        entry = (ROOT / "skills" / "hengmu" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Keep all eight focused Skill names directly invocable", entry)
        self.assertIn("explicitly invokes a focused Skill", entry)
        self.assertIn("activate this router", entry)

    def test_readmes_document_each_supported_host_installation(self) -> None:
        expectations = {
            "README.md": (
                "## Install in your IDE",
                "### Codex and ChatGPT desktop",
                "### Cursor",
                "### VS Code and GitHub Copilot",
                "### Kiro",
                '"chat.pluginLocations"',
                "copilot plugin install qingye-lab/hengmu",
                'cp -R "$HENGMU_ROOT/resources/." .kiro/resources/',
            ),
            "README.zh-CN.md": (
                "## 在不同 IDE 中安装",
                "### Codex 与 ChatGPT 桌面端",
                "### Cursor",
                "### VS Code 与 GitHub Copilot",
                "### Kiro",
                '"chat.pluginLocations"',
                "copilot plugin install qingye-lab/hengmu",
                'cp -R "$HENGMU_ROOT/resources/." .kiro/resources/',
            ),
        }
        for path, required_text in expectations.items():
            readme = (ROOT / path).read_text(encoding="utf-8")
            for text in required_text:
                self.assertIn(text, readme, f"{path} must document {text!r}")


if __name__ == "__main__":
    unittest.main()
