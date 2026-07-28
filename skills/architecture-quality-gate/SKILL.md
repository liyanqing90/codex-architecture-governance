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

## Procedure

1. Locate the project `.architecture/` or portfolio `.architecture-portfolio/` policy, baseline, and explicitly supplied or latest `*-verified.yaml` review.
2. Validate all inputs before evaluating them.
3. Run the deterministic gate:

```bash
python3 ../../resources/scripts/architecture_tool.py gate --project <repo> [--review <verified-review.yaml>] [--json]
```

Use `--portfolio <portfolio-root>` for portfolio reviews.

Resolve the script path from this Skill's directory.

4. Report the exact blocking finding IDs, expired waivers, baselined findings, ignored unverified findings, and freshness failures.
5. Preserve exit codes:
   - `0`: pass;
   - `1`: policy failure;
   - `2`: invalid or missing input.

## Integrity rules

- Gate only `kind: risk`, `verification.status: confirmed` findings.
- Never upgrade severity or confidence during gate execution.
- Never let an unverified finding block unless policy explicitly sets `unverified_behavior: fail`.
- Require a reason, owner, and expiry for every waiver.
- Treat expired baselines and waivers as inactive.
- Do not create a waiver or baseline entry merely to make CI pass.
- Do not modify product code, findings, policy, baseline, or waivers while running the gate.

If a user asks to change gate policy or accept risk, present the exact impact and treat that as a separate governance decision.
