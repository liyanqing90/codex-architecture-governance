#!/usr/bin/env python3
"""Validate the plugin repository's static contracts."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

EXPECTED_SKILLS = (
    "ai-agent-architecture-audit",
    "architecture-finding-verifier",
    "architecture-quality-gate",
    "architecture-remediation-planner",
    "mobile-architecture-audit",
    "portfolio-architecture-audit",
    "project-architecture-audit",
)
EVAL_KINDS = ("direct", "indirect", "incomplete", "negative", "edge")
REQUIRED_FILES = (
    ".codex-plugin/plugin.json",
    ".architecture/baseline.yaml",
    ".architecture/constraints.md",
    ".architecture/critical-flows.md",
    ".architecture/gate-policy.yaml",
    ".architecture/profile.yaml",
    ".architecture/reviews/README.md",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "NOTICE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "docs/evaluation.md",
    "docs/releasing.md",
    "evals/cases.yaml",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements.txt",
    "third_party/PAAD-MIT.txt",
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
)
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*]\("
    r"(?P<target><[^>]+>|[^)\s]+)"
    r"(?:\s+[\"'][^\"']*[\"'])?"
    r"\)"
)
RESOURCE_REF_RE = re.compile(r"`(?P<target>\.\./\.\./resources/[^`\s]+)`")
REFERENCE_REF_RE = re.compile(
    r"`(?P<target>\.\./(?:schemas|scripts|templates)/[^`\s]+)`"
)
FORBIDDEN_MARKERS = (
    "[" + "TODO:",
    "OWNER" + "/REPOSITORY",
    "Local " + "developer",
)
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing JSON file: {path}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"expected a JSON object in {path}")
        return None
    return payload


def load_yaml(path: Path, errors: list[str]) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing YAML file: {path}")
    except yaml.YAMLError as exc:
        errors.append(f"invalid YAML in {path}: {exc}")
    return None


def require_string(
    payload: dict[str, Any],
    key: str,
    source: str,
    errors: list[str],
) -> str | None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{source}.{key} must be a non-empty string")
        return None
    return value


def validate_manifest(root: Path, errors: list[str]) -> dict[str, Any] | None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path, errors)
    if manifest is None:
        return None

    name = require_string(manifest, "name", "plugin", errors)
    version = require_string(manifest, "version", "plugin", errors)
    require_string(manifest, "description", "plugin", errors)
    if name is not None and name != root.name:
        errors.append(
            f"plugin.name {name!r} must match repository directory {root.name!r}"
        )
    if version is not None and SEMVER_RE.fullmatch(version) is None:
        errors.append(f"plugin.version {version!r} is not strict Semantic Versioning")
    if manifest.get("skills") != "./skills/":
        errors.append("plugin.skills must be './skills/'")
    if manifest.get("license") != "MIT":
        errors.append("plugin.license must be 'MIT'")

    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append("plugin.author must be an object")
    else:
        author_name = require_string(author, "name", "plugin.author", errors)
        if author_name in {"Your Name", "Local " + "developer"}:
            errors.append("plugin.author.name must identify a real maintainer group")

    keywords = manifest.get("keywords")
    if (
        not isinstance(keywords, list)
        or len(keywords) < 3
        or not all(isinstance(item, str) and item.strip() for item in keywords)
    ):
        errors.append("plugin.keywords must contain at least three non-empty strings")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin.interface must be an object")
        return manifest
    for key in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        require_string(interface, key, "plugin.interface", errors)

    capabilities = interface.get("capabilities")
    if (
        not isinstance(capabilities, list)
        or not capabilities
        or not all(isinstance(item, str) and item.strip() for item in capabilities)
    ):
        errors.append("plugin.interface.capabilities must be a non-empty string array")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append(
            "plugin.interface.defaultPrompt must contain one to three prompts"
        )
    else:
        for index, prompt in enumerate(prompts):
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(
                    "plugin.interface.defaultPrompt"
                    f"[{index}] must be a non-empty string"
                )
            elif len(prompt) > 128:
                errors.append(
                    f"plugin.interface.defaultPrompt[{index}] exceeds 128 characters"
                )
    return manifest


def split_frontmatter(path: Path, errors: list[str]) -> tuple[Any, str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{path} must start with YAML frontmatter")
        return None
    try:
        closing = lines.index("---", 1)
    except ValueError:
        errors.append(f"{path} has unclosed YAML frontmatter")
        return None
    try:
        frontmatter = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError as exc:
        errors.append(f"invalid frontmatter in {path}: {exc}")
        return None
    return frontmatter, "\n".join(lines[closing + 1 :]).strip()


def validate_skill(root: Path, name: str, errors: list[str]) -> None:
    skill_root = root / "skills" / name
    skill_path = skill_root / "SKILL.md"
    if not skill_path.is_file():
        errors.append(f"missing Skill instructions: {skill_path}")
        return

    line_count = len(skill_path.read_text(encoding="utf-8").splitlines())
    if line_count >= 500:
        errors.append(f"{skill_path} has {line_count} lines; it must stay below 500")

    parsed = split_frontmatter(skill_path, errors)
    if parsed is None:
        return
    frontmatter, body = parsed
    if not isinstance(frontmatter, dict):
        errors.append(f"{skill_path} frontmatter must be a mapping")
    else:
        if set(frontmatter) != {"name", "description"}:
            errors.append(
                f"{skill_path} frontmatter keys must be exactly name and description"
            )
        if frontmatter.get("name") != name:
            errors.append(f"{skill_path} name must match its directory")
        description = frontmatter.get("description")
        if not isinstance(description, str) or len(description.strip()) < 80:
            errors.append(f"{skill_path} description is too short to route reliably")
        elif len(description) > 1024:
            errors.append(f"{skill_path} description exceeds 1,024 characters")
    if not body:
        errors.append(f"{skill_path} has no instruction body")

    ui_path = skill_root / "agents" / "openai.yaml"
    ui = load_yaml(ui_path, errors)
    if not isinstance(ui, dict) or not isinstance(ui.get("interface"), dict):
        errors.append(f"{ui_path} must contain an interface mapping")
    else:
        interface = ui["interface"]
        display_name = interface.get("display_name")
        short_description = interface.get("short_description")
        default_prompt = interface.get("default_prompt")
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{ui_path} interface.display_name is required")
        if (
            not isinstance(short_description, str)
            or not 25 <= len(short_description) <= 64
        ):
            errors.append(
                f"{ui_path} interface.short_description must be 25-64 characters"
            )
        if not isinstance(default_prompt, str) or f"${name}" not in default_prompt:
            errors.append(f"{ui_path} interface.default_prompt must mention ${name}")

    for match in RESOURCE_REF_RE.finditer(skill_path.read_text(encoding="utf-8")):
        referenced = (skill_root / match.group("target")).resolve()
        try:
            referenced.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{skill_path} resource escapes the plugin: {referenced}")
            continue
        if not referenced.is_file():
            errors.append(f"{skill_path} references missing resource: {referenced}")


def validate_skills(root: Path, errors: list[str]) -> None:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        errors.append(f"missing skills directory: {skills_root}")
        return
    actual = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    expected = sorted(EXPECTED_SKILLS)
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if missing:
            errors.append("missing Skills: " + ", ".join(missing))
        if extra:
            errors.append("unexpected directories under skills/: " + ", ".join(extra))
    for name in EXPECTED_SKILLS:
        validate_skill(root, name, errors)


def validate_reference_paths(root: Path, errors: list[str]) -> None:
    references_root = root / "resources" / "references"
    for path in sorted(references_root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in REFERENCE_REF_RE.finditer(text):
            referenced = (path.parent / match.group("target")).resolve()
            try:
                referenced.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path} resource escapes the plugin: {referenced}")
                continue
            if not referenced.is_file():
                errors.append(f"{path} references missing resource: {referenced}")


def validate_markdown_links(root: Path, errors: list[str]) -> None:
    excluded = {".git", ".pytest_cache", ".venv", "dist"}
    for path in sorted(root.rglob("*.md")):
        if excluded.intersection(path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group("target")
            target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("#"):
                continue
            local_text = unquote(target.split("#", 1)[0])
            if not local_text:
                continue
            local_path = (path.parent / local_text).resolve()
            try:
                local_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path} link escapes repository: {target}")
                continue
            if not local_path.exists():
                errors.append(f"{path} has broken local link: {target}")


def validate_schemas_and_yaml(root: Path, errors: list[str]) -> None:
    schemas_root = root / "resources" / "schemas"
    schema_paths = sorted(schemas_root.glob("*.schema.json"))
    if not schema_paths:
        errors.append(f"no JSON Schemas found in {schemas_root}")
    for path in schema_paths:
        payload = load_json(path, errors)
        if payload is None:
            continue
        try:
            Draft202012Validator.check_schema(payload)
        except SchemaError as exc:
            errors.append(f"invalid JSON Schema {path}: {exc.message}")

    yaml_roots = (
        root / ".architecture",
        root / "resources" / "templates",
        root / "skills",
        root / "evals",
        root / ".github",
    )
    for yaml_root in yaml_roots:
        if not yaml_root.exists():
            continue
        for pattern in ("*.yaml", "*.yml"):
            for path in sorted(yaml_root.rglob(pattern)):
                load_yaml(path, errors)


def validate_evals(root: Path, errors: list[str]) -> None:
    path = root / "evals" / "cases.yaml"
    payload = load_yaml(path, errors)
    if not isinstance(payload, dict):
        errors.append(f"{path} must contain a mapping")
        return
    if payload.get("schema_version") != "1.0":
        errors.append(f"{path} schema_version must be '1.0'")
    cases = payload.get("cases")
    if not isinstance(cases, list):
        errors.append(f"{path} cases must be an array")
        return

    ids: set[str] = set()
    coverage: dict[tuple[str, str], int] = {}
    for index, case in enumerate(cases):
        source = f"{path} cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{source} must be a mapping")
            continue
        case_id = case.get("id")
        skill = case.get("skill")
        kind = case.get("kind")
        prompt = case.get("prompt")
        expected = case.get("expected")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{source}.id must be a non-empty string")
        elif case_id in ids:
            errors.append(f"{source}.id is duplicated: {case_id}")
        else:
            ids.add(case_id)
        if skill not in EXPECTED_SKILLS:
            errors.append(f"{source}.skill is unknown: {skill!r}")
        if kind not in EVAL_KINDS:
            errors.append(f"{source}.kind is unknown: {kind!r}")
        if isinstance(skill, str) and isinstance(kind, str):
            key = (skill, kind)
            coverage[key] = coverage.get(key, 0) + 1
        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            errors.append(f"{source}.prompt must be a realistic prompt")
        if not isinstance(expected, dict):
            errors.append(f"{source}.expected must be a mapping")
            continue
        activates = expected.get("activates")
        outcome = expected.get("outcome")
        if not isinstance(activates, bool):
            errors.append(f"{source}.expected.activates must be a boolean")
        if not isinstance(outcome, str) or len(outcome.strip()) < 20:
            errors.append(
                f"{source}.expected.outcome must describe observable behavior"
            )
        if kind == "negative" and activates is not False:
            errors.append(f"{source} negative cases must not activate")
        if kind in {"direct", "indirect"} and activates is not True:
            errors.append(f"{source} direct and indirect cases must activate")

    expected_pairs = {(skill, kind) for skill in EXPECTED_SKILLS for kind in EVAL_KINDS}
    actual_pairs = set(coverage)
    missing = sorted(expected_pairs - actual_pairs)
    extra = sorted(actual_pairs - expected_pairs)
    duplicates = sorted(pair for pair, count in coverage.items() if count != 1)
    if missing:
        errors.append(
            "eval coverage is missing: "
            + ", ".join(f"{skill}/{kind}" for skill, kind in missing)
        )
    if extra:
        errors.append(
            "eval coverage has unknown pairs: "
            + ", ".join(f"{skill}/{kind}" for skill, kind in extra)
        )
    if duplicates:
        errors.append(
            "eval coverage must have exactly one case per pair: "
            + ", ".join(f"{skill}/{kind}" for skill, kind in duplicates)
        )


def validate_repository_hygiene(root: Path, errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required repository file: {relative}")

    runtime_roots = (
        root / ".codex-plugin",
        root / "resources",
        root / "skills",
    )
    for runtime_root in runtime_roots:
        if not runtime_root.exists():
            continue
        for path in runtime_root.rglob("*"):
            if (
                "__pycache__" in path.parts
                or path.suffix in {".pyc", ".pyo"}
                or path.name == ".DS_Store"
            ):
                errors.append(f"runtime tree contains a development artifact: {path}")
            if path.is_symlink():
                errors.append(f"runtime tree must not contain symlinks: {path}")

    excluded = {".git", ".pytest_cache", ".venv", "dist", "third_party"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if excluded.intersection(path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"{path} contains forbidden placeholder {marker!r}")


def validate_changelog(
    root: Path,
    manifest: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if manifest is None:
        return
    version = manifest.get("version")
    if not isinstance(version, str):
        return
    changelog_path = root / "CHANGELOG.md"
    try:
        changelog = changelog_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return
    if f"## [{version}]" not in changelog:
        errors.append(f"CHANGELOG.md has no section for plugin version {version}")


def validate_tool_version(
    root: Path,
    manifest: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if manifest is None or not isinstance(manifest.get("version"), str):
        return
    path = root / "resources" / "scripts" / "architecture_tool.py"
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (FileNotFoundError, SyntaxError) as exc:
        errors.append(f"cannot inspect architecture tool version: {exc}")
        return
    tool_version: str | None = None
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if (
            isinstance(target, ast.Name)
            and target.id == "TOOL_VERSION"
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            tool_version = node.value.value
            break
    if tool_version is None:
        errors.append(f"{path} must define a string TOOL_VERSION")
    elif tool_version != manifest["version"]:
        errors.append(
            f"architecture tool version {tool_version!r} does not match "
            f"plugin version {manifest['version']!r}"
        )


def validate_repository(root: Path) -> list[str]:
    root = root.expanduser().resolve()
    errors: list[str] = []
    validate_repository_hygiene(root, errors)
    manifest = validate_manifest(root, errors)
    validate_skills(root, errors)
    validate_reference_paths(root, errors)
    validate_markdown_links(root, errors)
    validate_schemas_and_yaml(root, errors)
    validate_evals(root, errors)
    validate_changelog(root, manifest, errors)
    validate_tool_version(root, manifest, errors)
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Codex Architecture Governance repository contracts."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root; defaults to the parent of scripts/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.expanduser().resolve()
    errors = validate_repository(root)
    if errors:
        print(f"Repository validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    schema_count = len(list((root / "resources" / "schemas").glob("*.json")))
    template_count = len(list((root / "resources" / "templates").glob("*.yaml")))
    eval_payload = yaml.safe_load(
        (root / "evals" / "cases.yaml").read_text(encoding="utf-8")
    )
    print(
        "Repository validation passed: "
        f"{len(EXPECTED_SKILLS)} Skills, "
        f"{len(eval_payload['cases'])} eval cases, "
        f"{schema_count} schemas, and {template_count} templates."
    )


if __name__ == "__main__":
    main()
