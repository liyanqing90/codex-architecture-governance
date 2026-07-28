#!/usr/bin/env python3
"""Validate Markdown knowledge packs and 0.2 read-only catalogs."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from architecture_tool import ArchitectureError
from architecture_tool import validate_knowledge as validate_legacy
from knowledge_model import KnowledgeError, validate_knowledge_tree

RESOURCE_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--knowledge-root",
        type=Path,
        default=RESOURCE_ROOT / "knowledge",
    )
    parser.add_argument("--today", type=date.fromisoformat)
    args = parser.parse_args()
    try:
        manifest, entries = validate_knowledge_tree(
            args.knowledge_root,
            schema_root=RESOURCE_ROOT / "schemas",
            today=args.today,
        )
        legacy = validate_legacy(today=args.today)
    except (ArchitectureError, KnowledgeError, OSError, ValueError) as exc:
        print(f"Knowledge validation failed: {exc}", file=sys.stderr)
        return 2
    print(
        "Knowledge validation passed: "
        f"{len(entries)} Markdown entries across "
        f"{len(manifest['packs'])} packs; "
        f"{legacy['entries']} legacy entries; "
        f"{legacy['rule_packs']} Rule Packs; "
        f"{legacy['providers']} Evidence Providers."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
