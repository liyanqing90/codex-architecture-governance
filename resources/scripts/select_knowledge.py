#!/usr/bin/env python3
"""Select relevant architecture knowledge with deterministic, explainable rules."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from knowledge_model import KnowledgeEntry, validate_knowledge_tree

RESOURCE_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_ROOT = RESOURCE_ROOT / "knowledge"
SCHEMA_ROOT = RESOURCE_ROOT / "schemas"
CANONICAL_DOMAIN_ID_MAP = {
    "ai-agent": "domain.ai-agent",
    "backend-api": "domain.backend-api",
    "cloud-native-platform": "domain.cloud-native-platform",
    "data-platform": "domain.data-platform",
    "identity": "domain.identity",
    "mobile": "domain.mobile",
    "plugin-platform": "domain.plugin-platform",
    "real-time-system": "domain.real-time-system",
    "test-automation-platform": "domain.test-automation-platform",
    "web-frontend": "domain.web-frontend",
}
# Entry metadata and pre-1.1 profiles used these short domain names.  They are
# normalized only for compatibility; quality names such as reliability or
# security are deliberately not coerced into unrelated product domains.
LEGACY_DOMAIN_ALIASES = {
    "data": "data-platform",
    "delivery": "cloud-native-platform",
    "frontend": "web-frontend",
    "testing": "test-automation-platform",
}
SKILL_REQUIRED = {
    "project-architecture-audit": (
        "foundation.quality-attributes",
        "foundation.evidence-reasoning",
        "foundation.proportional-design",
        "foundation.system-boundaries",
        "foundation.data-ownership",
    ),
    "architecture-solution-advisor": (
        "foundation.quality-attributes",
        "foundation.tradeoff-analysis",
        "foundation.proportional-design",
        "foundation.technology-selection",
        "foundation.evolutionary-architecture",
    ),
    "architecture-finding-verifier": (
        "foundation.evidence-reasoning",
        "foundation.quality-attributes",
    ),
    "architecture-remediation-planner": (
        "foundation.evolutionary-architecture",
        "foundation.tradeoff-analysis",
    ),
    "ai-agent-architecture-audit": (
        "foundation.evidence-reasoning",
        "domain.ai-agent",
        "decision.workflow-vs-agent",
        "decision.single-agent-vs-multi-agent",
    ),
    "mobile-architecture-audit": (
        "foundation.evidence-reasoning",
        "domain.mobile",
        "decision.local-first-vs-server-first",
    ),
    "portfolio-architecture-audit": (
        "foundation.system-boundaries",
        "foundation.technology-selection",
        "anti-pattern.premature-generic-platform",
    ),
}
TECHNOLOGY_ALIASES = {
    "apache-kafka": "technology.apache-kafka",
    "openai-agents-sdk": "technology.openai-agents-sdk",
    "postgresql": "technology.postgresql",
    "redis-valkey": "technology.redis",
}
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "from",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}
SELECTION_THRESHOLD = 20
GENERIC_TRIGGER_TOKENS = {
    "architecture",
    "data",
    "design",
    "deterministic",
    "knowledge",
    "platform",
    "runtime",
    "service",
    "system",
}


class SelectionError(RuntimeError):
    """Invalid knowledge selection input or result."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SelectionError(f"Missing YAML file: {path}") from exc
    except yaml.YAMLError as exc:
        raise SelectionError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SelectionError(f"Expected YAML mapping in {path}")
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-z0-9.+-]+", value.lower())
        if len(token) > 1 and token not in STOP_WORDS
    }


def fact_ids(facts: dict[str, Any], field: str) -> set[str]:
    return {str(item["id"]) for item in facts.get(field, [])}


def canonical_domain(value: str) -> str:
    return LEGACY_DOMAIN_ALIASES.get(value, value)


