#!/usr/bin/env python3
"""Run the repository test suite for the deterministic Evidence Provider."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junitxml", required=True)
    args = parser.parse_args()
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", f"--junitxml={args.junitxml}"],
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
