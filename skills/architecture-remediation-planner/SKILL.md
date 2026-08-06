---
name: architecture-remediation-planner
description: Converts an accepted architecture decision into an executable, dependency-aware migration roadmap for confirmed remediation findings or an accepted open/constrained Greenfield target. Use for implementation slices, compatibility, data migration, deployment sequencing, observability, rollback, stop conditions, effort, and acceptance criteria. Produces a plan only; it does not choose architecture or implement changes.
---

# Plan an architecture change

Turn an accepted target into a safe, observable, dependency-aware roadmap
without editing code or reopening the decision.

## Load and classify the source chain

Read `../../resources/references/review-contract.md` and
`../../resources/references/remediation-contract.md` completely. Load one
accepted Architecture Decision and validate its source chain.

Choose exactly one planning mode:

- **Remediation:** bind the accepted Decision to a verified Review. Include only
  confirmed unresolved Findings, their exact fingerprints, and their Knowledge
  IDs. Exclude candidate, rejected, needs-evidence, and resolved Findings.
- **Greenfield:** bind the accepted Decision to its approved Design Brief and
  target architecture. Use Plan 1.3. Do not invent a Review or Finding to make
  the legacy remediation shape fit: omit `finding_ids` and `finding_bindings`.
  Bind the Brief and Decision bytes. Across the Plan, cover every target runtime
  and deployment unit, data-ownership record, interface, trust boundary,
  technology ID, critical flow, and constraint. Keep operational controls
  explicit in deployment, observability, rollback, stop, and acceptance fields.

Recheck a remediation Finding if its fingerprint, evidence commit, contract, or
owning boundary changed. Stop when the Decision is proposed, stale, rejected,
superseded, or no longer satisfies the selected source mode.

## Plan the work

1. Group remediation Findings by violated invariant and owning boundary. For
   Greenfield, group work by target unit, critical flow, dependency, or
   surviving required constraint. Do not create fake findings.
2. Build a dependency graph covering prerequisites, external dependencies,
   sequencing conflicts, authority decisions, and work that will collapse after
   an earlier slice.
3. Preserve the accepted option and all surviving constraint assessments. Do
   not reopen technology, architecture, or preference scoring.
4. For each item, record the source binding, owner, desired invariant or target
   outcome, affected unit/flow/constraint, recommended option, alternatives,
   do-nothing consequence where applicable, effort and uncertainty, change risk,
   governed flag, dependencies, ordered slices, protection, observability,
   rollback, stop conditions, and measurable acceptance criteria.
5. Sequence by risk reduction, dependency, and reversibility: evidence and
   safety net; compatibility seam; reversible internal change; data or contract
   migration; consumer rollout; old-path removal after measured acceptance.

For every Greenfield item, name the Brief question and Decision target it
implements. Map each slice to at least one runtime unit and one critical flow or
explicit constraint assessment. The union of item bindings must cover the full
accepted target. Keep data ownership, interface compatibility, trust-boundary
controls, and operations visible in the acceptance criteria.

Do not prescribe a shared service because two projects look similar. Require
stable shared semantics, aligned lifecycle, explicit ownership, and acceptable
coupling. Mark persisted data, public contracts, authorization, production
infrastructure, deployment, and destructive effects as governed/high-risk.

## Output and validation

Write:

- `.architecture/reviews/<timestamp>-remediation.yaml`;
- `.architecture/reviews/<timestamp>-remediation-plan.md`.

Use `.architecture-portfolio/reviews/` for portfolio work. Use Plan schema 1.2
for readable remediation plans and Plan schema 1.3 for new Greenfield plans.
The machine-readable plan must bind the accepted Decision, and then either the
verified Review plus every Finding fingerprint or the Design Brief plus the
target architecture. Use only Knowledge IDs present in the Decision selection.

Validate the remediation chain:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-plan \
  <plan.yaml> --decision <accepted-decision.yaml> --project <repo> \
  --review <verified-review.yaml>
```

Validate the Greenfield chain:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-plan \
  <plan.yaml> --decision <accepted-decision.yaml> --project <repo> \
  --design-brief <architecture-design-brief.yaml>
```

Leave `completion_evidence` empty until evidence exists. A completed item must
bind repository-relative evidence files and exact SHA-256 values for every
declared evidence type. End with the smallest safe first slice and its
acceptance evidence; do not execute it unless the user separately requests
implementation.
