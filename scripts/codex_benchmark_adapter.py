#!/usr/bin/env python3
"""Run one benchmark case through Codex with a structured observation contract."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

CANONICAL_TRADEOFFS = (
    "availability",
    "client-complexity",
    "consistency",
    "cost",
    "delivery-semantics",
    "deployment-independence",
    "evaluation",
    "implementation-complexity",
    "latency",
    "maintainability",
    "migration-risk",
    "offline-capability",
    "operational-complexity",
    "recovery",
    "reliability",
    "reversibility",
    "routing-complexity",
    "safety",
    "security",
    "team-ownership",
)


def within(root: Path, value: Path, label: str) -> Path:
    resolved = value.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root: {resolved}") from exc
    return resolved


def build_prompt(
    *,
    skill_path: Path,
    knowledge_root: Path,
    fixture: Path,
    task: str,
) -> str:
    solution_output = ""
    if skill_path.parent.name == "architecture-solution-advisor":
        tradeoffs = ", ".join(CANONICAL_TRADEOFFS)
        solution_output = f"""
This is a solution-advisor case. Also return observed_decision with:
- selected_option: the canonical selected knowledge ID without its kind prefix
  (style.web-queue-worker becomes web-queue-worker), or the exact slug of a
  Decision Guide option heading (Single agent with tools becomes
  single-agent-with-tools). Never add keep, retain, adopt, current, display,
  or another synonym;
- compared_tradeoffs: atomic IDs from this canonical vocabulary only:
  {tradeoffs}. Record each dimension separately; never combine dimensions into
  an A-vs-B identifier;
- knowledge_ids: only IDs from knowledge entries you actually used;
- rejected_options: at least two viable options with evidence-backed reasons;
- migration_slices: concrete reversible slices, even when retaining the design.
"""
    else:
        solution_output = """
This is not a solution-advisor case. Return observed_decision with
selected_option set to "not-applicable" and all four array fields empty.
"""
    return f"""Read and follow the Skill completely:
{skill_path}

Inspect only this benchmark fixture and its files:
{fixture}

The architecture knowledge catalog is read-only at:
{knowledge_root}

Task:
{task}

Return only JSON matching the provided output schema. Report a finding only when
the fixture directly proves a machine Rule Pack invariant. Use only a Rule ID
allowed by the output schema; never use a Knowledge or Pattern ID as rule_id.
Each finding must cite a fixture-relative path and the smallest possible exact
excerpt. Prefer one line per evidence item, copy every leading space exactly,
and never insert an ellipsis or join non-contiguous lines. Do not invent
runtime, scale, team, compliance, or production evidence. Put architecture
recommendations in observed_recommendations; use an empty list when no change
is justified.
{solution_output}
"""


def allowed_rule_ids(root: Path) -> list[str]:
    result: set[str] = set()
    for path in sorted((root / "resources" / "rules").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        result.update(rule["id"] for rule in payload["rules"])
    if not result:
        raise RuntimeError("No machine Rule Pack IDs are available")
    return sorted(result)


def evidence_errors(observation: dict, fixture: Path) -> list[str]:
    errors: list[str] = []
    fixture = fixture.resolve()
    for finding in observation["observed_findings"]:
        for index, evidence in enumerate(finding["evidence"], start=1):
            relative = Path(evidence["path"])
            label = f"{finding['rule_id']} evidence {index}"
            if relative.is_absolute() or ".." in relative.parts:
                errors.append(f"{label} path is not fixture-relative")
                continue
            source = (fixture / relative).resolve()
            try:
                source.relative_to(fixture)
                lines = source.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError, ValueError):
                errors.append(f"{label} path cannot be read")
                continue
            line_start = evidence["line_start"]
            line_end = evidence["line_end"]
            if line_end < line_start or line_end > len(lines):
                errors.append(f"{label} line range is invalid")
                continue
            selected = "\n".join(lines[line_start - 1 : line_end])
            if evidence["excerpt"] not in selected:
                errors.append(f"{label} excerpt is not verbatim in its line range")
    return errors


def validate_observation(observation: dict, schema: dict) -> None:
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(observation),
        key=lambda error: list(error.path),
    )
    if errors:
        raise ValueError(
            "Codex observation failed schema validation: "
            + "; ".join(error.message for error in errors)
        )


def execute_codex(
    *,
    codex: str,
    model: str,
    fixture: Path,
    schema_path: Path,
    output_path: Path,
    prompt: str,
    timeout: int,
) -> dict:
    command = [
        codex,
        "exec",
        "--model",
        model,
        "--cd",
        str(fixture),
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
        prompt,
    ]
    process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise RuntimeError(
            f"Codex benchmark case failed ({process.returncode}): {detail}"
        )
    if not output_path.is_file():
        raise RuntimeError("Codex did not write a structured observation")
    return json.loads(output_path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parent.parent)
    parser.add_argument("--model", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--codex", default="codex")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    fixture = within(root, args.fixture, "fixture")
    skill_path = within(
        root,
        root / "skills" / args.skill / "SKILL.md",
        "Skill",
    )
    if not fixture.is_dir():
        raise ValueError(f"Fixture is not a directory: {fixture}")
    if not skill_path.is_file():
        raise ValueError(f"Skill is missing: {skill_path}")
    schema_path = within(
        root,
        root / "resources" / "schemas" / "benchmark-observation.schema.json",
        "observation schema",
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["properties"]["observed_findings"]["items"]["properties"]["rule_id"] = {
        "type": "string",
        "enum": allowed_rule_ids(root),
    }
    codex = shutil.which(args.codex)
    if codex is None:
        raise RuntimeError(f"Codex executable is unavailable: {args.codex}")
    prompt = build_prompt(
        skill_path=skill_path,
        knowledge_root=root / "resources" / "knowledge",
        fixture=fixture,
        task=args.prompt,
    )
    with tempfile.TemporaryDirectory(prefix="architecture-benchmark-") as temporary:
        temporary_root = Path(temporary)
        runtime_schema_path = temporary_root / "observation.schema.json"
        runtime_schema_path.write_text(
            json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        observation = {}
        for attempt in range(2):
            output_path = temporary_root / f"observation-{attempt + 1}.json"
            observation = execute_codex(
                codex=codex,
                model=args.model,
                fixture=fixture,
                schema_path=runtime_schema_path,
                output_path=output_path,
                prompt=prompt,
                timeout=args.timeout,
            )
            validate_observation(observation, schema)
            invalid_evidence = evidence_errors(observation, fixture)
            if not invalid_evidence:
                break
            if attempt == 1:
                detail = "; ".join(invalid_evidence)
                raise RuntimeError(
                    "Codex could not produce exact fixture evidence after one "
                    f"bounded correction: {detail}"
                )
            prompt = f"""Reread the fixture and correct only the invalid evidence
in this prior observation:

{json.dumps(observation, ensure_ascii=False)}

Validation errors:
{chr(10).join(f"- {error}" for error in invalid_evidence)}

Return the complete JSON observation again. Preserve a finding only when a
fixture-relative, contiguous line range contains its excerpt byte-for-byte.
Prefer a one-line excerpt and copy leading indentation exactly.
"""
    print(json.dumps(observation, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
