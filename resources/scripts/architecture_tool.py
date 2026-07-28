#!/usr/bin/env python3
"""Initialize, validate, and gate architecture review artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ModuleNotFoundError as exc:  # pragma: no cover - environment failure
    print(
        f"architecture_tool.py requires PyYAML and jsonschema (missing {exc.name}).",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


SHARED_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_ROOT = SHARED_ROOT / "schemas"
TEMPLATE_ROOT = SHARED_ROOT / "templates"
SEVERITY_ORDER = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}
TOOL_VERSION = "0.1.0"


class ArchitectureError(RuntimeError):
    """User-facing input or contract error."""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if len(slug) < 3:
        slug = f"{slug or 'project'}-app"
    return slug[:64].rstrip("-")


def normalize_yaml_scalars(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize_yaml_scalars(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_yaml_scalars(item) for item in value]
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ArchitectureError(f"Missing file: {path}") from exc
    except yaml.YAMLError as exc:
        raise ArchitectureError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ArchitectureError(f"Expected a YAML mapping in {path}")
    return normalize_yaml_scalars(value)


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_ROOT / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ArchitectureError(f"Missing bundled schema: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ArchitectureError(f"Invalid bundled schema {path}: {exc}") from exc


def format_validation_path(parts: Any) -> str:
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def validate_data(
    data: dict[str, Any],
    schema_name: str,
    source: Path,
) -> None:
    validator = Draft202012Validator(
        load_schema(schema_name),
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    if errors:
        messages = [
            f"{format_validation_path(error.absolute_path)}: {error.message}"
            for error in errors
        ]
        raise ArchitectureError(
            f"{source} does not match {schema_name}:\n  - " + "\n  - ".join(messages)
        )


def validate_file(path: Path, schema_name: str) -> dict[str, Any]:
    data = load_yaml(path)
    validate_data(data, schema_name, path)
    return data


def validate_review(path: Path) -> dict[str, Any]:
    data = validate_file(path, "review.schema.json")
    finding_ids: set[str] = set()
    findings = data["findings"]

    for index, finding in enumerate(findings):
        source = Path(f"{path}#findings[{index}]")
        if not isinstance(finding, dict):
            raise ArchitectureError(f"{source} must be a mapping")
        validate_data(finding, "finding.schema.json", source)
        finding_id = finding["id"]
        if finding_id in finding_ids:
            raise ArchitectureError(f"{path} has duplicate finding ID {finding_id}")
        finding_ids.add(finding_id)
        if finding["confidence"] < 0.60:
            raise ArchitectureError(
                f"{path} finding {finding_id} has confidence below 0.60"
            )
        if finding["kind"] == "strength" and finding["severity"] != "info":
            raise ArchitectureError(
                f"{path} strength {finding_id} must use severity 'info'"
            )
        if (
            finding["verification"]["status"] == "rejected"
            and finding["status"] != "rejected"
        ):
            raise ArchitectureError(
                f"{path} rejected finding {finding_id} must have status 'rejected'"
            )

    review_state = data["review"]["verification_state"]
    verification_states = [finding["verification"]["status"] for finding in findings]
    if review_state == "candidates":
        non_candidates = [
            finding["id"]
            for finding in findings
            if finding["verification"]["status"] != "candidate"
        ]
        if non_candidates:
            raise ArchitectureError(
                f"{path} is a candidate review but contains verified IDs: "
                + ", ".join(non_candidates)
            )
    elif "candidate" in verification_states:
        candidate_ids = [
            finding["id"]
            for finding in findings
            if finding["verification"]["status"] == "candidate"
        ]
        raise ArchitectureError(
            f"{path} is verified but still has candidate IDs: "
            + ", ".join(candidate_ids)
        )

    expected_counts = {
        "raw_findings": len(findings),
        "confirmed": verification_states.count("confirmed"),
        "rejected": verification_states.count("rejected"),
        "needs_evidence": verification_states.count("needs-evidence"),
    }
    for key, expected in expected_counts.items():
        actual = data["summary"][key]
        if actual != expected:
            raise ArchitectureError(
                f"{path} summary.{key} is {actual}, expected {expected}"
            )

    for coverage in data["coverage"]:
        missing = sorted(set(coverage["finding_ids"]) - finding_ids)
        if missing:
            raise ArchitectureError(
                f"{path} coverage {coverage['rule_id']} references unknown IDs: "
                + ", ".join(missing)
            )
        if coverage["status"] != "assessed" and not coverage.get("reason"):
            raise ArchitectureError(
                f"{path} coverage {coverage['rule_id']} requires a reason for "
                f"{coverage['status']}"
            )

    return data


def validate_plan(path: Path) -> dict[str, Any]:
    data = validate_file(path, "remediation-plan.schema.json")
    item_ids: set[str] = set()
    planned_findings: set[str] = set()
    for item in data["items"]:
        item_id = item["id"]
        if item_id in item_ids:
            raise ArchitectureError(f"{path} has duplicate plan item ID {item_id}")
        item_ids.add(item_id)
        duplicates = sorted(set(item["finding_ids"]) & planned_findings)
        if duplicates:
            raise ArchitectureError(
                f"{path} plans finding IDs more than once: " + ", ".join(duplicates)
            )
        planned_findings.update(item["finding_ids"])
    return data


def resolve_from_root(root: Path, configured_path: str) -> Path:
    path = Path(configured_path)
    return path if path.is_absolute() else root / path


def validate_project(root: Path) -> list[Path]:
    root = root.resolve()
    config_root = root / ".architecture"
    profile_path = config_root / "profile.yaml"
    policy_path = config_root / "gate-policy.yaml"
    baseline_path = config_root / "baseline.yaml"

    profile = validate_file(profile_path, "project-profile.schema.json")
    validate_file(policy_path, "gate-policy.schema.json")
    validate_file(baseline_path, "baseline.schema.json")

    validated = [profile_path, policy_path, baseline_path]
    for field in ("constraints_file", "critical_flows_file"):
        expected = resolve_from_root(root, profile["project"][field])
        if not expected.is_file():
            raise ArchitectureError(
                f"Profile field project.{field} points to missing file: {expected}"
            )
        validated.append(expected)

    reviews_root = resolve_from_root(root, profile["project"]["review_output"])
    if not reviews_root.is_dir():
        raise ArchitectureError(f"Missing review output directory: {reviews_root}")

    for artifact in sorted(reviews_root.glob("*.yaml")):
        payload = load_yaml(artifact)
        if "review" in payload:
            validate_review(artifact)
        elif "plan" in payload:
            validate_plan(artifact)
        else:
            raise ArchitectureError(
                f"Unknown YAML artifact in reviews directory: {artifact}"
            )
        validated.append(artifact)
    return validated


def validate_portfolio(root: Path) -> list[Path]:
    root = root.resolve()
    config_root = root / ".architecture-portfolio"
    registry_path = config_root / "portfolio.yaml"
    registry = validate_file(registry_path, "portfolio.schema.json")
    policy_path = config_root / "gate-policy.yaml"
    baseline_path = config_root / "baseline.yaml"
    validate_file(policy_path, "gate-policy.schema.json")
    validate_file(baseline_path, "baseline.schema.json")
    catalog_schemas = {
        "shared_capabilities": "shared-capabilities.schema.json",
        "technologies": "technology-catalog.schema.json",
        "dependencies": "dependency-map.schema.json",
    }
    validated = [registry_path, policy_path, baseline_path]
    for key, schema_name in catalog_schemas.items():
        catalog_path = resolve_from_root(root, registry["catalogs"][key])
        validate_file(catalog_path, schema_name)
        validated.append(catalog_path)

    project_ids = [project["id"] for project in registry["projects"]]
    duplicate_ids = sorted(
        {project_id for project_id in project_ids if project_ids.count(project_id) > 1}
    )
    if duplicate_ids:
        raise ArchitectureError(
            f"{registry_path} has duplicate project IDs: " + ", ".join(duplicate_ids)
        )
    known_ids = set(project_ids)
    for project in registry["projects"]:
        unknown = sorted(set(project["depends_on"]) - known_ids)
        if unknown:
            raise ArchitectureError(
                f"{registry_path} project {project['id']} depends on unknown IDs: "
                + ", ".join(unknown)
            )

    reviews_root = resolve_from_root(root, registry["portfolio"]["review_output"])
    if not reviews_root.is_dir():
        raise ArchitectureError(f"Missing portfolio review directory: {reviews_root}")
    for artifact in sorted(reviews_root.glob("*.yaml")):
        payload = load_yaml(artifact)
        if "review" in payload:
            validate_review(artifact)
        elif "plan" in payload:
            validate_plan(artifact)
        else:
            raise ArchitectureError(
                f"Unknown YAML artifact in portfolio reviews: {artifact}"
            )
        validated.append(artifact)
    return validated


def copy_template(name: str, destination: Path) -> None:
    source = TEMPLATE_ROOT / name
    if not source.is_file():
        raise ArchitectureError(f"Missing bundled template: {source}")
    shutil.copyfile(source, destination)


def init_project(args: argparse.Namespace) -> Path:
    root = Path(args.repo).resolve()
    if not root.is_dir():
        raise ArchitectureError(f"Repository directory does not exist: {root}")
    target = root / ".architecture"
    if target.exists():
        raise ArchitectureError(f"Refusing to overwrite existing directory: {target}")

    project_name = args.name or root.name
    project_id = args.project_id or slugify(project_name)
    with tempfile.TemporaryDirectory(prefix=".architecture-init-", dir=root) as temp:
        staged = Path(temp) / ".architecture"
        staged.mkdir()
        (staged / "reviews").mkdir()
        (staged / "reviews" / ".gitkeep").touch()

        profile = load_yaml(TEMPLATE_ROOT / "profile.yaml")
        profile["project"].update(
            {
                "id": project_id,
                "name": project_name,
                "type": args.types or ["service"],
                "lifecycle": args.lifecycle,
                "criticality": args.criticality,
                "owners": args.owners or ["unassigned"],
                "critical_qualities": args.qualities
                or ["maintainability", "recoverability"],
                "required_reviews": args.reviews or ["project-architecture"],
                "rule_packs": args.rule_packs or ["project-core"],
                "data_classification": args.data_classification,
            }
        )
        validate_data(
            profile,
            "project-profile.schema.json",
            staged / "profile.yaml",
        )
        write_yaml(staged / "profile.yaml", profile)
        copy_template("constraints.md", staged / "constraints.md")
        copy_template("critical-flows.md", staged / "critical-flows.md")
        copy_template("gate-policy.yaml", staged / "gate-policy.yaml")
        copy_template("baseline.yaml", staged / "baseline.yaml")
        staged.rename(target)
    return target


def init_portfolio(args: argparse.Namespace) -> Path:
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise ArchitectureError(f"Portfolio root does not exist: {root}")
    target = root / ".architecture-portfolio"
    if target.exists():
        raise ArchitectureError(f"Refusing to overwrite existing directory: {target}")

    portfolio_name = args.name or f"{root.name} Portfolio"
    portfolio_id = args.portfolio_id or slugify(portfolio_name)
    with tempfile.TemporaryDirectory(
        prefix=".architecture-portfolio-init-",
        dir=root,
    ) as temp:
        staged = Path(temp) / ".architecture-portfolio"
        staged.mkdir()
        (staged / "reviews").mkdir()
        (staged / "reviews" / ".gitkeep").touch()

        portfolio = load_yaml(TEMPLATE_ROOT / "portfolio.yaml")
        portfolio["portfolio"].update(
            {
                "id": portfolio_id,
                "name": portfolio_name,
                "owners": args.owners or ["unassigned"],
                "review_horizon_months": args.review_horizon_months,
            }
        )
        validate_data(
            portfolio,
            "portfolio.schema.json",
            staged / "portfolio.yaml",
        )
        write_yaml(staged / "portfolio.yaml", portfolio)
        copy_template(
            "shared-capabilities.yaml",
            staged / "shared-capabilities.yaml",
        )
        copy_template(
            "technology-catalog.yaml",
            staged / "technology-catalog.yaml",
        )
        copy_template("dependency-map.yaml", staged / "dependency-map.yaml")
        copy_template(
            "portfolio-gate-policy.yaml",
            staged / "gate-policy.yaml",
        )
        copy_template("baseline.yaml", staged / "baseline.yaml")
        staged.rename(target)
    return target


def parse_date(value: str, field: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ArchitectureError(f"Invalid date for {field}: {value}") from exc


def active_until(expires_on: str | None, today: date) -> bool:
    return expires_on is None or parse_date(expires_on, "expires_on") >= today


def current_git_commit(root: Path) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise ArchitectureError(
            f"Cannot resolve current git commit for {root}: "
            f"{process.stderr.strip() or 'not a git repository'}"
        )
    return process.stdout.strip()


def find_latest_review(reviews_root: Path) -> Path:
    candidates = sorted(reviews_root.glob("*-verified.yaml"))
    if not candidates:
        raise ArchitectureError(f"No verified review found in {reviews_root}")
    return candidates[-1]


def ensure_unique_entries(
    entries: list[dict[str, Any]],
    key: str,
    source: Path,
) -> None:
    values = [entry[key] for entry in entries]
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ArchitectureError(
            f"{source} has duplicate {key} values: " + ", ".join(duplicates)
        )


def gate_from_config(
    root: Path,
    config_root: Path,
    review_path: Path | None,
    today: date | None = None,
    commit_root: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    policy_path = config_root / "gate-policy.yaml"
    baseline_path = config_root / "baseline.yaml"
    policy = validate_file(policy_path, "gate-policy.schema.json")
    baseline = validate_file(baseline_path, "baseline.schema.json")
    ensure_unique_entries(
        baseline["findings"],
        "id",
        baseline_path,
    )
    ensure_unique_entries(
        policy["waivers"],
        "finding_id",
        policy_path,
    )
    if review_path is None:
        review_path = find_latest_review(config_root / "reviews")
    elif not review_path.is_absolute():
        review_path = root / review_path
    review_path = review_path.resolve()
    review = validate_review(review_path)

    if review["review"]["verification_state"] != "verified":
        raise ArchitectureError(f"Gate requires a verified review: {review_path}")

    evaluation_date = today or datetime.now(UTC).date()
    block = policy["block"]
    policy_failures: list[str] = []
    warnings: list[str] = []

    if review["review"]["kind"] not in policy["review_kinds"]:
        policy_failures.append(
            f"Review kind {review['review']['kind']} is not allowed by policy"
        )

    performed_at = datetime.fromisoformat(
        review["review"]["performed_at"].replace("Z", "+00:00")
    )
    review_age = (evaluation_date - performed_at.date()).days
    if review_age < 0:
        policy_failures.append(
            f"Review date {performed_at.date().isoformat()} is in the future"
        )
    elif review_age > block["max_review_age_days"]:
        policy_failures.append(
            f"Review is {review_age} days old; maximum is "
            f"{block['max_review_age_days']}"
        )

    if block["require_current_commit"]:
        reviewed_commit = review["review"].get("commit")
        if commit_root is None:
            policy_failures.append(
                "Current-commit matching is unsupported for portfolio reviews; "
                "use explicit per-project commits and freshness policy"
            )
        elif not reviewed_commit:
            policy_failures.append(
                "Policy requires current commit but the review has no single commit"
            )
        else:
            head = current_git_commit(commit_root)
            if head != reviewed_commit:
                policy_failures.append(
                    f"Review commit {reviewed_commit} does not match HEAD {head}"
                )

    active_baseline: dict[str, dict[str, Any]] = {}
    expired_baseline: list[str] = []
    for entry in baseline["findings"]:
        if active_until(entry.get("expires_on"), evaluation_date):
            active_baseline[entry["id"]] = entry
        else:
            expired_baseline.append(entry["id"])

    active_waivers: dict[str, dict[str, Any]] = {}
    expired_waivers: list[str] = []
    for entry in policy["waivers"]:
        if active_until(entry["expires_on"], evaluation_date):
            active_waivers[entry["finding_id"]] = entry
        else:
            expired_waivers.append(entry["finding_id"])

    blocking: list[dict[str, Any]] = []
    baselined: list[str] = []
    waived: list[str] = []
    unverified: list[str] = []

    for finding in review["findings"]:
        if finding["kind"] != "risk":
            continue
        if finding["severity"] not in block["severities"]:
            continue
        if finding["status"] not in block["statuses"]:
            continue
        if finding["confidence"] < block["minimum_confidence"]:
            continue

        finding_id = finding["id"]
        if finding["verification"]["status"] != "confirmed":
            unverified.append(finding_id)
            if block["unverified_behavior"] == "fail":
                blocking.append(
                    {
                        "id": finding_id,
                        "severity": finding["severity"],
                        "title": finding["title"],
                        "reason": "unverified finding matches blocking thresholds",
                    }
                )
            elif block["unverified_behavior"] == "warn":
                warnings.append(
                    f"Unverified finding {finding_id} matches blocking thresholds"
                )
            continue

        if finding_id in active_baseline:
            baselined.append(finding_id)
        elif finding_id in active_waivers:
            waived.append(finding_id)
        else:
            blocking.append(
                {
                    "id": finding_id,
                    "severity": finding["severity"],
                    "title": finding["title"],
                    "reason": "confirmed finding matches blocking thresholds",
                }
            )

    blocking.sort(key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["id"]))
    passed = not blocking and not policy_failures
    return {
        "status": "pass" if passed else "fail",
        "review": str(review_path),
        "review_id": review["review"]["id"],
        "evaluated_on": evaluation_date.isoformat(),
        "blocking": blocking,
        "policy_failures": policy_failures,
        "baselined": sorted(baselined),
        "waived": sorted(waived),
        "unverified": sorted(unverified),
        "expired_baseline": sorted(expired_baseline),
        "expired_waivers": sorted(expired_waivers),
        "warnings": warnings,
    }


def gate_project(
    project_root: Path,
    review_path: Path | None,
    today: date | None = None,
) -> dict[str, Any]:
    project_root = project_root.resolve()
    return gate_from_config(
        project_root,
        project_root / ".architecture",
        review_path,
        today,
        commit_root=project_root,
    )


def gate_portfolio(
    portfolio_root: Path,
    review_path: Path | None,
    today: date | None = None,
) -> dict[str, Any]:
    portfolio_root = portfolio_root.resolve()
    return gate_from_config(
        portfolio_root,
        portfolio_root / ".architecture-portfolio",
        review_path,
        today,
    )


def print_gate_result(result: dict[str, Any]) -> None:
    print(f"Architecture gate: {result['status'].upper()}")
    print(f"Review: {result['review_id']} ({result['review']})")
    for failure in result["policy_failures"]:
        print(f"POLICY: {failure}")
    for finding in result["blocking"]:
        print(
            f"BLOCK: {finding['id']} [{finding['severity']}] "
            f"{finding['title']} — {finding['reason']}"
        )
    if result["baselined"]:
        print("BASELINED: " + ", ".join(result["baselined"]))
    if result["waived"]:
        print("WAIVED: " + ", ".join(result["waived"]))
    if result["expired_baseline"]:
        print("EXPIRED BASELINE: " + ", ".join(result["expired_baseline"]))
    if result["expired_waivers"]:
        print("EXPIRED WAIVER: " + ", ".join(result["expired_waivers"]))
    for warning in result["warnings"]:
        print(f"WARN: {warning}")


def append_repeatable(parser: argparse.ArgumentParser, flag: str, dest: str) -> None:
    parser.add_argument(flag, dest=dest, action="append", default=[])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage architecture profiles, reviews, and quality gates."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {TOOL_VERSION}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    project = subparsers.add_parser(
        "init-project",
        help="Create .architecture configuration without overwriting existing files.",
    )
    project.add_argument("--repo", default=".")
    project.add_argument("--name")
    project.add_argument("--id", dest="project_id")
    project.add_argument(
        "--lifecycle",
        choices=["experimental", "active", "maintenance", "retiring"],
        default="active",
    )
    project.add_argument(
        "--criticality",
        choices=["low", "medium", "high", "mission-critical"],
        default="medium",
    )
    project.add_argument(
        "--data-classification",
        choices=["public", "internal", "confidential", "restricted", "mixed"],
        default="internal",
    )
    append_repeatable(project, "--type", "types")
    append_repeatable(project, "--owner", "owners")
    append_repeatable(project, "--quality", "qualities")
    append_repeatable(project, "--review", "reviews")
    append_repeatable(project, "--rule-pack", "rule_packs")

    portfolio = subparsers.add_parser(
        "init-portfolio",
        help="Create .architecture-portfolio configuration.",
    )
    portfolio.add_argument("--root", default=".")
    portfolio.add_argument("--name")
    portfolio.add_argument("--id", dest="portfolio_id")
    portfolio.add_argument("--review-horizon-months", type=int, default=12)
    append_repeatable(portfolio, "--owner", "owners")

    validate_project_parser = subparsers.add_parser(
        "validate-project",
        help="Validate project configuration and review artifacts.",
    )
    validate_project_parser.add_argument("root", nargs="?", default=".")

    validate_portfolio_parser = subparsers.add_parser(
        "validate-portfolio",
        help="Validate portfolio configuration and review artifacts.",
    )
    validate_portfolio_parser.add_argument("root", nargs="?", default=".")

    validate_review_parser = subparsers.add_parser(
        "validate-review",
        help="Validate one candidate or verified review.",
    )
    validate_review_parser.add_argument("path")

    validate_plan_parser = subparsers.add_parser(
        "validate-plan",
        help="Validate one remediation plan.",
    )
    validate_plan_parser.add_argument("path")

    gate = subparsers.add_parser(
        "gate",
        help="Evaluate a verified review against deterministic policy.",
    )
    gate_target = gate.add_mutually_exclusive_group()
    gate_target.add_argument("--project")
    gate_target.add_argument("--portfolio")
    gate.add_argument("--review")
    gate.add_argument("--json", action="store_true", dest="json_output")
    return parser


def run(args: argparse.Namespace) -> int:
    if args.command == "init-project":
        target = init_project(args)
        print(f"Initialized project architecture configuration: {target}")
        return 0
    if args.command == "init-portfolio":
        if not 1 <= args.review_horizon_months <= 60:
            raise ArchitectureError("--review-horizon-months must be between 1 and 60")
        target = init_portfolio(args)
        print(f"Initialized portfolio architecture configuration: {target}")
        return 0
    if args.command == "validate-project":
        validated = validate_project(Path(args.root))
        print(f"Project architecture configuration is valid ({len(validated)} files).")
        return 0
    if args.command == "validate-portfolio":
        validated = validate_portfolio(Path(args.root))
        print(
            f"Portfolio architecture configuration is valid ({len(validated)} files)."
        )
        return 0
    if args.command == "validate-review":
        validate_review(Path(args.path).resolve())
        print("Architecture review is valid.")
        return 0
    if args.command == "validate-plan":
        validate_plan(Path(args.path).resolve())
        print("Architecture remediation plan is valid.")
        return 0
    if args.command == "gate":
        review_path = Path(args.review) if args.review else None
        if args.portfolio:
            result = gate_portfolio(Path(args.portfolio), review_path)
        else:
            result = gate_project(Path(args.project or "."), review_path)
        if args.json_output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_gate_result(result)
        return 0 if result["status"] == "pass" else 1
    raise ArchitectureError(f"Unknown command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except ArchitectureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
