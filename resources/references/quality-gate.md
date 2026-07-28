# Architecture quality gate contract

The gate is deterministic. It consumes schemas, a verified review, policy, baseline, and waivers; it does not ask a model to reassess architecture.

## Inputs

Project inputs:

```text
.architecture/gate-policy.yaml
.architecture/baseline.yaml
.architecture/reviews/*-verified.yaml
```

Portfolio inputs use the same policy contracts under `.architecture-portfolio/`.

Use an explicitly supplied review when reproducibility matters. Otherwise the tool selects the lexically latest verified review.

## Evaluation

The gate:

1. validates all files;
2. checks that the review lifecycle is `verified`;
3. checks review age and optional commit policy;
4. selects risk findings;
5. applies verification, confidence, severity, and lifecycle filters;
6. applies active baseline entries and waivers;
7. reports blockers and exits predictably.

Only confirmed risks block by default. Candidate, rejected, and needs-evidence findings are reported according to `unverified_behavior`.

## Baseline versus waiver

- Baseline: acknowledges a pre-existing confirmed finding while preventing it from being treated as newly introduced. Include owner, reason, recorded date, and optional expiry.
- Waiver: accepts a specific gate exception temporarily. Owner, reason, and expiry are mandatory.

Neither changes the finding's verification or lifecycle status. Expired entries are inactive.

Use stable finding IDs. Do not baseline wildcard rules or severities.

## CI command

```bash
python3 /absolute/path/to/architecture_tool.py gate \
  --project "$REPOSITORY_ROOT" \
  --review "$REVIEW_ARTIFACT"
```

Use `--portfolio "$PORTFOLIO_ROOT"` for a portfolio review.

Exit codes:

- `0`: policy passed;
- `1`: valid inputs but the policy failed;
- `2`: missing or invalid inputs.

JSON output is available with `--json`.

## Policy changes

Changing blocked severities, confidence, freshness, commit matching, baseline, or waivers is a governance decision. Review the exact findings whose result changes. Never modify policy as part of running the gate.
