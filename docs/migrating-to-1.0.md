# Migrating to 1.0

Hengmu 1.0.0 is the first stable product release. It adds constrained Greenfield
design while preserving the router, all eight focused Skill names, and readable
artifact contracts through Decision 1.3 and Plan 1.2.

## What changes

| Area | Before | 1.0 |
| --- | --- | --- |
| Routing | Solution comparison and Greenfield design route to the Advisor | `design`, `specify`, `constrain`, and Chinese equivalents route to the same Advisor; no new Skill |
| Brief | Open Greenfield Brief 1.0 | Brief 1.0 remains readable; Brief 1.1 explicitly supports open or constrained mode, with typed inputs in constrained mode |
| Decision | Remediation through 1.2; legacy open Greenfield 1.3 | Decision 1.4 is the current Brief 1.1 target contract for open and constrained modes |
| Plan | Remediation Plan 1.2 | Plan 1.3 adds accepted Greenfield targets with no Findings |
| Release | 0.4 artifact set | Brief 1.1, Decision 1.4, and Plan 1.3 ship together as 1.0.0 |

## Constraint semantics

When creating Brief 1.1, classify each constraint as `required`, `preferred`, or
`prohibited`, and record its kind, target, scope, accountable authority,
rationale, and review trigger. The classification is an input, not proof.

The Advisor challenges required constraints for conflict and feasibility, keeps
only surviving hard requirements, permits preferred constraints to lose with a
trade-off, and hard-eliminates prohibited options. If no compliant variant
survives, stop and resolve the conflict. Do not convert a constraint into a fact,
Finding, or acceptance evidence.

## Migration paths

### Existing open Greenfield work

1. Continue reading Brief 1.0 and Decision 1.3 without conversion.
2. If constraints are now material, create a new Brief 1.1 rather than editing
   the old Brief.
3. Re-run Knowledge selection and bind the new Brief bytes.
4. Produce a proposed Decision 1.4 with the complete target architecture and
   one assessment for every constraint.
5. Obtain the normal authorized acceptance. Do not let the router or Advisor
   accept it.
6. Create Plan 1.3 only after acceptance; bind Brief and Decision directly and
   omit remediation-only Finding fields.

### Existing remediation work

Keep the verified Review, Finding fingerprints, accepted Decision through 1.2,
and Plan 1.2 chain. Do not rewrite it as Greenfield and do not add fake
Findings. If the accepted target needs constraints, create a new constrained
Brief/Decision only when the work is actually a new Greenfield design question;
otherwise record the constraint in the remediation decision context and retain
the Review source.

## Compatibility, rollback, and checks

Mixed readers may consume the old readable contracts. A 1.0 reader must reject
or clearly report missing 1.1/1.4/1.3 source bindings; it must not silently
downgrade a constrained artifact to open design. Roll back by retaining the old
accepted chain and rejecting or superseding the new proposal. No legacy artifact
needs to be deleted or rewritten.

Validate the new chain with the repository commands:

```bash
python3 resources/scripts/architecture_tool.py validate-design-brief \
  .architecture/architecture-design-brief.yaml --project .
python3 resources/scripts/architecture_tool.py validate-decision \
  .architecture/reviews/<decision.yaml> --project . \
  --design-brief .architecture/architecture-design-brief.yaml
python3 resources/scripts/architecture_tool.py validate-plan \
  .architecture/reviews/<plan.yaml> --project . \
  --decision .architecture/reviews/<accepted-decision.yaml> \
  --design-brief .architecture/architecture-design-brief.yaml
python3 resources/scripts/architecture_tool.py gate --project . \
  --decision .architecture/reviews/<accepted-decision.yaml> --stage change
```

Pass only the applicable source arguments. Confirm exact hashes, complete target
architecture sections, constraint assessments, empty Greenfield Finding lists,
and repository-relative completion evidence before claiming completion.
