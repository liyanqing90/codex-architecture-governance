---
name: architecture-solution-advisor
description: Compares architecture styles, patterns, technologies, keep-current options, and emerging upgrades or replacements for confirmed findings or an approved Greenfield design brief with explicit quality-attribute scenarios. Use after architecture verification for remediation, or before implementation for a new system, when a project needs a target architecture, technology-evolution assessment, technology selection, ADR-like decision, tradeoff analysis, or a reasoned choice between monoliths, services, events, workflows, agent runtimes, mobile data models, or shared portfolio capabilities. Emerging candidates require current official evidence, a measurable gap, compatibility and migration analysis, and bounded shadow or pilot evidence; popularity or novelty is not a recommendation. Produces an architecture decision, not an implementation plan or code change.
---

# Advise an architecture solution

Select the least-complex option that satisfies current evidence, quality
attributes, team capability, cost, and migration constraints.

## Establish a valid decision context

Read `../../resources/references/review-contract.md`,
`../../resources/references/solution-decision-contract.md`, the project
Profile, constraints, critical flows, and this Skill's
`references/decision-artifact-workflow.md` before creating artifacts.

Choose exactly one source mode:

- **Remediation:** use a verified Review and its bound repository facts and
  knowledge selection.
- **Greenfield:** use an approved, validated Design Brief. Do not manufacture
  an empty Review.

Create a decision-specific knowledge selection. Read the selected Markdown
entries completely. Default discretionary Advisor context to Golden Knowledge.
Allow standard Knowledge only for a required contract dependency, an explicit
caller include, maintainer mode, or an exact detected technology/profile
domain without a declared Golden replacement. A shared broad domain or task
trigger is never a replacement match.

Stop when remediation has no confirmed unresolved Finding, or Greenfield work
has no approved brief, measurable quality scenario, or decision authority. Do
not invent scale, team, budget, compliance, or migration requirements.

## Assess technology evolution without trend recommendations

Treat an emerging architecture or technology candidate as a hypothesis to
assess, never as a reason to change. This is an assessment lens within the
Remediation or Greenfield source modes above, not a third source mode or a
market-scanning workflow. Stop when there is no valid source context. A request
that supplies only a trend, vendor announcement, popularity signal, or vague
upgrade wish must first establish repository evidence or an approved brief.

Before comparing a candidate, record all of the following in the companion
Markdown decision record described by `references/decision-artifact-workflow.md`:

1. The keep-current/local-correction baseline, including the current owner,
   operating model, and consequence of doing nothing.
2. A measurable capability or quality gap: scenario, current observation,
   target, measurement method, evidence location, and decision threshold. A
   hypothetical future scale or benefit is an unknown, not a gap.
3. A volatile-claims register. For every version, support/lifecycle,
   compatibility, security, license, pricing, service-limit, roadmap, or
   benchmark claim, cite a current official source, publisher, URL, scope,
   review date, and freshness decision. If a current official source is
   unavailable or stale, record the claim as unknown and do not use it to
   select the candidate.
4. Compatibility and migration cost across public and persisted contracts,
   consumers, data, deployment, mixed versions, and the cost of exit.
5. Operational and team fit: accountable owner, on-call or support burden,
   required skills, observability, failure handling, security, and total
   operating cost. Documentation of capability does not prove fit.
6. Lock-in and reversibility: proprietary APIs or data formats, portability,
   exit path, rollback point, rollback data semantics, and irreversible gate.
7. Shadow or pilot evidence with a bounded cohort, success and stop criteria,
   observed quality/cost/operational measures, and evidence owner. If a safe
   shadow or pilot is applicable but has not run, select keep-current or a
   bounded evidence-only option; do not select adoption.
8. Explicit revisit triggers with a metric or event, threshold, owner, review
   date or cadence, and evidence that will reopen the comparison.

The assessment must include keep-current, the smallest compatible correction,
and a materially viable upgrade or replacement when evidence supports one.
Select a replacement only when the measured gap remains after the current
baseline is tested and the candidate's compatibility, fit, rollback, and
shadow/pilot evidence are sufficient. A valid outcome is keep-current and
revisit later; do not manufacture a recommendation to fill an emerging-tech
request. Acceptance of a proposed decision remains a separate authority act.

## Compare viable options

1. Restate the problem as quality-attribute scenarios: source, stimulus,
   environment, owning component, response, and measurable outcome.
2. Map runtime units, data owners, integration, deployment, and team
   responsibility from evidence, not directory names.
3. Record constraints and assumptions that would change the decision.
4. Generate a keep-current/local-correction option, the smallest viable
   structural improvement, and one materially viable alternative when evidence
   supports it.
5. Reject broad microservices without independent deployment and team
   autonomy; durable workflow when queue plus database state is enough; event
   sourcing for ordinary CRUD without temporal value; offline-first when server
   authority plus cache fits; and multi-agent orchestration when a fixed
   workflow or one agent suffices.
6. Compare every surviving option by business fit, quality effects, team
   capability, implementation and operational complexity, migration risk,
   reversibility, cost, maturity, and lock-in. For an emerging candidate,
   include measured gap, official-evidence freshness, shadow/pilot result,
   and exit cost in the comparison.
7. Select one option and explain why every non-selected option loses under
   current evidence.
8. Record measurable revisit triggers. Do not treat a score, benchmark, vendor
   claim, or current official capability statement as proof of project fit.

Treat framework documentation as capability evidence, not fit proof. Verify
volatile claims against current official sources and record the review date.

## Produce a decision, not a plan

Write the bound Architecture Decision YAML and companion Markdown in the
configured review directory. Keep the decision proposed until an authorized
decision maker accepts it. Include at least three options, hard eliminations,
rejection reasons, known facts, assumptions, unknowns, compatible migration or
implementation slices, rollback, validation, and stop conditions.

Use the command and schema procedures in
`references/decision-artifact-workflow.md` to select Knowledge, obtain
bindings, choose the correct decision schema, and validate the result. Do not
implement code or create a remediation plan in this workflow.
