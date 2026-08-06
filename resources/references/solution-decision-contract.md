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

## Emerging upgrades and replacements

An emerging architecture or technology is an assessment hypothesis, not a
recommendation. A decision may consider one only when it is grounded in a valid
Remediation or Greenfield source context and the companion Markdown contains a
complete evolution assessment packet. The packet must include:

- a keep-current/local-correction baseline with current owner, observed
  measures, and do-nothing consequence;
- a measurable capability or quality gap with scenario, current value, target,
  measurement method, evidence, and threshold;
- current official evidence for every volatile claim: version, support or
  lifecycle, compatibility, security, license, pricing, limits, roadmap, or
  benchmark. Record publisher, URL, scope, review/access date, and freshness;
- compatibility and migration cost for consumers, public or persisted
  contracts, data, deployment, mixed-version operation, and exit;
- operational and team fit, including accountable owner, required skills,
  support/on-call, observability, failure semantics, security, and operating
  cost;
- lock-in, portability, rollback point, rollback data semantics, and the
  irreversible gate;
- bounded shadow or pilot evidence with success/stop criteria, observed
  quality/cost/operational measures, and an evidence owner; and
- explicit revisit triggers containing a measurable metric or event, threshold,
  owner, review date or cadence, and reopening evidence.

If a volatile claim lacks current official evidence, or an applicable
shadow/pilot has not run, treat it as an unknown. Do not convert novelty,
popularity, a vendor promise, a benchmark, or an official capability statement
into project fit. The decision may select keep-current and revisit later; a
bounded pilot is evidence collection, not adoption authority. Acceptance is a
separate authorized lifecycle transition and is never implied by the advisor,
the stable router, or a score.

Mark this path with `decision.assessment_kind: technology-evolution`. Bind the
project-relative companion Markdown path and exact SHA-256 in
`evolution_assessment`, together with a `keep-current`, `evidence-only`, or
`adopt` disposition and structured baseline, gap, volatile-claim,
compatibility, operations, lock-in/exit, rollback, pilot, and revisit records.
Bind every measurement, gap record, official-source capture, and observed pilot
measure to a normalized project-relative file path and exact SHA-256. The
validator rejects an upgrade or replacement adoption unless every volatile
claim is current and the completed pilot contains bound observed measures.
Existing standard decisions remain compatible and do not require this binding.

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
