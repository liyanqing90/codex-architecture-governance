from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "package_plugin.py"
SPEC = importlib.util.spec_from_file_location("package_plugin", SCRIPT_PATH)
assert SPEC and SPEC.loader
package_plugin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_plugin)


class PackagePluginTests(unittest.TestCase):
    def test_archive_is_reproducible_and_runtime_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp_root = Path(temporary)
            first, first_checksum = package_plugin.build_package(
                ROOT,
                temp_root / "first",
            )
            second, _ = package_plugin.build_package(
                ROOT,
                temp_root / "second",
            )

            self.assertEqual(first.read_bytes(), second.read_bytes())
            digest = hashlib.sha256(first.read_bytes()).hexdigest()
            self.assertEqual(
                first_checksum.read_text(encoding="utf-8"),
                f"{digest}  {first.name}\n",
            )

            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
                timestamps = {item.date_time for item in archive.infolist()}

            self.assertEqual(names, sorted(names))
            self.assertIn(".codex-plugin/plugin.json", names)
            self.assertIn("resources/scripts/architecture_tool.py", names)
            self.assertIn("resources/selector-source.json", names)
            self.assertIn("resources/templates/knowledge-context.yaml", names)
            self.assertIn("skills/project-architecture-audit/SKILL.md", names)
            self.assertIn("LICENSE", names)
            self.assertIn("NOTICE", names)
            self.assertIn("requirements.txt", names)
            self.assertIn("requirements-runtime.lock", names)
            self.assertEqual(timestamps, {package_plugin.FIXED_ZIP_TIME})
            self.assertFalse(any(name.startswith(".architecture/") for name in names))
            self.assertFalse(any(name.startswith("scripts/") for name in names))
            self.assertFalse(any(name.startswith("tests/") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".pyc") for name in names))


if __name__ == "__main__":
    unittest.main()
