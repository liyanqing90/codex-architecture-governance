#!/usr/bin/env python3
"""Inspect repository facts without making architecture judgments."""

from __future__ import annotations

import argparse
import ast
import configparser
import json
import os
import re
import subprocess
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCRIPT_ROOT = Path(__file__).resolve().parent
RESOURCE_ROOT = SCRIPT_ROOT.parent
SCHEMA_ROOT = RESOURCE_ROOT / "schemas"
IGNORED_PARTS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "codegen",
    "dist",
    "generated",
    "node_modules",
    "third-party",
    "third_party",
    "target",
    "vendor",
}
FACT_ROLES = {
    "runtime",
    "production",
    "test",
    "benchmark-fixture",
    "example",
    "documentation",
    "generated",
    "vendor",
}
LANGUAGE_SUFFIXES = {
    ".c": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".dart": "dart",
    ".ex": "elixir",
    ".exs": "elixir",
    ".go": "go",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".php": "php",
    ".py": "python",
    ".rb": "ruby",
    ".rs": "rust",
    ".scala": "scala",
    ".swift": "swift",
    ".ts": "typescript",
    ".tsx": "typescript",
}
DEPENDENCY_FACTS = {
    "react": ("framework", "react", "frontend"),
    "next": ("framework", "nextjs", "frontend"),
    "vue": ("framework", "vue", "frontend"),
    "astro": ("framework", "astro", "frontend"),
    "vite": ("framework", "vite", "frontend"),
    "fastapi": ("framework", "fastapi", "backend"),
    "django": ("framework", "django", "backend"),
    "@nestjs/core": ("framework", "nestjs", "backend"),
    "spring-boot": ("framework", "spring-boot", "backend"),
    "langgraph": ("framework", "langgraph", "ai"),
    "openai-agents": ("framework", "openai-agents-sdk", "ai"),
    "@openai/agents": ("framework", "openai-agents-sdk", "ai"),
    "psycopg": ("storage", "postgresql", None),
    "asyncpg": ("storage", "postgresql", None),
    "pg": ("storage", "postgresql", None),
    "mysqlclient": ("storage", "mysql", None),
    "pymysql": ("storage", "mysql", None),
    "mongodb": ("storage", "mongodb", None),
    "pymongo": ("storage", "mongodb", None),
    "redis": ("storage", "redis", None),
    "neo4j": ("storage", "neo4j", None),
    "sqlite": ("storage", "sqlite", None),
    "sqlalchemy": ("framework", "sqlalchemy", "data"),
}
PYTHON_DEPENDENCY_FACT_IDS = {
    "asyncpg": "asyncpg",
    "django": "django",
    "fastapi": "fastapi",
    "langgraph": "langgraph",
    "mongodb": "mongodb",
    "mysqlclient": "mysqlclient",
    "neo4j": "neo4j",
    "openai-agents": "openai-agents",
    "psycopg": "psycopg",
    "pymongo": "pymongo",
    "pymysql": "pymysql",
    "redis": "redis",
    "sqlalchemy": "sqlalchemy",
}
PEP_508_NAME_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


class InspectionError(RuntimeError):
    """Invalid or inaccessible repository inspection."""


def _within(root: Path, candidate: Path, label: str) -> Path:
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise InspectionError(f"{label} escapes repository root: {candidate}") from exc
    return resolved


def _git(root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _paths(root: Path, scopes: list[Path]) -> list[Path]:
    """Return a bounded, deterministic set of inspectable repository files.

    Dependency/vendor and generated trees are intentionally pruned before
    traversal. They can be large, derived, or third-party and therefore cannot
    establish product architecture. Source files named like generated output
    outside those trees remain observable with the ``generated`` role.
    """
    result: list[Path] = []
    for scope in scopes:
        if scope.is_file():
            candidates = [scope]
        else:
            candidates = []
            for directory, directories, filenames in os.walk(
                scope,
                topdown=True,
                followlinks=False,
            ):
                directory_path = Path(directory)
                directories[:] = sorted(
                    name
                    for name in directories
                    if name not in IGNORED_PARTS
                    and not (directory_path / name).is_symlink()
                )
                candidates.extend(directory_path / name for name in sorted(filenames))
        for path in candidates:
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root)
            if IGNORED_PARTS.intersection(relative.parts):
                continue
            result.append(path)
    return sorted(set(result), key=lambda item: item.relative_to(root).as_posix())


def _relative(root: Path, paths: list[Path]) -> list[str]:
    return sorted({path.relative_to(root).as_posix() for path in paths})


