# Architecture solution decision contract

Use `../schemas/architecture-decision.schema.json` after a verified Review for
remediation, or after an approved Design Brief for Greenfield work. Existing
Decision artifacts through 1.3 remain readable. New Brief 1.1 Greenfield
targets use schema 1.4 in either explicit open or constrained mode and are part
of the 1.0 product release.

## Decision boundary and source modes

A remediation Decision solves confirmed unresolved Findings. A legacy open
Greenfield Decision solves Brief 1.0. A current Greenfield Decision solves Brief
1.1 in explicit open or constrained mode; constrained mode assesses every
required, preferred, and prohibited constraint. Greenfield
`problem.finding_ids` is always empty. A
Decision does not discover Findings, verify evidence, accept risk, plan work, or
authorize implementation.

Always compare keep-current/local correction, the smallest compatible structural
improvement, and a materially viable alternative when evidence supports one.
Every option records benefits, liabilities, assumptions, quality effects,
business/team/evolution fit, implementation and operational complexity,
maturity, lock-in, migration risk, reversibility, cost, and trade-off scores.

## Constraint semantics

Constraints are inputs to reasoning, not proof of feasibility, quality, or
compliance. Bind each one by ID, kind, disposition, target, scope, accountable
authority, rationale, review trigger, required Knowledge ID for architecture
style/pattern/technology constraints, and exact Brief bytes.

- Challenge required constraints for authority, ambiguity, conflict,
  feasibility, and hidden consequences. Only surviving required constraints are
  hard requirements, and every selected variant must satisfy all of them.
- Treat preferred constraints as weighted preferences. A preferred constraint
  may lose to a measured quality, compatibility, safety, cost, or operational
  trade-off; record the loss.
- Hard-eliminate prohibited options. Preserve the prohibition and reason outside
  the scorecard; do not allow a prohibited option to win on other scores.

Record fact, inference, assumption, unknown, and constraint assessment
separately. A detected dependency, Knowledge entry, owner assertion, or word
such as “must” never becomes evidence merely by appearing in the input. If
required constraints conflict and no compliant variant survives, stop with the
conflict rather than weakening a requirement.

## Required target architecture

Every 1.4 Decision must include a target architecture bound to the
selected option and Knowledge snapshot. It must describe:

- runtime units, responsibilities, and unit-level ownership;
- deployment units, environments, rollout, mixed-version behavior, and
  operational ownership;
- authoritative data owners, stores, lifecycle, consistency, and recovery;
- interfaces, consumers, schemas/contracts, compatibility, and evolution;
- trust boundaries, covered runtime units, identities, permissions, secrets,
  and untrusted inputs;
- critical flows, triggers, steps, failure outcomes, recovery, and measures;
- operations, observability, capacity, backup/restore, on-call, and incident
  controls;
- an assessment for every required, preferred, and prohibited constraint; and
- the exact Knowledge IDs, versions, and SHA-256 values used by the decision.

Every assessment repeats the Brief Knowledge ID exactly. A satisfied selected
constraint binds concrete `target_refs`; a technology constraint points only to
runtime units whose `technologies` contain that ID. A prohibited constraint can
be satisfied only when its Knowledge ID is absent from both the selected option
and target runtime.

Legacy open 1.3 Decisions remain readable and may lack a structured target. Do
not retrofit constraints by mutating them. Start current open or constrained
target work with Brief 1.1 and Decision 1.4; the absence of constraints in open
mode does not excuse missing data ownership, interfaces, trust boundaries,
critical flows, or operations.

## Knowledge and evidence

Use task-scoped Markdown entries selected from `../knowledge/manifest.yaml`:
quality models for scenarios; styles for organization; patterns for mechanisms;
technology profiles for capabilities and lock-in; reference architectures for
complete paths; migrations for staged change; domains for specialist needs; and
decision guides for rejection rules. Bind selected IDs, versions, and hashes.
Knowledge is guidance. It never overrides repository evidence or proves project
fit.

## Technology evolution

Use `decision.assessment_kind: technology-evolution` only for an explicit
emerging technology, upgrade, or replacement question inside a valid
Remediation or Greenfield source mode. Require a companion packet with:

- keep-current baseline, owner, observed measures, and do-nothing consequence;
- measurable gap, current value, target, method, evidence, and threshold;
- current official source for every volatile version, lifecycle,
  compatibility, security, license, pricing, limit, roadmap, or benchmark claim;
- consumer, public/persisted contract, data, deployment, mixed-version, and exit
  migration cost;
- accountable operator, skills, support, observability, failure, security, and
  operating cost;
- portability, lock-in, rollback point, data recovery, and irreversible gate;
- bounded pilot/shadow evidence or an explicit keep-current/evidence-only
  disposition; and
- measurable, owned revisit triggers with date/cadence and reopening evidence.

Missing or stale official evidence and an unrun applicable pilot are unknowns;
they cannot support adoption. Never pin a version from model memory. A current
official capability statement, benchmark, popularity signal, or vendor promise
does not establish project fit.

## Authority, migration, and validation

Use `proposed`, `accepted`, `rejected`, and `superseded` as authority states.
An approved Brief 1.1 also binds policy-authorized approver identities,
approval time/authority, repository-relative SHA-256 evidence, and one detached
SSH signature per approver; template authors and status text do not grant
authority.
Only an authorized decision maker may move a Decision to `accepted`. Bind
remediation Decisions to the verified Review ID and SHA-256. Bind Greenfield
Decisions to the Design Brief path and SHA-256. Bind the Knowledge selection and
all cited entries.

Include compatible migration slices, rollback, validation, hard eliminations,
revisit triggers, decision makers, known facts, assumptions, unknowns, and the
reason every non-selected option loses. Validate the complete chain with the
architecture tool; status strings alone are never proof.
