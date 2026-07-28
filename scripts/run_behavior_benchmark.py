#!/usr/bin/env python3
"""Run benchmark cases through a caller-supplied agent command."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def load_yaml(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a mapping")
    return payload


def validate(payload: dict, schema: dict, source: Path) -> None:
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(payload),
        key=lambda error: list(error.path),
    )
    if errors:
        detail = "; ".join(error.message for error in errors)
        raise ValueError(f"{source} is invalid: {detail}")


def render_command(
    template: list[str],
    *,
    skill: str,
    fixture: Path,
    prompt: str,
) -> list[str]:
    values = {
        "skill": skill,
        "fixture": str(fixture),
        "prompt": prompt,
    }
    rendered: list[str] = []
    for part in template:
        for key, value in values.items():
            part = part.replace(f"{{{key}}}", value)
        rendered.append(part)
    return rendered


def evidence_is_valid(fixture: Path, evidence: object) -> bool:
    if not isinstance(evidence, list) or not evidence:
        return False
    fixture = fixture.resolve()
    for record in evidence:
        if not isinstance(record, dict):
            return False
        if set(record) != {"path", "line_start", "line_end", "excerpt"}:
            return False
        if not isinstance(record["path"], str):
            return False
        relative = Path(record["path"])
        if relative.is_absolute() or ".." in relative.parts:
            return False
        source = (fixture / relative).resolve()
        try:
            source.relative_to(fixture)
            lines = source.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError, ValueError):
            return False
        line_start = record["line_start"]
        line_end = record["line_end"]
        if (
            not isinstance(line_start, int)
            or not isinstance(line_end, int)
            or line_start < 1
            or line_end < line_start
            or line_end > len(lines)
        ):
            return False
        selected = "\n".join(lines[line_start - 1 : line_end])
        if not isinstance(record["excerpt"], str) or record["excerpt"] not in selected:
            return False
    return True


def run_benchmark(args: argparse.Namespace) -> dict:
    root = args.root.resolve()
    repetitions = getattr(args, "repetitions", 1)
    corpus_path = args.ground_truth.resolve()
    corpus = load_yaml(corpus_path)
    schema_path = root / "resources" / "schemas" / "benchmark.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(corpus, schema, corpus_path)
    if corpus["benchmark"]["kind"] != "ground-truth":
        raise ValueError("Benchmark input must be ground truth")

    result = {
        "schema_version": "1.1",
        "benchmark": {
            "id": corpus["benchmark"]["id"],
            "version": corpus["benchmark"]["version"],
            "kind": "run",
            "model": args.model,
            "surface": args.surface,
            "skill_version": args.skill_version,
            "run_at": datetime.now(UTC).isoformat(),
            "repetitions": repetitions,
        },
        "cases": [],
    }
    for case in corpus["cases"]:
        fixture = (root / case["fixture"]).resolve()
        try:
            fixture.relative_to(root)
        except ValueError as exc:
            raise ValueError(
                f"Case {case['id']} fixture escapes benchmark root"
            ) from exc
        if not fixture.is_dir():
            raise ValueError(f"Case {case['id']} fixture is missing: {fixture}")
        trials = []
        for trial_index in range(1, repetitions + 1):
            command = render_command(
                args.command,
                skill=case["skill"],
                fixture=fixture,
                prompt=case["prompt"],
            )
            started = time.monotonic()
            process = subprocess.run(
                command,
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
                timeout=args.timeout,
            )
            duration_seconds = time.monotonic() - started
            if process.returncode != 0:
                raise RuntimeError(
                    f"Case {case['id']} trial {trial_index} failed "
                    f"({process.returncode}): {process.stderr.strip()}"
                )
            try:
                observed = json.loads(process.stdout)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Case {case['id']} trial {trial_index} did not return JSON: {exc}"
                ) from exc
            if not isinstance(observed, dict):
                raise ValueError(
                    f"Case {case['id']} trial {trial_index} output must be "
                    "a JSON object"
                )
            observed_findings = observed.get("observed_findings", [])
            observed_recommendations = observed.get(
                "observed_recommendations",
                [],
            )
            if not isinstance(observed_findings, list):
                raise ValueError(
                    f"Case {case['id']} observed_findings must be an array"
                )
            if not isinstance(observed_recommendations, list):
                raise ValueError(
                    f"Case {case['id']} observed_recommendations must be an array"
                )
            normalized_findings = []
            for index, finding in enumerate(observed_findings):
                if not isinstance(finding, dict):
                    raise ValueError(
                        f"Case {case['id']} finding {index} must be an object"
                    )
                evidence = finding.get("evidence", [])
                normalized_findings.append(
                    {
                        "rule_id": finding.get("rule_id"),
                        "severity": finding.get("severity"),
                        "evidence": evidence,
                        "evidence_valid": evidence_is_valid(fixture, evidence),
                    }
                )
            trial = {
                "index": trial_index,
                "duration_seconds": duration_seconds,
                "observed_findings": normalized_findings,
                "observed_recommendations": observed_recommendations,
            }
            usage = observed.get("usage")
            if usage is not None:
                if not isinstance(usage, dict):
                    raise ValueError(f"Case {case['id']} usage must be an object")
                trial["usage"] = usage
            trials.append(trial)
        first_trial = trials[0]
        result["cases"].append(
            {
                "id": case["id"],
                "fixture": case["fixture"],
                "expected_findings": [],
                "forbidden_recommendations": [],
                "observed_findings": first_trial["observed_findings"],
                "observed_recommendations": first_trial["observed_recommendations"],
                "trials": trials,
            }
        )
    validate(result, schema, args.output)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run architecture benchmark cases through a command whose stdout "
            "is a JSON observation."
        )
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--ground-truth",
        type=Path,
        default=Path("benchmarks/ground-truth.yaml"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--surface", required=True)
    parser.add_argument("--skill-version", default="0.3.1")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--repetitions", type=int, default=1, choices=range(1, 21))
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help=(
            "Command arguments after --. Use {skill}, {fixture}, and {prompt} "
            "placeholders."
        ),
    )
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command template is required after --")
    return args


def main() -> None:
    args = parse_args()
    result = run_benchmark(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(result, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote benchmark run: {args.output}")


if __name__ == "__main__":
    main()
