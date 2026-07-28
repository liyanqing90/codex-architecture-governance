#!/usr/bin/env python3
# ruff: noqa: E501
"""Migrate 0.2 YAML knowledge catalogs to Markdown frontmatter entries."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

KIND_MAP = {
    "quality-model": ("foundation", "foundations"),
    "domain-guidance": ("domain", "domains"),
    "decision-guide": ("decision-guide", "decision-guides"),
    "architecture-style": ("architecture-style", "architecture-styles"),
    "pattern": ("pattern", "patterns"),
    "technology-profile": ("technology-profile", "technology-profiles"),
    "reference-architecture": ("reference-architecture", "reference-architectures"),
    "migration": ("migration-guide", "migration-guides"),
}
PREFIX_MAP = {
    "foundation": "foundation",
    "domain": "domain",
    "decision-guide": "decision",
    "architecture-style": "style",
    "pattern": "pattern",
    "technology-profile": "technology",
    "reference-architecture": "reference",
    "migration-guide": "migration",
}


class MigrationError(RuntimeError):
    """Unsafe or invalid legacy knowledge migration."""


def sentence_list(value: Any, fallback: str) -> list[str]:
    if isinstance(value, list):
        result = [str(item).strip() for item in value if str(item).strip()]
        if result:
            return result
    return [fallback]


def bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def slug_tokens(value: str) -> list[str]:
    return list(
        dict.fromkeys(
            item for item in re.split(r"[^a-z0-9]+", value.lower()) if len(item) > 2
        )
    )


def metadata_for(kind: str, entry: dict[str, Any]) -> dict[str, Any]:
    canonical_kind, _ = KIND_MAP[kind]
    entry_id = str(entry["id"])
    sources = entry.get("sources", [])
    quality_attributes = [
        str(item).lower().replace("_", "-")
        for item in entry.get("quality_attributes", [])
    ]
    domains = [str(entry.get("category", "cross-cutting")).lower()]
    triggers = slug_tokens(entry_id) or ["architecture"]
    metadata: dict[str, Any] = {
        "id": f"{PREFIX_MAP[canonical_kind]}.{entry_id}",
        "kind": canonical_kind,
        "version": "1.0.0",
        "status": "active",
        "domains": domains,
        "triggers": triggers,
        "quality_attributes": quality_attributes,
        "related": [],
        "legacy_ids": [f"{kind}:{entry_id}"],
        "last_reviewed": entry["freshness"]["reviewed_on"],
        "review_after_days": entry["freshness"]["review_after_days"],
        "source_policy": (
            "official-docs-required"
            if canonical_kind == "technology-profile"
            else "stable-principles-plus-official-docs"
        ),
        "sources": sources,
    }
    if canonical_kind == "technology-profile":
        metadata["dynamic_facts"] = True
        metadata["version_range"] = (
            "Current supported stable releases; verify official documentation "
            "before a project decision."
        )
    return metadata


def body_for(entry: dict[str, Any]) -> str:
    name = str(entry["name"])
    intent = sentence_list(entry.get("intent"), f"Use {name} for its declared intent.")
    fit = sentence_list(entry.get("fit_when"), f"The stated problem matches {name}.")
    avoid = sentence_list(
        entry.get("avoid_when"),
        f"The project has not proven a need for {name}.",
    )
    benefits = sentence_list(
        entry.get("benefits"),
        f"Addresses the declared {name} problem.",
    )
    liabilities = sentence_list(
        entry.get("liabilities"),
        "Introduces implementation and operating complexity that must be owned.",
    )
    capabilities = sentence_list(
        entry.get("required_capabilities"),
        "An accountable owner, explicit contracts, tests, and operational evidence.",
    )
    warnings = sentence_list(
        entry.get("warning_signals"),
        "The mechanism is adopted by convention without a traced failure path.",
    )
    alternatives = sentence_list(
        entry.get("alternatives") or entry.get("implementation_options"),
        "Keep the current design and apply a smaller local correction.",
    )
    migrations = sentence_list(
        entry.get("migration_paths"),
        "Introduce the mechanism behind a compatible boundary, verify it, then remove the old path.",
    )
    mechanism = sentence_list(entry.get("decision_rules"), intent[0])
    tradeoffs = sentence_list(
        entry.get("quality_attributes"),
        "Balance business fit, reliability, maintainability, cost, and cognitive load.",
    )
    return f"""# {name}

## Problem and intent

{bullets(intent)}

## Mechanism

{bullets(mechanism)}

## Fit when

{bullets(fit)}

## Avoid when

{bullets(avoid)}

## Required capabilities

{bullets(capabilities)}

## Benefits

{bullets(benefits)}

## Costs and liabilities

{bullets(liabilities)}

## Failure modes

{bullets(warnings)}

## Alternatives

{bullets(alternatives)}

## Migration and exit

{bullets(migrations)}

## Evidence to inspect

- Trace the owning boundary, direct configuration or code, affected consumers, failure path, tests, and current operational evidence.
- For technology capabilities, confirm volatile behavior from the cited official source at decision time.

## Evidence that changes the recommendation

- A simpler option meeting the same measurable quality scenario should replace this recommendation.
- Missing ownership, compatibility, recovery, cost, or operational capability invalidates adoption until resolved.

## Quality trade-offs

{bullets(tradeoffs)}

## Volatile facts

- Product versions, support status, compatibility, security advisories, licensing, pricing, and service limits are time-sensitive and must be rechecked.
- Stable mechanism guidance remains separate from current vendor or release information.
"""


def destination_for(
    output_root: Path,
    legacy_kind: str,
    entry: dict[str, Any],
) -> Path:
    canonical_kind, directory = KIND_MAP[legacy_kind]
    entry_id = str(entry["id"])
    if canonical_kind == "domain":
        return output_root / directory / entry_id / "overview.md"
    return output_root / directory / f"{entry_id}.md"


def migrate(source_root: Path, output_root: Path, *, check: bool) -> int:
    generated = 0
    for source in sorted(source_root.rglob("*.yaml")):
        if source.name == "manifest.yaml":
            continue
        payload = yaml.safe_load(source.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("kind") not in KIND_MAP:
            continue
        for entry in payload["entries"]:
            destination = destination_for(output_root, payload["kind"], entry)
            metadata = metadata_for(payload["kind"], entry)
            rendered = (
                "---\n"
                + yaml.safe_dump(
                    metadata,
                    sort_keys=False,
                    allow_unicode=True,
                    width=88,
                )
                + "---\n\n"
                + body_for(entry)
            )
            if destination.exists():
                if destination.read_text(encoding="utf-8") != rendered:
                    raise MigrationError(
                        f"Refusing to overwrite divergent entry: {destination}"
                    )
            elif check:
                raise MigrationError(f"Missing migrated entry: {destination}")
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(rendered, encoding="utf-8")
            generated += 1
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        count = migrate(
            args.source_root.resolve(),
            args.output_root.resolve(),
            check=args.check,
        )
    except (MigrationError, OSError, yaml.YAMLError) as exc:
        print(f"Knowledge migration failed: {exc}")
        return 2
    print(
        f"Knowledge migration: {count} entries {'checked' if args.check else 'written'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
