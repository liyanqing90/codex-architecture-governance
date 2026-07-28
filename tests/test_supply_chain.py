from __future__ import annotations

import importlib.util
import json
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

            with zipfile.ZipFile(archive) as bundle:
                archive_names = {f"./{name}" for name in bundle.namelist()}
            sbom_names = {record["fileName"] for record in first["files"]}
            self.assertEqual(sbom_names, archive_names)

            packages = {record["name"]: record for record in first["packages"]}
            self.assertIn("codex-architecture-governance", packages)
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