def _path_role(relative: str) -> str:
    parts = tuple(part.lower() for part in Path(relative).parts)
    part_set = set(parts)
    name = parts[-1] if parts else ""
    if "vendor" in part_set or "third_party" in part_set or "third-party" in part_set:
        return "vendor"
    if (
        "generated" in part_set
        or "autogenerated" in part_set
        or "codegen" in part_set
        or any(part.endswith(".generated") for part in parts)
        or ".generated." in name
        or name.startswith("generated_")
    ):
        return "generated"
    if "benchmarks" in part_set and ("fixtures" in part_set or "fixture" in part_set):
        return "benchmark-fixture"
    if name.startswith(("requirements-dev", "requirements-test")):
        return "test"
    if (
        part_set & {"tests", "test", "__tests__", "spec", "specs"}
        or name.startswith("test_")
        or re.search(r"(?:_test|\.spec|\.test)\.[a-z0-9]+$", name)
    ):
        return "test"
    if part_set & {"examples", "example", "samples", "sample", "demos", "demo"}:
        return "example"
    if part_set & {"docs", "doc", "documentation"}:
        return "documentation"
    if parts and parts[0] in {"src", "app", "lib", "runtime"}:
        return "runtime"
    return "production"


def _fact_records(
    records: dict[tuple[str, str], set[str]],
) -> list[dict[str, Any]]:
    return [
        {"id": key[0], "role": key[1], "evidence": sorted(value)}
        for key, value in sorted(records.items())
    ]


def _categorized_fact_records(
    records: dict[tuple[str, str, str], set[str]],
) -> list[dict[str, Any]]:
    return [
        {
            "id": key[1],
            "category": key[0],
            "role": key[2],
            "evidence": sorted(value),
        }
        for key, value in sorted(records.items())
    ]


def _python_dependency_ids(values: list[str]) -> set[str]:
    """Map parsed Python requirement names to known product facts.

    PEP 508 names are normalized before exact alias lookup. Requirement
    specifiers, extras, markers, URLs, comments, and similarly named packages
    never become substring evidence for another dependency.
    """
    result: set[str] = set()
    for value in values:
        stripped = value.strip()
        if not stripped or stripped.startswith(("#", "-")):
            continue
        match = PEP_508_NAME_RE.match(stripped)
        if match is None:
            continue
        normalized = re.sub(r"[-_.]+", "-", match.group(1).lower())
        dependency = PYTHON_DEPENDENCY_FACT_IDS.get(normalized)
        if dependency is not None:
            result.add(dependency)
    return result


def _static_string_sequence(
    node: ast.AST,
    assignments: dict[str, list[str]],
) -> list[str] | None:
    """Resolve a deliberately small, non-executing setup.py value subset."""
    if isinstance(node, ast.Name):
        value = assignments.get(node.id)
        return list(value) if value is not None else None
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        values: list[str] = []
        for item in node.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            values.append(item.value)
        return values
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _static_string_sequence(node.left, assignments)
        right = _static_string_sequence(node.right, assignments)
        return None if left is None or right is None else [*left, *right]
    return None


