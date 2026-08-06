# Remediation planning contract

Use `../schemas/remediation-plan.schema.json`. A Plan is execution guidance,
not architecture selection or implementation authority. Existing Plan artifacts
through 1.2 remain readable. New Greenfield target plans use Plan 1.3 in the
1.0 product release.

## Planning modes and source bindings

### Remediation

Plan only from `verification.status: confirmed` Findings covered by an accepted
Decision. Bind the trusted Review and Decision IDs and SHA-256 values, every
Finding ID and semantic fingerprint, and only Knowledge IDs present in the
Decision selection. Exclude candidate, rejected, needs-evidence, and resolved
Findings. Recheck a Finding when its evidence commit, fingerprint, contract, or
owning boundary materially changed.

### Greenfield target

Plan from an accepted open or constrained Greenfield Decision. Bind the exact
Design Brief and Decision bytes and the selected target architecture. Do not
invent a Review, Finding, or remediation risk: `finding_ids` and
`finding_bindings` remain empty. For every item bind the Brief decision question,
target runtime/deployment unit, data owner, interface, trust boundary, critical
flow, operational concern, and relevant required/preferred/prohibited constraint
assessment.

Stop when the Decision is proposed, stale, rejected, superseded, or lacks the
source bindings required by its mode.

## Planning unit

Group items when they share an owning boundary, target unit, critical flow, or
invariant. Keep them separate when authority, migration, rollback, or ownership
differs. Each item records:

- source Decision and, where applicable, Review and Finding bindings;
- desired invariant or target outcome and accountable owner;
- affected unit, flow, interface, data owner, trust boundary, operation, and
  constraint assessment;
- recommended option and alternatives with real trade-offs;
- do-nothing consequence for remediation or the unbuilt-target consequence for
  Greenfield;
- effort size, uncertainty, assumptions, dependencies, change risk, and
  governed/high-risk flag;
- ordered slices, compatibility and data strategy, deployment strategy,
  observability, rollback/containment, and stop conditions;
- measurable acceptance criteria covering the primary path, owning invariant,
  and an adjacent failure or alternate path; and
- accepted evidence types and, only after completion, repository-relative
  evidence with exact SHA-256, result, observation time, and optional provider
  run binding.

## Sequencing and safety

Prefer evidence and safety nets; compatible seams; reversible internal changes;
justified data or contract migration; consumer rollout; and old-path removal
only after measured acceptance. Order by risk reduction, dependency, and
reversibility rather than severity alone. Identify work that should be reverified
after an earlier slice.

Do not recommend a shared service because code looks similar. Require stable
shared semantics, aligned lifecycle, accountable ownership, and acceptable
coupling. Mark persisted data, public contracts, authorization, production
infrastructure, deployment, and destructive effects as governed/high-risk.
Planning does not authorize execution.

## Effort and acceptance

- `xs`: hours, one local boundary;
- `s`: roughly one to three focused days;
- `m`: several days across a bounded subsystem;
- `l`: multi-week or cross-team work;
- `xl`: program-level, migration, or portfolio coordination.

Effort is a range indicator, not a promise. “Refactor complete”, “clean
architecture”, or a file-size target is not acceptance evidence. Leave
`completion_evidence` empty until evidence exists. Every declared evidence type
must be covered before an item or Plan claims completion.

Validate a remediation plan with:

```bash
python3 ../scripts/architecture_tool.py validate-plan \
  <plan.yaml> --decision <accepted-decision.yaml> --project <repository-root> \
  --review <verified-review.yaml>
```

Validate a Greenfield implementation plan with:

```bash
python3 ../scripts/architecture_tool.py validate-plan \
  <plan.yaml> --decision <accepted-decision.yaml> --project <repository-root> \
  --design-brief <architecture-design-brief.yaml>
```

The validator must reject fake Greenfield Findings, missing Brief/Decision
bindings, stale constraint assessments, and completion claims without hashed
evidence.
