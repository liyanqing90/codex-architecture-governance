#!/usr/bin/env python3
"""Build a project profile while preserving detected, declared, and inferred sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

RESOURCE_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_ROOT = RESOURCE_ROOT / "schemas"
CONTRIBUTING_FACT_ROLES = {"runtime", "production"}


class ProfileBuildError(RuntimeError):
    """Invalid or unsafe project-profile construction."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProfileBuildError(f"Missing file: {path}") from exc
    except yaml.YAMLError as exc:
        raise ProfileBuildError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProfileBuildError(f"Expected YAML mapping in {path}")
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fact_ids(facts: dict[str, Any], field: str) -> set[str]:
    return {
        str(item["id"])
        for item in facts.get(field, [])
        if _fact_contributes(facts, item)
    }


def _fact_contributes(facts: dict[str, Any], fact: dict[str, Any]) -> bool:
    # Version 1.0 predates fact roles.  Keep its all-facts-contribute
    # interpretation even if a hand-maintained historical record happens to
    # include a role-like field; applying 1.1 semantics retroactively would
    # silently change its recorded routing.
    if facts.get("schema_version") == "1.0":
        return True
    role = fact.get("role")
    return str(role) in CONTRIBUTING_FACT_ROLES


def derive_domains(facts: dict[str, Any]) -> list[str]:
    languages = fact_ids(facts, "languages")
    frameworks = fact_ids(facts, "frameworks")
    storage = fact_ids(facts, "storage")
    interfaces = fact_ids(facts, "interfaces")
    infrastructure = fact_ids(facts, "infrastructure")
    # A Domain Pack is product context, not a generic property of every
    # repository.  Start empty so that non-contributing observations (tests,
    # fixtures, examples, documentation, generated code, and vendor trees)
    # cannot route an otherwise context-free repository into a domain pack.
    # Broad architecture foundations remain selected by the requesting Skill.
    domains: set[str] = set()
    if frameworks & {"react", "nextjs", "vue", "astro", "vite"}:
        domains.add("frontend")
    if frameworks & {
        "aspnet-core",
        "django",
        "fastapi",
        "nestjs",
        "spring-boot",
    } or interfaces & {"rest", "graphql", "grpc"}:
        domains.add("backend-api")
    if storage:
        domains.add("data")
    if frameworks & {
        "langgraph",
        "microsoft-agent-framework",
        "openai-agents-sdk",
    }:
        domains.add("ai-agent")
    if languages & {"swift", "dart", "kotlin"}:
        domains.add("mobile")
    if infrastructure & {
        "apache-kafka",
        "kubernetes",
        "nats",
        "rabbitmq",
    }:
        domains.add("distributed-systems")
    return sorted(domains)


def derive_types(domains: list[str]) -> list[str]:
    types: set[str] = set()
    if "frontend" in domains:
        types.add("web-application")
    if "backend-api" in domains:
        types.add("service")
    if "ai-agent" in domains:
        types.add("ai-agent-platform")
    if "mobile" in domains:
        types.add("mobile-application")
    if not types:
        types.add("software-project")
    return sorted(types)


def derive_review_contract(
    domains: list[str],
) -> tuple[list[str], list[dict[str, Any]], list[str]]:
    specialist_packs = [
        pack
        for domain, pack in (
            ("frontend", "web-frontend"),
            ("backend-api", "backend-api"),
            ("data", "data-platform"),
            ("distributed-systems", "cloud-native-platform"),
        )
        if domain in domains
    ]
    project_packs = ["project-core", *specialist_packs]
    required_reviews = ["project-architecture"]
    requirements: list[dict[str, Any]] = [
        {
            "id": "project-architecture",
            "kind": "project",
            "rule_packs": project_packs,
        }
    ]
    packs = list(project_packs)
    if "ai-agent" in domains:
        required_reviews.append("ai-agent-architecture")
        requirements.append(
            {
                "id": "ai-agent-architecture",
                "kind": "ai-agent",
                "rule_packs": ["ai-agent-core"],
            }
        )
        packs.append("ai-agent-core")
    if "mobile" in domains:
        required_reviews.append("mobile-architecture")
        requirements.append(
            {
                "id": "mobile-architecture",
                "kind": "mobile",
                "rule_packs": ["mobile-core"],
            }
        )
        packs.append("mobile-core")
    return required_reviews, requirements, packs


