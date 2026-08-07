#!/usr/bin/env python3
"""Build a deterministic, runtime-only plugin archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path

FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
CODEX_MANIFEST_PATH = Path(".codex-plugin/plugin.json")
AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PORTABLE_MANIFEST_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
PORTABLE_DESCRIPTION = (
    "Evidence-bound architecture review and target design for Codex and "
    "compatible Agent Plugins, with verification, decisions, remediation "
    "plans, and deterministic quality gates."
)
PORTABLE_KEYWORDS = (
    "agent-plugins",
    "agent-skills",
    "architecture",
    "architecture-governance",
    "architecture-review",
    "codex",
    "cursor",
    "developer-tools",
    "governance",
    "quality-gate",
)
COMMON_RUNTIME_FILES = (
    Path("LICENSE"),
    Path("NOTICE"),
    Path("requirements-runtime.lock"),
    Path("requirements.txt"),
    Path("third_party/PAAD-MIT.txt"),
)
RUNTIME_DIRECTORIES = (Path("resources"), Path("skills"))
FORBIDDEN_PARTS = {"__pycache__"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


class PackageError(RuntimeError):
    """Invalid package source or output."""


def load_codex_manifest(root: Path) -> dict[str, object]:
    manifest_path = root / CODEX_MANIFEST_PATH
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PackageError(f"Missing plugin manifest: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise PackageError(f"Invalid plugin manifest: {exc}") from exc
    if not isinstance(manifest, dict):
        raise PackageError(f"Plugin manifest must be an object: {manifest_path}")
    return manifest


def load_identity(root: Path) -> tuple[str, str]:
    manifest = load_codex_manifest(root)
    try:
        name = manifest["name"]
        version = manifest["version"]
    except (KeyError, TypeError) as exc:
        raise PackageError("Plugin manifest requires name and version") from exc
    if not isinstance(name, str) or not isinstance(version, str):
        raise PackageError("Plugin name and version must be strings")
    return name, version


def portable_manifest(codex_manifest: dict[str, object]) -> dict[str, object]:
    """Project the Codex manifest onto the Agent Plugins portable contract."""

    manifest: dict[str, object] = {
        "$schema": AGENT_PLUGINS_SCHEMA,
        "name": codex_manifest.get("name"),
        "description": PORTABLE_DESCRIPTION,
        "keywords": list(PORTABLE_KEYWORDS),
    }
    for key in (
        "version",
        "author",
        "homepage",
        "repository",
        "license",
        "extensions",
    ):
        if key in codex_manifest:
            manifest[key] = codex_manifest[key]
    validate_portable_manifest(manifest)
    return manifest


def validate_portable_manifest(manifest: dict[str, object]) -> None:
    """Validate the portable fields needed by Agent Plugins 1.0.0."""

    unknown = sorted(set(manifest) - PORTABLE_MANIFEST_FIELDS)
    if unknown:
        raise PackageError(
            "Agent Plugins manifest has unknown top-level fields: " + ", ".join(unknown)
        )
    if manifest.get("$schema") != AGENT_PLUGINS_SCHEMA:
        raise PackageError("Agent Plugins manifest has the wrong $schema")

    name = manifest.get("name")
    if (
        not isinstance(name, str)
        or not 1 <= len(name) <= 64
        or re.fullmatch(r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", name)
        is None
    ):
        raise PackageError("Agent Plugins manifest has an invalid name")

    for key in (
        "version",
        "description",
        "homepage",
        "repository",
        "license",
    ):
        if key in manifest and not isinstance(manifest[key], str):
            raise PackageError(f"Agent Plugins manifest field {key!r} must be a string")

    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict) or set(author) - {"name", "email", "url"}:
            raise PackageError("Agent Plugins manifest author is invalid")
        if not all(isinstance(value, str) for value in author.values()):
            raise PackageError("Agent Plugins manifest author values must be strings")

    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list)
        or not all(isinstance(value, str) for value in keywords)
    ):
        raise PackageError("Agent Plugins manifest keywords must be strings")

    extensions = manifest.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict)
        or not all(isinstance(value, dict) for value in extensions.values())
    ):
        raise PackageError("Agent Plugins manifest extensions must be objects")


def assert_runtime_file(root: Path, path: Path) -> None:
    absolute = root / path
    if absolute.is_symlink():
        raise PackageError(f"Refusing to package symlink: {absolute}")
    if not absolute.is_file():
        raise PackageError(f"Missing runtime file: {absolute}")
    if FORBIDDEN_PARTS.intersection(path.parts):
        raise PackageError(f"Refusing to package cache path: {absolute}")
    if path.suffix in FORBIDDEN_SUFFIXES or path.name == ".DS_Store":
        raise PackageError(f"Refusing to package development artifact: {absolute}")


def collect_runtime_files(root: Path, package_format: str = "codex") -> list[Path]:
    root = root.expanduser().resolve()
    files = list(COMMON_RUNTIME_FILES)
    if package_format == "codex":
        files.append(CODEX_MANIFEST_PATH)
    elif package_format != "agent-plugins":
        raise PackageError(f"Unsupported package format: {package_format}")
    for directory in RUNTIME_DIRECTORIES:
        source = root / directory
        if not source.is_dir():
            raise PackageError(f"Missing runtime directory: {source}")
        if source.is_symlink():
            raise PackageError(f"Refusing to package symlinked directory: {source}")
        for path in source.rglob("*"):
            relative = path.relative_to(root)
            if (
                (path.is_file() or path.is_symlink())
                and not FORBIDDEN_PARTS.intersection(relative.parts)
                and path.suffix not in FORBIDDEN_SUFFIXES
                and path.name != ".DS_Store"
            ):
                if package_format == "agent-plugins" and relative.parts[-2:] == (
                    "agents",
                    "openai.yaml",
                ):
                    continue
                files.append(relative)
    unique = sorted(set(files), key=lambda path: path.as_posix())
    for path in unique:
        assert_runtime_file(root, path)
    return unique


def archive_info(path: Path) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(path.as_posix(), FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    mode = 0o755 if path.suffix == ".py" else 0o644
    info.external_attr = mode << 16
    return info


def build_package(
    root: Path,
    output_dir: Path,
    package_format: str = "codex",
) -> tuple[Path, Path]:
    root = root.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    codex_manifest = load_codex_manifest(root)
    name, version = load_identity(root)
    files = collect_runtime_files(root, package_format)
    payloads = {path.as_posix(): (root / path).read_bytes() for path in files}
    if package_format == "agent-plugins":
        payloads["plugin.json"] = (
            json.dumps(
                portable_manifest(codex_manifest),
                indent=2,
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )
    elif package_format != "codex":
        raise PackageError(f"Unsupported package format: {package_format}")
    entries = sorted(payloads.items())
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = "" if package_format == "codex" else "-agent-plugins"
    archive_path = output_dir / f"{name}-{version}{suffix}.zip"
    checksum_path = archive_path.with_suffix(".zip.sha256")

    with tempfile.NamedTemporaryFile(
        prefix=f".{name}-",
        suffix=".zip",
        dir=output_dir,
        delete=False,
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(
            temporary_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for relative, payload in entries:
                archive_path_name = Path(relative)
                archive.writestr(
                    archive_info(archive_path_name),
                    payload,
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
        temporary_path.replace(archive_path)
    finally:
        temporary_path.unlink(missing_ok=True)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path.write_text(
        f"{digest}  {archive_path.name}\n",
        encoding="utf-8",
    )
    return archive_path, checksum_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a deterministic runtime-only plugin archive."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Plugin root; defaults to the parent of scripts/.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for the ZIP and SHA-256 checksum.",
    )
    parser.add_argument(
        "--format",
        dest="package_format",
        choices=("codex", "agent-plugins"),
        default="codex",
        help="Package contract to emit; defaults to the native Codex format.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        archive_path, checksum_path = build_package(
            args.root,
            args.output_dir,
            args.package_format,
        )
    except PackageError as exc:
        print(f"Packaging failed: {exc}")
        raise SystemExit(2) from exc
    print(f"Built {archive_path}")
    print(f"Checksum {checksum_path}")


if __name__ == "__main__":
    main()
