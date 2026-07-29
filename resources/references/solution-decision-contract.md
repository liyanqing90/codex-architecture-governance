# Architecture solution decision contract

Use `../schemas/architecture-decision.schema.json` after a verified review for
remediation, or after an approved
`../schemas/architecture-design-brief.schema.json` for Greenfield design.

## Decision boundary

A remediation decision solves confirmed findings. A Greenfield decision solves
explicit Design Brief questions and quality scenarios with an empty Finding
list. A decision does not discover findings, accept risk, plan implementation,
or authorize change.

Always include a keep-current/local-correction option. Add structural options
only when current constraints support them. Compare at least three options.
Every option records benefits, liabilities, assumptions, all declared
quality-attribute effects, business/team/evolution fit, complexity tier,
implementation and operational complexity, maturity and lock-in, migration
risk, reversibility, cost, and the complete trade-off scorecard.

Use the task-scoped Markdown entries selected from
`../knowledge/manifest.yaml` as maintained decision evidence:

- quality model for vocabulary and scenarios;
- styles for system organization;
- patterns for bounded mechanisms;
- technology profiles for implementation capabilities and lock-in;
- reference architectures for complete control/data paths;
- migrations for staged evolution;
- domain guidance for specialist requirements;
- decision guides for hard rejection rules.

Knowledge entries do not override project evidence. A technology's capability
does not prove project fit.

## Status and authority

- `proposed`: advisor output awaiting authority;
- `accepted`: authorized decision that may enter remediation;
- `rejected`: considered but not selected for implementation;
- `superseded`: replaced by another recorded decision.

Bind remediation to the verified Review ID and file SHA-256. Bind Greenfield
to the Design Brief path and file SHA-256. Bind every cited
architecture style, pattern, technology profile, reference architecture, and
migration guide to the exact selected entry version and SHA-256. Bind the
selection artifact itself. Remediation includes only confirmed, unresolved
Finding IDs; Greenfield includes none.
Record known facts, assumptions, unknowns, hard eliminations, why every
nonselected option was rejected, compatible migration slices, all decision
makers, and at least one measurable revisit trigger.

Generate the non-inferable bindings with:

```bash
python3 ../scripts/architecture_tool.py decision-bindings \
  --project <repository-root> \
  --review <verified-review.yaml> \
  --knowledge-selection <decision-knowledge-selection.yaml>
```

For Greenfield, replace `--review` with
`--design-brief <architecture-design-brief.yaml>`.

Validate with:

```bash
python3 ../scripts/architecture_tool.py validate-decision \
  <decision.yaml> --review <verified-review.yaml> --project <repository-root>
```

For Greenfield validation, replace `--review` with `--design-brief`.
