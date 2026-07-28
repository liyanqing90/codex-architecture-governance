#!/usr/bin/env python3
"""Generate reproducible hashes for architecture artifacts and findings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from architecture_tool import (
    ArchitectureError,
    canonical_sha256,
    file_sha256,
    finding_fingerprint,
    load_yaml,
)


def fingerprint(path: Path, subject_id: str | None) -> dict[str, Any]:
    path = path.expanduser().resolve()
    payload = load_yaml(path)
    result: dict[str, Any] = {
        "path": str(path),
        "file_sha256": file_sha256(path),
        "canonical_sha256": canonical_sha256(payload),
    }
    if "review" in payload:
        review_subject = payload["review"]["subject"]["id"]
        result["kind"] = "review"
        result["artifact_id"] = payload["review"]["id"]
        result["findings"] = [
            {
                "id": finding["id"],
                "fingerprint": finding_fingerprint(review_subject, finding),
                "evidence_fingerprint": canonical_sha256(finding["evidence"]),
            }
            for finding in payload["findings"]
        ]
    elif "decision" in payload:
        result["kind"] = "architecture-decision"
        result["artifact_id"] = payload["decision"]["id"]
    elif "plan" in payload:
        result["kind"] = "remediation-plan"
        result["artifact_id"] = payload["plan"]["id"]
    elif "run" in payload:
        result["kind"] = "evidence-run"
        result["artifact_id"] = payload["run"]["id"]
    elif "id" in payload and "rule_id" in payload:
        if subject_id is None:
            raise ArchitectureError("A standalone Finding requires --subject-id")
        result["kind"] = "finding"
        result["artifact_id"] = payload["id"]
        result["finding_fingerprint"] = finding_fingerprint(subject_id, payload)
        result["evidence_fingerprint"] = canonical_sha256(payload["evidence"])
    else:
        result["kind"] = "generic-artifact"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--subject-id")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = fingerprint(args.artifact, args.subject_id)
    except (ArchitectureError, OSError) as exc:
        print(f"Artifact fingerprint failed: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        output = args.output.expanduser().resolve()
        if output.exists():
            print(
                f"Artifact fingerprint failed: refusing to overwrite {output}",
                file=sys.stderr,
            )
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Artifact fingerprint written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
