---
name: architecture-quality-gate
description: Deterministic architecture quality gate for verified review artifacts. Use in local checks or CI to validate architecture configuration, block configured confirmed severities, enforce review freshness, and honor explicit baselines or time-limited waivers. Never treats raw model findings as gate failures and never replaces finding verification.
---

# Run the architecture quality gate

Evaluate machine-readable, verified findings against repository policy. Do not reinterpret or silently rewrite the policy.

## Load the contract

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/quality-gate.md`
- `../../resources/references/evidence-provider-contract.md`

## Procedure

1. Locate the project `.architecture/` or portfolio
   `.architecture-portfolio/` policy, baseline, risk-acceptance registry, and
   explicitly supplied or newest-by-`performed_at` verified review.
2. Validate all inputs before evaluating them.
3. Run the deterministic gate:

```bash
python3 ../../resources/scripts/architecture_tool.py gate \
  --project <repo> \
  [--review <verified-review.yaml>] \
  [--base-commit <ancestor>] \
  [--stage contract|finding|change|release|all] \
  [--json] [--sarif-output <results.sarif>]
```

Use `--portfolio <portfolio-root>` for portfolio reviews.

Resolve the script path from this Skill's directory.

4. Report contract failures, missing required review workflows, Evidence
   Provider resolution, changed paths and public-contract classifications,
   exact blocking IDs, verification/signature failures, unauthorized or
   overlapping roles, incomplete plans, expired acceptances and waivers,
   baselined or waived findings, and accepted risks.
5. Preserve exit codes:
   - `0`: pass;
   - `1`: policy failure;
   - `2`: invalid or missing input.

## Integrity rules

- Gate only `kind: risk`, `verification.status: confirmed` findings.
- Never upgrade severity or confidence during gate execution.
- Never let an unverified finding block unless policy explicitly sets `unverified_behavior: fail`.
- Require an exact Finding fingerprint, reason, approval identity, and expiry
  for every waiver.
- Require a separate authorized accepter and policy approver, compensating
  controls, exact fingerprint, and expiry for every accepted risk.
- Treat expired baselines, waivers, and risk acceptances as inactive.
- Reject legacy `1.0` artifacts for enforcement while preserving migration
  readability.
- Require passed, hash-valid provider runs for configured release evidence and
  V4/V5 verification.
- Require every complete plan item to cover its declared acceptance evidence
  types with repository-contained, hash-valid evidence.
- Do not create a waiver or baseline entry merely to make CI pass.
- Do not modify product code, findings, policy, baseline, or waivers while running the gate.

If a user asks to change gate policy or accept risk, present the exact impact
and treat that as a separate governance decision. Never encode acceptance by
editing only `finding.status`.
