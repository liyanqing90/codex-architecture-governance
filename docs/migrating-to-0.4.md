# Migrating to 0.4

Version 0.4 strengthens knowledge curation, adds a Greenfield decision path,
extends behavior scoring, and makes verification floors proportional to risk.
Existing public Skill names and schema `1.1`/`1.2` remediation artifacts remain
supported.

## Knowledge

Existing standard entries remain valid. Generated entries now default to
`status: draft`; an active entry cannot declare
`curation.method: generated`.

Golden entries add:

- `maturity: golden`;
- a non-generated `curation` record;
- kind-specific mechanism sections;
- named decision options with fit, avoid, cost, and failure fields;
- claim IDs mapped to the exact sources that support them.

Selection schema `1.1` adds `priority` to each selected item. The selector
continues to validate schema `1.0`, but new selections use canonical Profile
domain IDs and emit `required`, `recommended`, or `optional`.

## Greenfield decisions

Do not create an empty Review for a new system. Create and validate a Design
Brief:

```bash
cp resources/templates/architecture-design-brief.yaml \
  .architecture/architecture-design-brief.yaml
python3 resources/scripts/architecture_tool.py validate-design-brief \
  .architecture/architecture-design-brief.yaml
```

Generate bindings with `decision-bindings --design-brief ...`. Use
Architecture Decision schema `1.3`, `decision_kind: greenfield`, an empty
`problem.finding_ids`, and the emitted `source_context` fields. Existing
remediation workflows can stay on schema `1.2`.

## Verification policy

`block.minimum_verification_level` remains the compatibility floor. Add
`block.verification_levels` to select higher floors by severity and stage:

```yaml
verification_levels:
  by_severity:
    critical: V3
    high: V2
    medium: V1
    low: V1
    info: V0
  accepted_risk: V4
  release: V4
```

The gate applies the highest applicable floor. Projects may choose stricter
levels but should not lower them merely to make an existing artifact pass.

## Benchmarks

Benchmark schema `1.2` adds structured Solution Advisor decisions. Update agent
commands to emit `observed_decision` for cases with `expected_decision`. The
bundled `codex_benchmark_adapter.py` provides a read-only structured Codex
surface. Empty and legacy run files remain useful schema fixtures but are not
model-quality evidence.