def default_project(facts: dict[str, Any], facts_path: Path) -> dict[str, Any]:
    declared_root = Path(facts["repository"]["root"])
    if declared_root == Path():
        root = (
            facts_path.parent.parent
            if facts_path.parent.name == ".architecture"
            else facts_path.parent
        )
    else:
        root = declared_root.expanduser().resolve()
    try:
        facts_reference = facts_path.relative_to(root).as_posix()
    except ValueError:
        facts_reference = str(facts_path)
    project_id = root.name.lower().replace("_", "-").replace(" ", "-")
    project_id = "".join(
        character
        for character in project_id
        if character.isascii() and (character.isalnum() or character == "-")
    ).strip("-")
    if len(project_id) < 3:
        project_id = "architecture-project"
    project_id = project_id[:63].rstrip("-")
    domains = derive_domains(facts)
    types = derive_types(domains)
    required_reviews, requirements, packs = derive_review_contract(domains)
    evidence_paths = sorted(
        {
            item
            for field in (
                "languages",
                "frameworks",
                "storage",
                "interfaces",
                "infrastructure",
            )
            for record in facts[field]
            if _fact_contributes(facts, record)
            for item in record["evidence"]
        }
    )
    return {
        "id": project_id,
        "name": root.name,
        "type": types,
        "lifecycle": "active",
        "criticality": "medium",
        "owners": ["unassigned"],
        "critical_qualities": ["maintainability", "recoverability"],
        "quality_attributes": [
            {
                "id": "maintainability",
                "priority": "high",
                "rationale": "Changes must remain bounded to an accountable owner.",
                "target": {"architecture_boundary_tests": "required"},
                "evidence": ["Repository architecture tests"],
                "scenario": {
                    "source": "A maintainer changes one owned module.",
                    "trigger": "A feature or correction changes module behavior.",
                    "environment": "Normal development and CI.",
                    "target": "The owning module and its public boundary.",
                    "response": (
                        "The change remains bounded and violations fail "
                        "deterministically."
                    ),
                    "measure": "Architecture boundary checks pass.",
                },
            },
            {
                "id": "reliability.recoverability",
                "priority": "high",
                "rationale": "Critical work must reach an explicit terminal outcome.",
                "target": {"recovery_test": "required"},
                "evidence": ["Critical-flow recovery tests"],
                "scenario": {
                    "source": "An expected interruption occurs.",
                    "trigger": "A critical flow is interrupted after work begins.",
                    "environment": "Normal operation under a declared failure.",
                    "target": "The critical-flow state owner.",
                    "response": "The flow resumes, compensates, or terminates safely.",
                    "measure": "Recovery tests prove no duplicate irreversible effect.",
                },
            },
        ],
        "business_context": {
            "product_stage": "early",
            "team_count": 1,
            "ownership_model": "One provisional accountable product team.",
            "operational_maturity": "medium",
            "distributed_system_experience": "unknown",
            "on_call": False,
            "change_frequency": "unknown",
            "regulatory_constraints": [],
            "user_scale": "Unknown; declare before scale-sensitive decisions.",
            "throughput": "Unknown; require runtime evidence before optimization.",
            "latency_targets": "Unknown; define per critical flow.",
            "availability_target": "Unknown; define per critical flow.",
            "data_volume": "Unknown; require measured evidence.",
            "consistency": "Define per authoritative data flow.",
            "offline_requirement": "unknown",
            "deployment_model": "Detected from repository facts; confirm with owners.",
            "budget": "unknown",
            "deadlines": "Unknown; confirm before migration planning.",
            "required_stack": sorted(fact_ids(facts, "frameworks")),
            "prohibited_services": [],
            "migration_limits": ["Preserve public and persisted contracts."],
        },
        "repository_facts": {
            "path": facts_reference,
            "sha256": file_sha256(facts_path),
        },
        "required_knowledge_domains": domains,
        "profile_sources": {
            "detected": [facts_reference],
            "declared": [],
            "inferred": [
                {
                    "inference": (
                        "Project domains and types inferred from detected files "
                        "and dependencies."
                    ),
                    "confidence": 0.8 if evidence_paths else 0.35,
                    "basis": evidence_paths or ["No recognized manifest evidence."],
                },
                {
                    "inference": "One provisional team and medium operations maturity.",
                    "confidence": 0.25,
                    "basis": ["No declared team or operating model was supplied."],
                },
            ],
        },
        "required_reviews": required_reviews,
        "review_requirements": requirements,
        "rule_packs": packs,
        "data_classification": "internal",
        "constraints_file": ".architecture/constraints.md",
        "critical_flows_file": ".architecture/critical-flows.md",
        "review_output": ".architecture/reviews",
    }


