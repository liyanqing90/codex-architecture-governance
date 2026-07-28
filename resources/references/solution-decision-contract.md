# Architecture solution decision contract

Use `../schemas/architecture-decision.schema.json` after a verified review and
before remediation planning.

## Decision boundary

A decision solves confirmed findings or an explicit quality-attribute
scenario. It does not discover findings, accept risk, plan implementation, or
authorize change.

Always include a keep-current/local-correction option. Add structural options
only when current constraints support them. Compare at least three options.
Every option records benefits, liabilities, assumptions, all declared
quality-attribute effects, business/team/evolution fit, complexity tier,
implementation and operational complexity, maturity and lock-in, migration
risk, reversibility, cost, and the complete trade-off scorecard.

Use the catalogs under `../knowledge/` as maintained decision evidence:

- quality model for vocabulary and scenarios;
- styles for system organization;
- patterns for bounded mechanisms;
- technology profiles for implementation capabilities and lock-in;
- reference architectures for complete control/data paths;
- migrations for staged evolution;
- domain guidance for specialist requirements;
- decision guides for hard rejection rules.

Catalog entries do not override project evidence. A technology's capability
does not prove project fit.

## Status and authority

- `proposed`: advisor output awaiting authority;
- `accepted`: authorized decision that may enter remediation;
- `rejected`: considered but not selected for implementation;
- `superseded`: replaced by another recorded decision.

Bind the decision to the verified Review ID and file SHA-256. Bind every cited
architecture style, pattern, and technology profile to the exact current
catalog version and SHA-256. Include only confirmed, unresolved Finding IDs.
Record hard eliminations, why every nonselected option was rejected, all
decision makers, and at least one measurable revisit trigger.

Generate the non-inferable bindings with:

```bash
python3 ../scripts/architecture_tool.py decision-bindings \
  --project <repository-root> --review <verified-review.yaml>
```

Validate with:

```bash
python3 ../scripts/architecture_tool.py validate-decision \
  <decision.yaml> --review <verified-review.yaml> --project <repository-root>
```
