#!/usr/bin/env python3
"""Generate a deterministic SPDX 2.3 SBOM for a packaged plugin archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

PACKAGE_RE = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>[^\s\\]+)")
DEFAULT_LICENSE_POLICY = (
    Path(__file__).resolve().parent.parent
    / "resources"
    / "supply-chain"
    / "runtime-licenses.json"
)


class SbomError(RuntimeError):
    """Invalid input for SBOM generation."""


def digest_bytes(algorithm: str, value: bytes) -> str:
    return hashlib.new(algorithm, value).hexdigest()


def spdx_id(value: str) -> str:
    rendered = re.sub(r"[^A-Za-z0-9.-]+", "-", value).strip("-")
    return f"SPDXRef-{rendered or 'item'}"


def locked_packages(path: Path) -> list[tuple[str, str]]:
    packages: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = PACKAGE_RE.match(line.strip())
        if match is None:
            continue
        name = match.group("name")
        key = name.lower().replace("_", "-")
        version = match.group("version")
        previous = packages.get(key)
        if previous is not None and previous != version:
            raise SbomError(f"{path} pins {name} more than once")
        packages[key] = version
    if not packages:
        raise SbomError(f"{path} contains no exact package pins")
    return sorted(packages.items())


def load_licenses(path: Path) -> dict[str, str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        packages = payload["packages"]
    except (OSError, KeyError, json.JSONDecodeError, TypeError) as exc:
        raise SbomError(f"Cannot read license policy {path}: {exc}") from exc
    result = {
        name.lower().replace("_", "-"): record["license"]
        for name, record in packages.items()
    }
    if any(not value or value == "NOASSERTION" for value in result.values()):
        raise SbomError(f"{path} contains an unapproved license")
    return result


def build_sbom(
    archive_path: Path,
    lock_path: Path,
    license_policy_path: Path = DEFAULT_LICENSE_POLICY,
) -> dict[str, Any]:
    archive_path = archive_path.resolve()
    lock_path = lock_path.resolve()
    archive_sha256 = digest_bytes("sha256", archive_path.read_bytes())
    dependencies = locked_packages(lock_path)
    licenses = load_licenses(license_policy_path)
    dependency_names = {name for name, _ in dependencies}
    if set(licenses) != dependency_names:
        raise SbomError(
            "License policy package set does not match runtime dependency lock"
        )

    try:
        with zipfile.ZipFile(archive_path) as archive:
            names = sorted(archive.namelist())
            contents = {name: archive.read(name) for name in names}
    except (FileNotFoundError, zipfile.BadZipFile) as exc:
        raise SbomError(f"Cannot read plugin archive {archive_path}: {exc}") from exc
    if ".codex-plugin/plugin.json" not in contents:
        raise SbomError("Archive does not contain .codex-plugin/plugin.json")
    manifest = json.loads(contents[".codex-plugin/plugin.json"])
    plugin_name = manifest["name"]
    plugin_version = manifest["version"]
    plugin_id = spdx_id(f"Package-{plugin_name}")

    files: list[dict[str, Any]] = []
    verification_inputs: list[str] = []
    for index, name in enumerate(names, start=1):
        value = contents[name]
        sha1 = digest_bytes("sha1", value)
        verification_inputs.append(sha1)
        files.append(
            {
                "fileName": f"./{name}",
                "SPDXID": spdx_id(f"File-{index}-{name}"),
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": digest_bytes("sha256", value),
                    }
                ],
                "licenseConcluded": "NOASSERTION",
                "copyrightText": "NOASSERTION",
            }
        )

    packages: list[dict[str, Any]] = [
        {
            "name": plugin_name,
            "SPDXID": plugin_id,
            "versionInfo": plugin_version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": True,
            "packageVerificationCode": {
                "packageVerificationCodeValue": digest_bytes(
                    "sha1",
                    "".join(sorted(verification_inputs)).encode("ascii"),
                )
            },
            "licenseConcluded": "MIT",
            "licenseDeclared": "MIT",
            "copyrightText": "NOASSERTION",
            "checksums": [{"algorithm": "SHA256", "checksumValue": archive_sha256}],
        }
    ]
    relationships: list[dict[str, str]] = [
        {
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": plugin_id,
        }
    ]
    for name, version in dependencies:
        dependency_id = spdx_id(f"Package-Python-{name}")
        license_id = licenses[name]
        packages.append(
            {
                "name": name,
                "SPDXID": dependency_id,
                "versionInfo": version,
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": license_id,
                "licenseDeclared": license_id,
                "copyrightText": "NOASSERTION",
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": f"pkg:pypi/{name}@{version}",
                    }
                ],
            }
        )
        relationships.append(
            {
                "spdxElementId": plugin_id,
                "relationshipType": "DEPENDS_ON",
                "relatedSpdxElement": dependency_id,
            }
        )
    relationships.extend(
        {
            "spdxElementId": plugin_id,
            "relationshipType": "CONTAINS",
            "relatedSpdxElement": file_record["SPDXID"],
        }
        for file_record in files
    )
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"{plugin_name}-{plugin_version}",
        "documentNamespace": (
            "https://github.com/liyanqing90/codex-architecture-governance/"
            f"sbom/{archive_sha256}"
        ),
        "creationInfo": {
            "created": "1970-01-01T00:00:00Z",
            "creators": ["Tool: codex-architecture-governance-sbom-0.3.1"],
        },
        "documentDescribes": [plugin_id],
        "packages": packages,
        "files": files,
        "relationships": relationships,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument(
        "--lock",
        type=Path,
        default=Path("requirements-runtime.lock"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--license-policy",
        type=Path,
        default=DEFAULT_LICENSE_POLICY,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_sbom(args.archive, args.lock, args.license_policy)
    except (OSError, KeyError, json.JSONDecodeError, SbomError) as exc:
        print(f"SBOM generation failed: {exc}")
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote SPDX SBOM: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
