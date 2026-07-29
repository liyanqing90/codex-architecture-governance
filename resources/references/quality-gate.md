# Architecture quality gate contract

The gate is deterministic. It consumes schemas, a verified review, policy, baseline, and waivers; it does not ask a model to reassess architecture.

## Inputs

Project inputs:

```text
.architecture/gate-policy.yaml
.architecture/baseline.yaml
.architecture/risk-acceptances.yaml
.architecture/evidence-providers.yaml
.architecture/evidence/*.yaml
.architecture/reviews/*-verified.yaml
.architecture/reviews/*-architecture-decision.yaml
.architecture/reviews/*-remediation.yaml
```

Portfolio inputs use the same policy contracts under `.architecture-portfolio/`.

Use an explicitly supplied review when reproducibility matters. Otherwise the
tool selects the verified review with the latest `performed_at`, using ID and
filename only as deterministic tie-breakers.

## Evaluation

The gate:

1. validates all files;
2. checks that the review lifecycle is `verified`;
3. checks artifact bindings, required workflow freshness, exact machine Rule
   Pack coverage, Evidence Provider run hashes, verification level, role
   authority, required role separation, and SSH signature policy;
4. applies time-window, exact-commit, ancestor, or diff-aware freshness;
5. classifies the base-commit diff, including public contracts and persisted
   artifacts that require an accepted decision;
6. selects risk findings;
7. applies confidence, severity, and lifecycle filters;
8. applies fingerprint-bound baseline, waiver, or risk acceptance;
9. applies contract, finding, change, or release stage requirements;
10. at release, checks evidence-type requirements, authorized accepted
    decisions, and complete remediation evidence;
11. reports blockers and exits predictably.

Only confirmed risks block by default. Candidate, rejected, and needs-evidence findings are reported according to `unverified_behavior`.

Stages are cumulative:

- `contract`: schema, identity, provenance, hashes, roles, required review
  workflows, and exact coverage;
- `finding`: confirmed risk policy and accountable suppressions;
- `change`: Git ancestry/diff, public-contract governance, compatible migration
  or active remediation planning, clean-tree, signature, and evidence
  resolution. Governance-only commits may follow a review, but classified
  critical or security paths may not change after the reviewed commit;
- `release`: evidence-type quorum, accepted decision authority, and
  SHA-256-bound completion evidence.

## Baseline versus waiver

- Baseline: acknowledges a pre-existing confirmed finding while preventing it from being treated as newly introduced. Include owner, reason, recorded date, and optional expiry.
- Waiver: accepts a specific gate exception temporarily. Owner, reason, and expiry are mandatory.

Neither changes the finding's verification or lifecycle status. Expired entries are inactive.

Use stable Finding IDs plus exact fingerprints. Do not baseline wildcard rules
or severities. An `accepted-risk` status is blocking unless an active registry
entry has a separate authorized accepter and policy approver, compensating
controls, exact fingerprint, and expiry.

## CI command

```bash
python3 /absolute/path/to/architecture_tool.py gate \
  --project "$REPOSITORY_ROOT" \
  --review "$REVIEW_ARTIFACT" \
  --base-commit "$BASE_COMMIT" \
  --stage all
```

Use `--portfolio "$PORTFOLIO_ROOT"` for a portfolio review.

Exit codes:

- `0`: policy passed;
- `1`: valid inputs but the policy failed;
- `2`: missing or invalid inputs.

JSON output is available with `--json`; GitHub-compatible SARIF is available
with `--sarif-output <path>`.

## Policy changes

Changing blocked severities, confidence, verification level, freshness, commit
matching, role membership/separation, signature requirements, release evidence
types, baseline, or waivers is a governance decision. Review the exact
findings and change classes whose result changes. Never modify policy as part
of running the gate.