def build_profile(
    facts_path: Path,
    *,
    declared_path: Path | None = None,
) -> dict[str, Any]:
    facts_path = facts_path.expanduser().resolve()
    facts = load_yaml(facts_path)
    facts_schema = json.loads(
        (SCHEMA_ROOT / "repository-facts.schema.json").read_text(encoding="utf-8")
    )
    facts_errors = list(Draft202012Validator(facts_schema).iter_errors(facts))
    if facts_errors:
        raise ProfileBuildError(
            f"{facts_path} is not valid repository facts: {facts_errors[0].message}"
        )
    if declared_path is None:
        project = default_project(facts, facts_path)
    else:
        declared_path = declared_path.expanduser().resolve()
        declared = load_yaml(declared_path)
        declared_root = Path(facts["repository"]["root"])
        project_root = (
            (
                facts_path.parent.parent
                if facts_path.parent.name == ".architecture"
                else facts_path.parent
            )
            if declared_root == Path()
            else declared_root.expanduser().resolve()
        )
        try:
            declared_reference = declared_path.relative_to(project_root).as_posix()
        except ValueError:
            declared_reference = str(declared_path)
        project = dict(declared.get("project", declared))
        required_fields = {"id", "name", "type", "owners"}
        missing = sorted(required_fields - set(project))
        if missing:
            raise ProfileBuildError(
                f"{declared_path} lacks declared profile fields: " + ", ".join(missing)
            )
        defaults = default_project(facts, facts_path)
        for key, value in defaults.items():
            project.setdefault(key, value)
        project["repository_facts"] = defaults["repository_facts"]
        project["required_knowledge_domains"] = sorted(
            set(project.get("required_knowledge_domains", []))
            | set(defaults["required_knowledge_domains"])
        )
        sources = project.get("profile_sources", defaults["profile_sources"])
        sources["detected"] = sorted(
            set(sources.get("detected", [])) | {str(facts_path)}
        )
        sources["declared"] = sorted(
            set(sources.get("declared", [])) | {declared_reference}
        )
        project["profile_sources"] = sources
    result = {"schema_version": "1.1", "project": project}
    schema = json.loads(
        (SCHEMA_ROOT / "project-profile.schema.json").read_text(encoding="utf-8")
    )
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(result),
        key=lambda error: tuple(str(item) for item in error.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'.'.join(str(item) for item in error.absolute_path) or '<root>'}: "
            f"{error.message}"
            for error in errors[:10]
        )
        raise ProfileBuildError(f"Generated profile is invalid: {details}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--facts", type=Path, required=True)
    parser.add_argument("--declared", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        profile = build_profile(args.facts, declared_path=args.declared)
        output = args.output.expanduser().resolve()
        if output.exists() and not args.force:
            raise ProfileBuildError(
                f"Refusing to overwrite existing output without --force: {output}"
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            yaml.safe_dump(profile, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except (ProfileBuildError, OSError) as exc:
        print(f"Project profile build failed: {exc}", file=sys.stderr)
        return 2
    print(f"Project profile written: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
