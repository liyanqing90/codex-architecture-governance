#!/usr/bin/env python3
"""Run benchmark cases through a caller-supplied agent command."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def relative_to_root(root: Path, path: Path, label: str) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root: {resolved}") from exc


def tree_manifest(path: Path) -> tuple[str, int]:
    records = []
    for child in sorted(item for item in path.rglob("*") if item.is_file()):
        records.append(
            {
                "path": child.relative_to(path).as_posix(),
                "sha256": file_sha256(child),
            }
        )
    return sha256_bytes(canonical_json(records).encode()), len(records)


def git_output(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise ValueError(process.stderr.strip() or "Git command failed")
    return process.stdout.strip()


def collect_provenance(
    *,
    root: Path,
    corpus_path: Path,
    corpus: dict,
    command: list[str],
) -> dict:
    schema_root = root / "resources" / "schemas"
    input_specs = (
        ("ground-truth", corpus_path),
        ("benchmark-schema", schema_root / "benchmark.schema.json"),
        ("observation-schema", schema_root / "benchmark-observation.schema.json"),
        ("dependency-lock", root / "requirements-runtime.lock"),
        ("knowledge-manifest", root / "resources" / "knowledge" / "manifest.yaml"),
    )
    inputs = [
        {
            "role": role,
            "path": relative_to_root(root, path, role),
            "sha256": file_sha256(path),
        }
        for role, path in input_specs
    ]

    runner = Path(__file__).resolve()
    tool_paths = [runner]
    for token in command:
        candidate = Path(token)
        if not candidate.is_absolute():
            candidate = root / candidate
        if candidate.is_file():
            try:
                relative_to_root(root, candidate, "command tool")
            except ValueError:
                continue
            tool_paths.append(candidate.resolve())
    tools = []
    seen_paths: set[str] = set()
    for path in tool_paths:
        relative = relative_to_root(root, path, "tool")
        if relative in seen_paths:
            continue
        seen_paths.add(relative)
        tools.append(
            {
                "id": (
                    "benchmark-runner"
                    if path == runner
                    else path.stem.replace("_", "-")
                ),
                "path": relative,
                "sha256": file_sha256(path),
            }
        )

    fixtures = []
    for case in corpus["cases"]:
        fixture = (root / case["fixture"]).resolve()
        relative = relative_to_root(root, fixture, f"case {case['id']} fixture")
        digest, file_count = tree_manifest(fixture)
        fixtures.append(
            {
                "case_id": case["id"],
                "path": relative,
                "sha256": digest,
                "file_count": file_count,
            }
        )

    tracked_paths = [item["path"] for item in inputs]
    tracked_paths.extend(item["path"] for item in tools)
    tracked_paths.extend(item["path"] for item in fixtures)
    dirty = bool(
        git_output(
            root,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            *tracked_paths,
        )
    )
    return {
        "source": {
            "repository": ".",
            "commit": git_output(root, "rev-parse", "HEAD"),
            "dirty": dirty,
        },
        "environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "command_template_sha256": sha256_bytes(
            canonical_json(command).encode("utf-8")
        ),
        "inputs": inputs,
        "fixtures": fixtures,
        "tools": tools,
    }


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
    output_path = args.output.resolve()
    log_path = output_path.with_suffix(".log.jsonl")
    corpus = load_yaml(corpus_path)
    schema_path = root / "resources" / "schemas" / "benchmark.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    observation_schema_path = (
        root / "resources" / "schemas" / "benchmark-observation.schema.json"
    )
    observation_schema = json.loads(observation_schema_path.read_text(encoding="utf-8"))
    # Keep the standalone observation schema usable by model surfaces while
    # avoiding network or resolver behavior during local validation.
    observation_schema["properties"]["usage"] = schema["$defs"]["trial"]["properties"][
        "usage"
    ]
    validate(corpus, schema, corpus_path)
    if corpus["benchmark"]["kind"] != "ground-truth":
        raise ValueError("Benchmark input must be ground truth")
    provenance = collect_provenance(
        root=root,
        corpus_path=corpus_path,
        corpus=corpus,
        command=args.command,
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("", encoding="utf-8")
    log_records = 0

    result = {
        "schema_version": "1.3",
        "benchmark": {
            "id": corpus["benchmark"]["id"],
            "version": corpus["benchmark"]["version"],
            "kind": "run",
            "model": args.model,
            "surface": args.surface,
            "skill_version": args.skill_version,
            "run_at": datetime.now(UTC).isoformat(),
            "repetitions": repetitions,
            "provenance": provenance,
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
            command_sha256 = sha256_bytes(canonical_json(command).encode("utf-8"))
            stdout_sha256 = sha256_bytes(process.stdout.encode("utf-8"))
            stderr_sha256 = sha256_bytes(process.stderr.encode("utf-8"))
            if process.returncode != 0:
                failed_record = {
                    "schema_version": "1.0",
                    "case_id": case["id"],
                    "trial_index": trial_index,
                    "duration_seconds": duration_seconds,
                    "exit_code": process.returncode,
                    "command_sha256": command_sha256,
                    "stdout_sha256": stdout_sha256,
                    "stderr_sha256": stderr_sha256,
                    "observation": None,
                }
                with log_path.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(canonical_json(failed_record) + "\n")
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
            validate(observed, observation_schema, observation_schema_path)
            log_record = {
                "schema_version": "1.0",
                "case_id": case["id"],
                "trial_index": trial_index,
                "duration_seconds": duration_seconds,
                "exit_code": process.returncode,
                "command_sha256": command_sha256,
                "stdout_sha256": stdout_sha256,
                "stderr_sha256": stderr_sha256,
                "observation": observed,
            }
            log_record_text = canonical_json(log_record)
            with log_path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(log_record_text + "\n")
            log_records += 1
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
                "execution": {
                    "exit_code": process.returncode,
                    "command_sha256": command_sha256,
                    "stdout_sha256": stdout_sha256,
                    "stderr_sha256": stderr_sha256,
                    "observation_sha256": sha256_bytes(
                        canonical_json(observed).encode("utf-8")
                    ),
                    "log_record_sha256": sha256_bytes(log_record_text.encode("utf-8")),
                },
            }
            observed_decision = observed.get("observed_decision")
            if case.get("expected_decision") is not None:
                if observed_decision is None:
                    raise ValueError(
                        f"Case {case['id']} requires observed_decision output"
                    )
                trial["observed_decision"] = observed_decision
            elif observed_decision is not None:
                trial["observed_decision"] = observed_decision
            usage = observed.get("usage")
            if usage is not None:
                if not isinstance(usage, dict):
                    raise ValueError(f"Case {case['id']} usage must be an object")
                trial["usage"] = usage
            trials.append(trial)
        first_trial = trials[0]
        result_case = {
            "id": case["id"],
            "fixture": case["fixture"],
            "expected_findings": [],
            "forbidden_recommendations": [],
            "observed_findings": first_trial["observed_findings"],
            "observed_recommendations": first_trial["observed_recommendations"],
            "trials": trials,
        }
        if "observed_decision" in first_trial:
            result_case["observed_decision"] = first_trial["observed_decision"]
        result["cases"].append(result_case)
    provenance["execution_log"] = {
        "path": log_path.name,
        "format": "jsonl",
        "sha256": file_sha256(log_path),
        "records": log_records,
    }
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
    parser.add_argument("--skill-version", default="0.4.0")
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