def select_knowledge(
    facts_path: Path,
    *,
    profile_path: Path | None,
    task: str,
    skill: str,
    maximum_entries: int,
    includes: list[str] | None = None,
    excludes: list[str] | None = None,
) -> dict[str, Any]:
    if maximum_entries < 1:
        raise SelectionError("maximum_entries must be positive")
    facts_path = facts_path.expanduser().resolve()
    facts = load_yaml(facts_path)
    facts_schema = json.loads(
        (SCHEMA_ROOT / "repository-facts.schema.json").read_text(encoding="utf-8")
    )
    facts_errors = list(Draft202012Validator(facts_schema).iter_errors(facts))
    if facts_errors:
        raise SelectionError(
            f"{facts_path} is not valid repository facts: {facts_errors[0].message}"
        )
    profile: dict[str, Any] | None = None
    if profile_path is not None:
        profile_path = profile_path.expanduser().resolve()
        profile = load_yaml(profile_path)
        profile_schema = json.loads(
            (SCHEMA_ROOT / "project-profile.schema.json").read_text(encoding="utf-8")
        )
        profile_errors = list(
            Draft202012Validator(
                profile_schema,
                format_checker=FormatChecker(),
            ).iter_errors(profile)
        )
        if profile_errors:
            raise SelectionError(
                f"{profile_path} is not a valid profile: {profile_errors[0].message}"
            )
    _, entries = validate_knowledge_tree(
        KNOWLEDGE_ROOT,
        schema_root=SCHEMA_ROOT,
    )
    includes = includes or []
    excludes = excludes or []
    unknown_includes = sorted(set(includes) - set(entries))
    unknown_excludes = sorted(set(excludes) - set(entries))
    if unknown_includes or unknown_excludes:
        raise SelectionError(
            "Unknown knowledge IDs: " + ", ".join(unknown_includes + unknown_excludes)
        )
    overlap = sorted(set(includes) & set(excludes))
    if overlap:
        raise SelectionError(
            "Knowledge IDs cannot be both included and excluded: " + ", ".join(overlap)
        )
    scores: dict[str, int] = dict.fromkeys(entries, 0)
    reasons: dict[str, set[str]] = {entry_id: set() for entry_id in entries}
    priorities: dict[str, str] = dict.fromkeys(entries, "recommended")

    def add(
        entry_id: str,
        score: int,
        reason: str,
        *,
        priority: str = "recommended",
    ) -> None:
        if entry_id not in entries or entry_id in excludes:
            return
        scores[entry_id] += score
        reasons[entry_id].add(reason)
        priority_rank = {"optional": 0, "recommended": 1, "required": 2}
        if priority_rank[priority] > priority_rank[priorities[entry_id]]:
            priorities[entry_id] = priority

    for entry_id in SKILL_REQUIRED.get(skill, ()):
        add(
            entry_id,
            100,
            f"Required foundation or lens for {skill}.",
            priority="required",
        )
    for entry_id in includes:
        add(entry_id, 1000, "Explicit caller include.", priority="required")

    profile_domains: set[str] = set()
    if profile is not None:
        profile_domains.update(
            canonical_domain(str(item))
            for item in profile["project"].get("required_knowledge_domains", [])
        )
    project_domains = set(profile_domains)
    frameworks = fact_ids(facts, "frameworks")
    storage = fact_ids(facts, "storage")
    infrastructure = fact_ids(facts, "infrastructure")
    languages = fact_ids(facts, "languages")
    if frameworks & {"react", "nextjs", "vue", "astro", "vite"}:
        project_domains.add("web-frontend")
    if frameworks & {
        "aspnet-core",
        "django",
        "fastapi",
        "nestjs",
        "spring-boot",
    }:
        project_domains.add("backend-api")
    if frameworks & {
        "langgraph",
        "microsoft-agent-framework",
        "openai-agents-sdk",
    }:
        project_domains.add("ai-agent")
    if storage:
        project_domains.add("data-platform")
    if languages & {"dart", "kotlin", "swift"}:
        project_domains.add("mobile")
    if infrastructure & {
        "kubernetes",
    }:
        project_domains.add("cloud-native-platform")
    for domain in sorted(project_domains):
        mapped = CANONICAL_DOMAIN_ID_MAP.get(domain)
        if mapped is not None:
            add(
                mapped,
                80,
                f"Project profile or detected facts require {domain}.",
                priority="required" if domain in profile_domains else "recommended",
            )

    for fact_id in sorted(frameworks | storage | infrastructure):
        technology_id = TECHNOLOGY_ALIASES.get(
            fact_id,
            f"technology.{fact_id}",
        )
        add(
            technology_id,
            90,
            f"Repository facts detect {fact_id}.",
        )

    task_tokens = normalized_tokens(task)
    negated_tokens: set[str] = set()
    for match in re.finditer(
        r"\b(?:without|exclude|excluding|avoid|avoiding|do not|don't|not)\b"
        r"(?P<tail>[^.;\n]{0,120})",
        task.lower(),
    ):
        negated_tokens.update(normalized_tokens(match.group("tail")))
    for entry_id, entry in entries.items():
        if entry_id in excludes:
            continue
        trigger_tokens = {
            token
            for trigger in entry.metadata["triggers"]
            for token in normalized_tokens(str(trigger))
        }
        matched = sorted((task_tokens & trigger_tokens) - negated_tokens)
        entry_domains = {
            canonical_domain(str(domain)) for domain in entry.metadata["domains"]
        }
        matched_domains = sorted(entry_domains & project_domains)
        distinctive_matches = set(matched) - GENERIC_TRIGGER_TOKENS
        reference_match = (
            entry.metadata["kind"] != "reference-architecture"
            or (
                bool(matched_domains)
                and (len(distinctive_matches) >= 1 or len(set(matched)) >= 2)
            )
            or len(distinctive_matches) >= 2
        )
        if (
            matched
            and reference_match
            and (matched_domains or len(matched) >= 2 or distinctive_matches)
        ):
            add(
                entry_id,
                25 + min(len(matched), 4),
                "Task matches trigger(s): " + ", ".join(matched),
            )
        if matched_domains:
            add(
                entry_id,
                6,
                "Entry domain matches project: " + ", ".join(matched_domains),
            )

    candidates = [
        (entry_id, score)
        for entry_id, score in scores.items()
        if score >= SELECTION_THRESHOLD and entry_id not in excludes
    ]
    candidates.sort(key=lambda item: (-item[1], item[0]))
    profile_required = {
        CANONICAL_DOMAIN_ID_MAP[domain]
        for domain in profile_domains
        if domain in CANONICAL_DOMAIN_ID_MAP
    }
    mandatory = {
        entry_id
        for entry_id in (
            *SKILL_REQUIRED.get(skill, ()),
            *includes,
            *profile_required,
        )
        if entry_id in entries and entry_id not in excludes
    }
    if len(mandatory) > maximum_entries:
        raise SelectionError(
            f"Context budget {maximum_entries} is below {len(mandatory)} "
            "mandatory entries"
        )
    selected_ids: list[str] = []
    for entry_id, _ in candidates:
        if len(selected_ids) >= maximum_entries:
            break
        selected_ids.append(entry_id)
    for entry_id in sorted(mandatory - set(selected_ids)):
        if len(selected_ids) >= maximum_entries:
            replace_index = next(
                (
                    index
                    for index in range(len(selected_ids) - 1, -1, -1)
                    if selected_ids[index] not in mandatory
                ),
                None,
            )
            if replace_index is None:
                raise SelectionError("Cannot satisfy mandatory knowledge budget")
            selected_ids.pop(replace_index)
        selected_ids.append(entry_id)
    selected_ids = sorted(
        set(selected_ids),
        key=lambda entry_id: (-scores[entry_id], entry_id),
    )
    if not selected_ids:
        fallback = "foundation.evidence-reasoning"
        selected_ids = [fallback]
        reasons[fallback].add("Default evidence discipline fallback.")
        priorities[fallback] = "required"

    # Expand one hop only. Related entries are useful context, but never displace
    # explicitly required or normally relevant entries and never bypass excludes.
    seed_ids = list(selected_ids)
    for seed_id in seed_ids:
        if len(selected_ids) >= maximum_entries:
            break
        for related_id in entries[seed_id].metadata["related"]:
            if (
                related_id in excludes
                or related_id in selected_ids
                or len(selected_ids) >= maximum_entries
            ):
                continue
            selected_ids.append(related_id)
            priorities[related_id] = "optional"
            reasons[related_id].add(f"One-hop relation from {seed_id}.")

    selected: list[dict[str, Any]] = []
    for entry_id in selected_ids:
        entry: KnowledgeEntry = entries[entry_id]
        selected.append(
            {
                "id": entry_id,
                "version": entry.metadata["version"],
                "path": entry.path.relative_to(KNOWLEDGE_ROOT).as_posix(),
                "sha256": entry.sha256,
                "priority": priorities[entry_id],
                "reasons": sorted(reasons[entry_id]),
            }
        )
    excluded_records = []
    for entry_id in sorted(set(entries) - set(selected_ids)):
        if entry_id in excludes:
            reason = "Explicit caller exclusion."
        elif scores[entry_id] >= SELECTION_THRESHOLD:
            reason = "Relevant but outside the configured context budget."
        elif scores[entry_id] > 0:
            reason = "Domain-only relevance is below the selection threshold."
        else:
            reason = (
                "No project fact, profile domain, task trigger, or skill rule "
                "selected it."
            )
        excluded_records.append({"id": entry_id, "reason": reason})
    result = {
        "schema_version": "1.1",
        "selection": selected,
        "excluded": excluded_records,
        "inputs": {
            "skill": skill,
            "task": task,
            "facts_sha256": file_sha256(facts_path),
        },
        "budget": {
            "maximum_entries": maximum_entries,
            "selected_entries": len(selected),
        },
    }
    if profile_path is not None:
        result["inputs"]["profile_sha256"] = file_sha256(profile_path)
    schema = json.loads(
        (SCHEMA_ROOT / "knowledge-selection.schema.json").read_text(encoding="utf-8")
    )
    errors = list(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(result)
    )
    if errors:
        raise SelectionError(
            f"Generated knowledge selection is invalid: {errors[0].message}"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--facts", type=Path, required=True)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--task", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--max-entries", type=int, default=24)
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        result = select_knowledge(
            args.facts,
            profile_path=args.profile,
            task=args.task,
            skill=args.skill,
            maximum_entries=args.max_entries,
            includes=args.include,
            excludes=args.exclude,
        )
        output = args.output.expanduser().resolve()
        if output.exists() and not args.force:
            raise SelectionError(
                f"Refusing to overwrite existing output without --force: {output}"
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            yaml.safe_dump(result, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except (SelectionError, OSError) as exc:
        print(f"Knowledge selection failed: {exc}", file=sys.stderr)
        return 2
    print(
        f"Knowledge selection written: {args.output.resolve()} "
        f"({result['budget']['selected_entries']} entries)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
