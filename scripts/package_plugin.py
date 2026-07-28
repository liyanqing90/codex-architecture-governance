#!/usr/bin/env python3
"""Build a deterministic, runtime-only plugin archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
RUNTIME_FILES = (
    Path(".codex-plugin/plugin.json"),
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


def load_identity(root: Path) -> tuple[str, str]:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PackageError(f"Missing plugin manifest: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise PackageError(f"Invalid plugin manifest: {exc}") from exc
    try:
        name = manifest["name"]
        version = manifest["version"]
    except (KeyError, TypeError) as exc:
        raise PackageError("Plugin manifest requires name and version") from exc
    if not isinstance(name, str) or not isinstance(version, str):
        raise PackageError("Plugin name and version must be strings")
    return name, version


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


def collect_runtime_files(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    files = list(RUNTIME_FILES)
    for directory in RUNTIME_DIRECTORIES:
        source = root / directory
        if not source.is_dir():
            raise PackageError(f"Missing runtime directory: {source}")
        if source.is_symlink():
            raise PackageError(f"Refusing to package symlinked directory: {source}")
        files.extend(
            path.relative_to(root)
            for path in source.rglob("*")
            if path.is_file() or path.is_symlink()
        )
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


def build_package(root: Path, output_dir: Path) -> tuple[Path, Path]:
    root = root.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    name, version = load_identity(root)
    files = collect_runtime_files(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{name}-{version}.zip"
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
            for relative in files:
                archive.writestr(
                    archive_info(relative),
                    (root / relative).read_bytes(),
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
        description="Build a deterministic Codex plugin archive."
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        archive_path, checksum_path = build_package(args.root, args.output_dir)
    except PackageError as exc:
        print(f"Packaging failed: {exc}")
        raise SystemExit(2) from exc
    print(f"Built {archive_path}")
    print(f"Checksum {checksum_path}")


if __name__ == "__main__":
    main()
