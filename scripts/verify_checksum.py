#!/usr/bin/env python3
"""Verify a sha256sum-compatible checksum file on every supported platform."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def verify(checksum_path: Path) -> Path:
    checksum_path = checksum_path.resolve()
    parts = checksum_path.read_text(encoding="utf-8").strip().split(maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"{checksum_path} is not a sha256sum record")
    expected, raw_name = parts
    if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        raise ValueError(f"{checksum_path} has an invalid SHA-256 value")
    name = raw_name.lstrip("*")
    artifact = (checksum_path.parent / name).resolve()
    artifact.relative_to(checksum_path.parent)
    actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(
            f"{artifact} checksum mismatch: expected {expected}, observed {actual}"
        )
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checksum", type=Path, nargs="+")
    args = parser.parse_args()
    try:
        verified = [verify(path) for path in args.checksum]
    except (OSError, ValueError) as exc:
        print(f"Checksum verification failed: {exc}")
        return 1
    for path in verified:
        print(f"Verified SHA-256: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
