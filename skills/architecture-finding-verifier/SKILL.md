---
name: architecture-finding-verifier
description: Independently verifies candidate architecture findings against current code and repository evidence. Use after any project, AI-agent, mobile, or portfolio architecture audit; when a finding may be based on weak heuristics; or before remediation and quality gates. Filters false positives, deduplicates findings, recalibrates severity and confidence, and preserves an auditable decision trail without changing code.
---

# Verify architecture findings

Act as a skeptical second pass. The objective is not to defend the audit; it is to determine which claims survive direct inspection.

## Load the contract

Read `../../resources/references/review-contract.md` completely. Load the candidate review and the repository profile and constraints when present.

## Verification procedure

1. Record the candidate review ID, reviewed commit, current commit, scope, and evidence freshness.
2. If the code has moved, relocate evidence by symbol and history. Mark the finding `needs-evidence` when it cannot be tied to current code.
3. For every candidate, read the cited source and the smallest sufficient set of callers, callees, schemas, tests, configuration, history, or runtime evidence.
4. State the claimed invariant and attempt the strongest counter-hypothesis.
5. Confirm that the evidence proves an architecture relationship or failure mode rather than a stylistic preference.
6. Check the owning boundary, affected components, severity, confidence, and rule ID.
7. Merge genuine duplicates while retaining all original IDs and contributing reviewers.
8. Set exactly one status:
   - `confirmed`: direct evidence supports the claim and impact;
   - `rejected`: evidence contradicts the claim or shows an intentional, safe pattern;
   - `needs-evidence`: the claim remains plausible but cannot be proved.

Do not use cross-reviewer agreement as proof; treat it only as a reason to inspect more carefully.

## Mandatory false-positive checks

Reject or downgrade claims supported only by:

- line count, file count, import count, fan-out, or cyclomatic complexity;
- names such as `utils`, `manager`, `service`, or `singleton`;
- use of SQLite, PostgreSQL, Redis, Neo4j, a global instance, or a framework;
- theoretical scale, security, or availability requirements absent from the profile;
- a document that contradicts current executable behavior;
- a missing pattern that is not applicable to the system.

Metrics and conventions may locate evidence, but cannot be the evidence.

## Output

Never overwrite the candidate artifact. Write:

- `.architecture/reviews/<timestamp>-<kind>-verified.yaml` and
  `.architecture/reviews/<timestamp>-<kind>-report.md`, or
- `.architecture-portfolio/reviews/<timestamp>-portfolio-verified.yaml` and
  `.architecture-portfolio/reviews/<timestamp>-portfolio-report.md`.

Retain rejected and needs-evidence items in YAML, but include only confirmed risks and strengths in the human report. Record the verification rationale and verifier identity for every item.

Preserve the source review structure defined by
`../../resources/templates/review.yaml` or
`../../resources/templates/portfolio-review.yaml`.

Validate the result:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-review <verified-review.yaml>
```

Do not propose remediation or modify product code.
