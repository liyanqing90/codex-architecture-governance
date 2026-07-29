---
name: architecture-solution-advisor
description: Compares architecture styles, patterns, technologies, and keep-current options for confirmed findings or an approved Greenfield design brief with explicit quality-attribute scenarios. Use after architecture verification for remediation, or before implementation for a new system, when a project needs a target architecture, technology selection, ADR-like decision, tradeoff analysis, or a reasoned choice between monoliths, services, events, workflows, agent runtimes, mobile data models, or shared portfolio capabilities. Produces an architecture decision, not an implementation plan or code change.
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
   reversibility, cost, maturity, and lock-in.
7. Select one option and explain why every non-selected option loses under
   current evidence.
8. Record measurable revisit triggers. Do not treat a score as proof.

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
