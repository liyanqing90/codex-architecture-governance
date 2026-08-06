# Add constrained target architecture to the existing solution workflow

- Status: accepted
- Date: 2026-08-06
- Decision owners: Hengmu maintainers
- Scope: public routing, Solution Advisor and remediation-planner workflows,
  Brief/Decision/Plan contracts, documentation, and evaluation corpus
- Release: 1.0.0

## Context

Hengmu can already compare open Greenfield and remediation options, but a user
with real delivery, security, data, or platform limits has no typed way to ask
for a compliant target. Treating every limit as an unqualified “constraint” also
risks turning an owner assertion into proof, preserving a preferred option when
it should lose, or leaving a prohibited option in consideration. A new public
Skill would fragment the eight-name compatibility surface and duplicate the
Solution Advisor's authority boundary.

## Decision

Extend `architecture-solution-advisor` to support open and constrained design.
Route `design`, `specify`, `constrain`, and Chinese equivalents through the
existing `hengmu` router to that Skill. Add no public Skill.

Constrained Brief 1.1 inputs classify constraints as required, preferred, or
prohibited. The Advisor challenges required constraints for authority, conflict,
and feasibility; only surviving required constraints are hard requirements.
Preferred constraints may lose with a recorded trade-off. Prohibited options are
hard-eliminated. Inputs are never proof of feasibility, compliance, or project
fit.

Current Decision 1.4 binds a Brief 1.1 target architecture containing runtime
and deployment units, data ownership, interfaces, trust boundaries, critical
flows, operations, constraint assessments, and Knowledge. Open mode has no
declared constraints; constrained mode assesses every declared constraint.
Accepted Greenfield targets enter Plan 1.3, which binds the Brief and Decision
directly, keeps Finding lists empty, and maps work to target units, flows, and
constraints.

Keep technology-evolution as an explicit evidence lens only for upgrade,
replacement, or emerging-technology questions. Do not pin versions from model
memory.

## Alternatives considered

1. **Add a ninth constrained-design Skill.** Rejected: duplicates decision
   authority, breaks the focused-name boundary, and creates routing ambiguity.
2. **Treat all constraints as proof or hard requirements.** Rejected: hides
   conflicts, makes preferences unnecessarily binding, and confuses intent with
   evidence.
3. **Route constrained design to technology-evolution.** Rejected: most
   constrained designs are not technology upgrades and should not inherit
   volatile-claim or pilot requirements.
4. **Keep the current open-only workflow.** Rejected: cannot express or audit
   compliant variants for real hard constraints.

## Consequences

Positive:

- one stable public route supports design/specification/constraint intent;
- decisions expose the operational architecture needed for implementation;
- constraint conflict and preference loss become reviewable rather than implicit;
- Greenfield planning is source-bound without fake remediation Findings; and
- old artifacts and focused Skill names remain readable and invocable.

Costs and risks:

- Brief, Decision, and Plan validators must enforce the new versions and
  source-chain rules;
- maintainers must obtain authoritative constraint sources and current volatile
  evidence; and
- a complete target artifact can still describe a poor architecture, so
  acceptance remains an accountable human transition.

## Verification and rollout

The 1.0 release adds direct, indirect, incomplete, negative, and edge routing
cases; decision-quality cases for constraint semantics and target completeness;
artifact tamper cases for Brief/Decision/Plan source bindings; and Knowledge
selection cases that prevent technology-evolution misuse and version inference.
Repository validation, schema/Skill validation, tests, lint, formatting,
packaging, checksum, and SBOM checks remain release evidence.

Roll out the three new artifact versions together. Preserve legacy chains as
readable history. Roll back by retaining the previous accepted chain and
rejecting or superseding a new constrained proposal; never rewrite a legacy
artifact to simulate migration.

## Revisit triggers

Revisit this decision if a future release needs a distinct design authority,
constraint strengths become persisted beyond Brief/Decision, the eight focused
Skill boundary changes, or the target architecture fields no longer cover a
critical runtime or trust flow.