def _setup_py_dependencies(text: str) -> set[str]:
    """Read literal ``install_requires`` values without executing setup.py."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()

    assignments: dict[str, list[str]] = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            value = _static_string_sequence(statement.value, assignments)
            if value is not None:
                for target in statement.targets:
                    if isinstance(target, ast.Name):
                        assignments[target.id] = value
        elif isinstance(statement, ast.AnnAssign) and isinstance(
            statement.target, ast.Name
        ):
            value = (
                _static_string_sequence(statement.value, assignments)
                if statement.value
                else None
            )
            if value is not None:
                assignments[statement.target.id] = value

    dependencies: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        is_setup_call = (
            isinstance(node.func, ast.Name) and node.func.id == "setup"
        ) or (isinstance(node.func, ast.Attribute) and node.func.attr == "setup")
        if not is_setup_call:
            continue
        for keyword in node.keywords:
            if keyword.arg == "install_requires":
                values = _static_string_sequence(keyword.value, assignments)
                if values is not None:
                    dependencies.extend(values)
    return _python_dependency_ids(dependencies)


def _manifest_dependencies(path: Path) -> set[str]:
    """Return only dependencies that can represent shipped product behavior.

    Development-only dependency sections are deliberately ignored. They often
    contain framework names used only by test, build, documentation, or lint
    tooling and must not infer product domains or technology profiles.
    """
    name = path.name.lower()
    text = path.read_text(encoding="utf-8", errors="ignore")
    result: set[str] = set()
    if name == "package.json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return result
        for field in ("dependencies", "optionalDependencies", "peerDependencies"):
            values = payload.get(field, {})
            if isinstance(values, dict):
                result.update(str(item).lower() for item in values)
        return result
    if name.startswith("requirements") and name.endswith(".txt"):
        return _python_dependency_ids(text.splitlines())
    if name == "pyproject.toml":
        try:
            payload = tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            return result
        project = payload.get("project", {})
        if isinstance(project, dict):
            dependencies = project.get("dependencies", [])
            if isinstance(dependencies, list):
                result.update(
                    _python_dependency_ids([str(item) for item in dependencies])
                )
        poetry = payload.get("tool", {}).get("poetry", {})
        if isinstance(poetry, dict):
            dependencies = poetry.get("dependencies", {})
            if isinstance(dependencies, dict):
                result.update(
                    _python_dependency_ids([str(item) for item in dependencies])
                )
        return result
    if name == "setup.cfg":
        parser = configparser.ConfigParser()
        try:
            parser.read_string(text)
        except configparser.Error:
            return result
        if parser.has_option("options", "install_requires"):
            result.update(
                _python_dependency_ids(
                    parser.get("options", "install_requires").splitlines()
                )
            )
        return result
    if name == "setup.py":
        return _setup_py_dependencies(text)
    if name == "pom.xml":
        # Do not execute build files. A bounded structural read can distinguish
        # test-scoped Maven dependencies from shipped dependencies.
        for block in re.findall(r"<dependency>(.*?)</dependency>", text, re.DOTALL):
            if re.search(r"<scope>\s*test\s*</scope>", block, re.IGNORECASE):
                continue
            if "spring-boot" in block.lower():
                result.add("spring-boot")
        return result
    if name in {"build.gradle", "build.gradle.kts"}:
        for line in text.splitlines():
            lowered = line.lower()
            if "spring-boot" not in lowered:
                continue
            if re.search(
                r"\btest(?:implementation|runtimeonly|compileonly)\b",
                lowered,
            ):
                continue
            if re.search(
                r"\b(?:implementation|api|runtimeonly|compileonly)\b",
                lowered,
            ):
                result.add("spring-boot")
    return result


def inspect_repository(
    repo: Path,
    *,
    scope_values: list[str] | None = None,
    scanned_at: datetime | None = None,
) -> dict[str, Any]:
    root = repo.expanduser().resolve()
    if not root.is_dir():
        raise InspectionError(f"Repository root is not a directory: {root}")
    scope_values = scope_values or ["."]
    scopes = [_within(root, root / value, f"scope {value!r}") for value in scope_values]
    for scope in scopes:
        if not scope.exists():
            raise InspectionError(f"Scope does not exist: {scope}")
    files = _paths(root, scopes)
    relative_files = {path: path.relative_to(root).as_posix() for path in files}

    languages: dict[tuple[str, str], set[str]] = {}
    frameworks: dict[tuple[str, str, str], set[str]] = {}
    storage: dict[tuple[str, str], set[str]] = {}
    interfaces: dict[tuple[str, str], set[str]] = {}
    infrastructure: dict[tuple[str, str], set[str]] = {}
    manifests: list[Path] = []
    migrations: list[Path] = []
    api_definitions: list[Path] = []
    ci: list[Path] = []
    deployments: list[Path] = []

    manifest_names = {
        "build.gradle",
        "build.gradle.kts",
        "cargo.toml",
        "composer.json",
        "gemfile",
        "go.mod",
        "package.json",
        "pom.xml",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "setup.cfg",
        "setup.py",
    }
    for path in files:
        relative = relative_files[path]
        lower = relative.lower()
        suffix = path.suffix.lower()
        role = _path_role(relative)
        if role not in FACT_ROLES:
            raise InspectionError(f"Unsupported repository fact role: {role}")
        language = LANGUAGE_SUFFIXES.get(suffix)
        if language is not None:
            languages.setdefault((language, role), set()).add(relative)
        if path.name.lower() in manifest_names or suffix in {".csproj", ".sln"}:
            manifests.append(path)
            for dependency in _manifest_dependencies(path):
                fact = DEPENDENCY_FACTS.get(dependency)
                if fact is None:
                    continue
                fact_type, fact_id, category = fact
                if fact_type == "framework":
                    frameworks.setdefault(
                        (str(category), fact_id, role),
                        set(),
                    ).add(relative)
                else:
                    storage.setdefault((fact_id, role), set()).add(relative)
        if "migration" in {
            part.lower() for part in path.parts
        } or path.name.lower().startswith(("alembic", "flyway", "liquibase")):
            migrations.append(path)
        if path.name.lower() in {
            "openapi.json",
            "openapi.yaml",
            "openapi.yml",
            "swagger.json",
            "swagger.yaml",
            "swagger.yml",
        }:
            interfaces.setdefault(("rest", role), set()).add(relative)
            api_definitions.append(path)
        elif suffix == ".graphql":
            interfaces.setdefault(("graphql", role), set()).add(relative)
            api_definitions.append(path)
        elif suffix == ".proto":
            interfaces.setdefault(("grpc", role), set()).add(relative)
            api_definitions.append(path)
        if lower.startswith(".github/workflows/") or "/.github/workflows/" in lower:
            ci.append(path)
        if path.name in {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}:
            infrastructure.setdefault(("docker", role), set()).add(relative)
            deployments.append(path)
        if suffix == ".tf":
            infrastructure.setdefault(("terraform", role), set()).add(relative)
            deployments.append(path)
        if path.name.lower() in {"nginx.conf", "caddyfile"}:
            fact_id = "nginx" if path.name.lower() == "nginx.conf" else "caddy"
            infrastructure.setdefault((fact_id, role), set()).add(relative)
            deployments.append(path)
        if suffix in {".yaml", ".yml"} and any(
            part.lower() in {"k8s", "kubernetes", "helm", "charts"}
            for part in path.parts
        ):
            infrastructure.setdefault(("kubernetes", role), set()).add(relative)
            deployments.append(path)
        if suffix in {".db", ".sqlite", ".sqlite3"}:
            storage.setdefault(("sqlite", role), set()).add(relative)

    # Content checks are limited to deployment manifests and do not infer quality.
    for path in sorted(set(manifests + deployments)):
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        relative = relative_files[path]
        role = _path_role(relative)
        for token, fact_id in (
            ("postgres", "postgresql"),
            ("mysql", "mysql"),
            ("mongo", "mongodb"),
            ("redis", "redis"),
            ("neo4j", "neo4j"),
            ("kafka", "apache-kafka"),
            ("rabbitmq", "rabbitmq"),
            ("nats", "nats"),
        ):
            if token in content:
                target = (
                    storage
                    if fact_id
                    in {
                        "postgresql",
                        "mysql",
                        "mongodb",
                        "redis",
                        "neo4j",
                    }
                    else infrastructure
                )
                target.setdefault((fact_id, role), set()).add(relative)

    commit = _git(root, "rev-parse", "HEAD") or "unknown"
    status = _git(root, "status", "--porcelain", "--untracked-files=normal")
    dirty = status is not None and bool(status)
    timestamp = scanned_at or datetime.now(UTC)
    result = {
        "schema_version": "1.1",
        "repository": {
            "root": ".",
            "commit": commit,
            "dirty": dirty,
            "scanned_at": timestamp.isoformat(),
            "scope": sorted(scope_values),
        },
        "languages": _fact_records(languages),
        "frameworks": _categorized_fact_records(frameworks),
        "storage": _fact_records(storage),
        "interfaces": _fact_records(interfaces),
        "infrastructure": _fact_records(infrastructure),
        "artifacts": {
            "manifests": _relative(root, manifests),
            "migrations": _relative(root, migrations),
            "api_definitions": _relative(root, api_definitions),
            "ci": _relative(root, ci),
            "deployments": _relative(root, deployments),
        },
    }
    schema = json.loads(
        (SCHEMA_ROOT / "repository-facts.schema.json").read_text(encoding="utf-8")
    )
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(result),
        key=lambda error: tuple(str(item) for item in error.absolute_path),
    )
    if errors:
        detail = "; ".join(error.message for error in errors[:10])
        raise InspectionError(f"Generated repository facts are invalid: {detail}")
    return result


def write_output(path: Path, payload: dict[str, Any], *, force: bool) -> None:
    path = path.expanduser().resolve()
    if path.exists() and not force:
        raise InspectionError(
            f"Refusing to overwrite existing output without --force: {path}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        payload = inspect_repository(
            args.repo,
            scope_values=args.scope or None,
        )
        write_output(args.output, payload, force=args.force)
    except (InspectionError, OSError, subprocess.SubprocessError) as exc:
        print(f"Repository inspection failed: {exc}", file=sys.stderr)
        return 2
    print(f"Repository facts written: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
