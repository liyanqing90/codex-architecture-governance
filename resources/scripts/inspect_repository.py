#!/usr/bin/env python3
"""Inspect repository facts without making architecture judgments."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
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
    "dist",
    "node_modules",
    "target",
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
    "agents": ("framework", "openai-agents-sdk", "ai"),
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
    result: list[Path] = []
    for scope in scopes:
        candidates = [scope] if scope.is_file() else scope.rglob("*")
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


def _fact_records(records: dict[str, set[str]]) -> list[dict[str, Any]]:
    return [
        {"id": key, "evidence": sorted(value)} for key, value in sorted(records.items())
    ]


def _categorized_fact_records(
    records: dict[tuple[str, str], set[str]],
) -> list[dict[str, Any]]:
    return [
        {"id": key[1], "category": key[0], "evidence": sorted(value)}
        for key, value in sorted(records.items())
    ]


def _manifest_dependencies(path: Path) -> set[str]:
    name = path.name.lower()
    text = path.read_text(encoding="utf-8", errors="ignore")
    result: set[str] = set()
    if name == "package.json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return result
        for field in ("dependencies", "devDependencies", "peerDependencies"):
            values = payload.get(field, {})
            if isinstance(values, dict):
                result.update(str(item).lower() for item in values)
        return result
    if name in {"requirements.txt", "pyproject.toml", "setup.cfg", "setup.py"}:
        lowered = text.lower()
        for dependency in DEPENDENCY_FACTS:
            if dependency in lowered:
                result.add(dependency)
        return result
    if name in {"pom.xml", "build.gradle", "build.gradle.kts"}:
        lowered = text.lower()
        if "spring-boot" in lowered:
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

    languages: dict[str, set[str]] = {}
    frameworks: dict[tuple[str, str], set[str]] = {}
    storage: dict[str, set[str]] = {}
    interfaces: dict[str, set[str]] = {}
    infrastructure: dict[str, set[str]] = {}
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
        "setup.cfg",
        "setup.py",
    }
    for path in files:
        relative = relative_files[path]
        lower = relative.lower()
        suffix = path.suffix.lower()
        language = LANGUAGE_SUFFIXES.get(suffix)
        if language is not None:
            languages.setdefault(language, set()).add(relative)
        if path.name.lower() in manifest_names or suffix in {".csproj", ".sln"}:
            manifests.append(path)
            for dependency in _manifest_dependencies(path):
                fact = DEPENDENCY_FACTS.get(dependency)
                if fact is None:
                    continue
                fact_type, fact_id, category = fact
                if fact_type == "framework":
                    frameworks.setdefault(
                        (str(category), fact_id),
                        set(),
                    ).add(relative)
                else:
                    storage.setdefault(fact_id, set()).add(relative)
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
            interfaces.setdefault("rest", set()).add(relative)
            api_definitions.append(path)
        elif suffix == ".graphql":
            interfaces.setdefault("graphql", set()).add(relative)
            api_definitions.append(path)
        elif suffix == ".proto":
            interfaces.setdefault("grpc", set()).add(relative)
            api_definitions.append(path)
        if lower.startswith(".github/workflows/") or "/.github/workflows/" in lower:
            ci.append(path)
        if path.name in {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}:
            infrastructure.setdefault("docker", set()).add(relative)
            deployments.append(path)
        if suffix == ".tf":
            infrastructure.setdefault("terraform", set()).add(relative)
            deployments.append(path)
        if path.name.lower() in {"nginx.conf", "caddyfile"}:
            fact_id = "nginx" if path.name.lower() == "nginx.conf" else "caddy"
            infrastructure.setdefault(fact_id, set()).add(relative)
            deployments.append(path)
        if suffix in {".yaml", ".yml"} and any(
            part.lower() in {"k8s", "kubernetes", "helm", "charts"}
            for part in path.parts
        ):
            infrastructure.setdefault("kubernetes", set()).add(relative)
            deployments.append(path)
        if suffix in {".db", ".sqlite", ".sqlite3"}:
            storage.setdefault("sqlite", set()).add(relative)

    # Content checks are limited to deployment manifests and do not infer quality.
    for path in sorted(set(manifests + deployments)):
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        relative = relative_files[path]
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
                target.setdefault(fact_id, set()).add(relative)

    commit = _git(root, "rev-parse", "HEAD") or "unknown"
    status = _git(root, "status", "--porcelain", "--untracked-files=normal")
    dirty = status is not None and bool(status)
    timestamp = scanned_at or datetime.now(UTC)
    result = {
        "schema_version": "1.0",
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
