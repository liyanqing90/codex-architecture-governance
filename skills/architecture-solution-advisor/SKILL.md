---
name: architecture-solution-advisor
description: Compare, design, specify, or constrain an architecture for a verified remediation Review or an approved Design Brief. Use for open or constrained target architecture, technology and pattern selection, ADR-like decisions, trade-off analysis, and bounded technology-evolution assessment. Required, preferred, and prohibited constraints are challenged inputs; they are not proof. Produce a decision and target architecture, never an implementation plan or code change.
---

# Advise an architecture solution

Produce the least-complex target that satisfies the evidence, quality scenarios,
accountable constraints, and operating reality. Keep the decision proposed until
an authorized decision maker accepts it.

## Establish the source and design mode

Read `../../resources/references/review-contract.md`,
`../../resources/references/solution-decision-contract.md`, the project Profile,
constraints, critical flows, and
`references/decision-artifact-workflow.md` completely before creating artifacts.

Choose exactly one source mode:

- **Remediation:** bind a verified Review and its repository facts, critical-flow
  coverage, and Knowledge selection. Include only confirmed unresolved Findings.
- **Legacy open Greenfield:** continue to read an approved Design Brief 1.0 and
  its Decision 1.3 chain. Do not manufacture a Review or Finding list.
- **Current Greenfield target:** bind an approved Design Brief 1.1. Honor its
  explicit `open` or `constrained` design mode; constrained mode binds every
  declared constraint record. Treat the Brief as the design question, not as
  independent proof.

Stop when remediation has no confirmed unresolved Finding, Greenfield has no
approved brief or measurable scenario, or the decision owner is missing. Do not
invent scale, budget, team capability, compliance, migration requirements, or
observations.

Use the open mode when the brief asks what architecture should satisfy its
scenarios without typed constraints. Use the constrained mode when it declares
required, preferred, or prohibited constraints and asks for a compliant target.
A constrained request is still advisor work; do not route it to a new Skill.

## Normalize and challenge constraints

Record each constraint with its kind, disposition, target, scope, accountable
authority, rationale, and review trigger:

- **required:** challenge conflicts, ambiguity, infeasibility, and hidden
  consequences. Keep a required constraint only when the authority and evidence
  survive that challenge. Produce variants that comply with every surviving hard
  requirement; if none exists, stop with the conflict instead of weakening it.
- **preferred:** compare it as a weighted preference. It may lose to a quality,
  safety, cost, or compatibility trade-off; record why.
- **prohibited:** hard-eliminate an option that violates the prohibition and
  record the exact reason. Do not score it as a merely weak alternative.

Inputs, owner assertions, and Knowledge guidance do not prove that a constraint
is feasible or that a selected architecture works. Distinguish fact, inference,
assumption, unknown, and constraint assessment in the artifact. Never turn a
technology name, detected dependency, preference, or “must” in prose into an
observed fact.

## Select Knowledge and compare options

Create a decision-specific Knowledge selection and read every selected Markdown
entry completely after its compact context validates. Bind selected IDs,
versions, and SHA-256 values. Default discretionary context to Golden Knowledge;
use Standard entries only for required contract dependencies, explicit includes,
maintainer mode, or an exact detected domain without a declared Golden
replacement.

Restate quality-attribute scenarios with source, stimulus, environment, owning
unit, response, and measure. Map current and proposed runtime units, deployment
units, data owners, interfaces, trust boundaries, critical flows, and operations
from evidence and the Brief. Compare at least:

1. keep-current or the smallest local correction;
2. the smallest compatible structural improvement; and
3. a materially viable alternative when current evidence supports one.

Compare business fit, quality effects, team fit, runtime and deployment burden,
data and interface compatibility, migration and rollback, operations, cost,
maturity, reversibility, and lock-in. Reject broad microservices, durable
workflow, event sourcing, offline-first, or multi-agent designs when their
independent invariant is not evidenced. Explain why every non-selected option
loses, including hard eliminations.

## Technology evolution is a narrow lens, not trend recommendations

Use `technology-evolution` only when the user explicitly asks about an emerging
technology, upgrade, or replacement and a valid Remediation or Greenfield source
context exists. Require the companion assessment's measured gap, current
official evidence for volatile claims, compatibility, migration, operational and
team fit, lock-in, rollback, bounded shadow or pilot evidence, or an explicit
keep-current disposition, and measurable
revisit triggers. A newer release, popularity, vendor claim, benchmark, or
Knowledge capability statement is not project fit. Do not put version pins in an
artifact from memory; record a version only when it is bound to current official
evidence or repository evidence.

## Produce the decision and target architecture

Write the bound Architecture Decision YAML and companion Markdown under the
configured review directory. Preserve Decision 1.3 for existing Brief 1.0
chains. Use Decision 1.4 for new Brief 1.1 targets in either open or constrained
mode. Validate the exact source, selection, and evidence hashes.

Every 1.4 Decision must include a target architecture with:

- runtime units with responsibilities, accountable owners, deployment-unit
  references, and Knowledge-bound technology IDs;
- deployment units with environment, owner, rollout, mixed-version, and on-call
  behavior;
- data ownership with stable ID, owning runtime unit, store, lifecycle,
  consistency, and recovery;
- interfaces and external systems with stable endpoints, contracts,
  compatibility, evolution, and trust-boundary references;
- structured trust boundaries covering identities, permissions, secrets,
  untrusted inputs, and controls;
- an exact binding from every Brief critical flow to runtime units, including
  failure outcome, recovery, and measure;
- operational deployment, observability, recovery, capacity, backup/restore,
  on-call, and incident controls;
- one assessment for every required, preferred, and prohibited constraint; and
- the exact Knowledge selection and hashes used to reason about the target.

Keep `problem.finding_ids` empty for all Greenfield decisions. Do not implement
the target or create a remediation plan in this workflow. Use the remediation
planner only after the decision is accepted.

Use the commands and binding procedures in
`references/decision-artifact-workflow.md` to validate the result.
