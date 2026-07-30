from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


package_plugin = load_script("package_plugin", ROOT / "scripts" / "package_plugin.py")
generate_sbom = load_script("generate_sbom", ROOT / "scripts" / "generate_sbom.py")
audit_licenses = load_script("audit_licenses", ROOT / "scripts" / "audit_licenses.py")
verify_checksum = load_script(
    "verify_checksum",
    ROOT / "scripts" / "verify_checksum.py",
)


class SupplyChainTests(unittest.TestCase):
    def test_windows_pytest_dependency_is_explicitly_hash_locked(self) -> None:
        requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
        lock = (ROOT / "requirements-dev.lock").read_text(encoding="utf-8")
        self.assertIn(
            "colorama==0.4.6",
            requirements,
        )
        self.assertRegex(
            lock,
            re.compile(r"colorama==0\.4\.6\s*\\"),
        )
        self.assertIn(
            "typing-extensions==4.16.0",
            requirements,
        )
        self.assertRegex(
            lock,
            re.compile(r"typing-extensions==4\.16\.0\s*\\"),
        )
        self.assertIn(
            "pytest>=9.0.3,<10",
            requirements,
        )
        self.assertRegex(
            lock,
            re.compile(r"pytest==9\.1\.1\s*\\"),
        )

    def test_release_attestation_uses_exact_sbom_path(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("SBOM_PATH=dist/hengmu-", workflow)
        self.assertIn('--output "${SBOM_PATH}"', workflow)
        self.assertIn("sbom-path: ${{ env.SBOM_PATH }}", workflow)
        self.assertIn('"${SBOM_PATH}"', workflow)
        self.assertNotIn("sbom-path: dist/*.spdx.json", workflow)

    def test_checksum_and_sbom_cover_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            archive, checksum = package_plugin.build_package(ROOT, output)
            self.assertEqual(verify_checksum.verify(checksum), archive)

            first = generate_sbom.build_sbom(
                archive,
                ROOT / "requirements-runtime.lock",
            )
            second = generate_sbom.build_sbom(
                archive,
                ROOT / "requirements-runtime.lock",
            )
            self.assertEqual(first, second)
            self.assertEqual(first["spdxVersion"], "SPDX-2.3")
            plugin_version = next(
                record["versionInfo"]
                for record in first["packages"]
                if record["name"] == "hengmu"
            )
            self.assertEqual(
                first["creationInfo"]["creators"],
                [f"Tool: hengmu-sbom-{plugin_version}"],
            )

            with zipfile.ZipFile(archive) as bundle:
                archive_names = {f"./{name}" for name in bundle.namelist()}
            sbom_names = {record["fileName"] for record in first["files"]}
            self.assertEqual(sbom_names, archive_names)

            packages = {record["name"]: record for record in first["packages"]}
            self.assertIn("hengmu", packages)
            self.assertTrue(
                first["documentNamespace"].startswith(
                    "https://github.com/qingye-lab/hengmu/sbom/"
                )
            )
            self.assertIn("jsonschema", packages)
            self.assertIn("pyyaml", packages)
            self.assertFalse(
                any(
                    record["licenseDeclared"] == "NOASSERTION"
                    for record in first["packages"]
                )
            )
            json.dumps(first)

            audit = audit_licenses.audit(
                ROOT / "requirements-runtime.lock",
                ROOT / "resources" / "supply-chain" / "runtime-licenses.json",
            )
            self.assertEqual(audit["status"], "pass")
            self.assertEqual(len(audit["packages"]), 7)

    def test_checksum_rejects_tampered_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            archive, checksum = package_plugin.build_package(ROOT, output)
            archive.write_bytes(archive.read_bytes() + b"tamper")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                verify_checksum.verify(checksum)

    def test_sbom_requires_exact_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            archive, _ = package_plugin.build_package(ROOT, output)
            unlocked = output / "requirements.txt"
            unlocked.write_text("PyYAML>=6,<7\n", encoding="utf-8")
            with self.assertRaisesRegex(generate_sbom.SbomError, "no exact"):
                generate_sbom.build_sbom(archive, unlocked)


if __name__ == "__main__":
    unittest.main()
