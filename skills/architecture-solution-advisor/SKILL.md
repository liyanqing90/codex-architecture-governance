---
name: architecture-solution-advisor
description: Compares architecture styles, patterns, technologies, and keep-current options for confirmed findings or an approved Greenfield design brief with explicit quality-attribute scenarios. Use after architecture verification for remediation, or before implementation for a new system, when a project needs a target architecture, technology selection, ADR-like decision, tradeoff analysis, or a reasoned choice between monoliths, services, events, workflows, agent runtimes, mobile data models, or shared portfolio capabilities. Produces an architecture decision, not an implementation plan or code change.
---

# Advise an architecture solution

Select the least complex option that satisfies current evidence, quality
attributes, team capability, cost, and migration constraints.

## Load the decision inputs

Read completely:

- `../../resources/references/review-contract.md`;
- `../../resources/references/solution-decision-contract.md`;
- the project Profile, constraints, and critical flows;
- `../../resources/knowledge/manifest.yaml`;
- only Markdown entries selected for this decision.

Choose exactly one source mode:

- **Remediation:** read the verified review and the repository-facts and
  knowledge-selection artifacts bound to that Review.
- **Greenfield:** read a validated
  `../../resources/schemas/architecture-design-brief.schema.json` artifact.
  The brief, not an empty or manufactured review, supplies objectives, facts,
  assumptions, unknowns, boundaries, critical flows, and quality scenarios.

Validate a Greenfield brief before using it:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-design-brief \
  <repo>/.architecture/architecture-design-brief.yaml
```

Create a decision-specific selection rather than reusing unrelated audit
context:

```bash
python3 ../../resources/scripts/architecture_tool.py select-knowledge \
  --facts <repository-facts.yaml> \
  --profile <profile.yaml> \
  --task "<decision problem>" \
  --skill architecture-solution-advisor \
  --output <repo>/.architecture/decision-knowledge-selection.yaml
```

Read every selected Markdown entry completely. The selection must include each
style, pattern, technology, reference architecture, and migration cited by an
option.

Stop when remediation has no confirmed unresolved finding, or Greenfield work
has no approved design brief, measurable quality scenario, or decision
authority. Do not invent scale, team, budget, compliance, or migration
requirements.

## Decision workflow

1. Restate the problem as quality-attribute scenarios:
   source → stimulus → environment → owning component → response → measurable
   outcome.
2. Map the current architecture from runtime units, data owners, integration,
   deployment, and team responsibility rather than directory names.
3. Record constraints and assumptions that would change the decision.
4. Generate at least:
   - keep the current architecture with a local correction;
   - the lowest-complexity structural improvement;
   - one materially viable alternative when evidence supports it.
5. Apply hard rejection rules. Reject:
   - broad microservices without independent deployment and team autonomy;
   - durable workflow when a queue and database state are sufficient;
   - event sourcing for ordinary CRUD without temporal or audit value;
   - offline-first when server authority plus cache meets the requirement;
   - multi-agent orchestration when a fixed workflow or one agent suffices.
6. Compare each surviving option by:
   business fit, quality-attribute effects, team capability, implementation
   complexity, operational complexity, migration risk, reversibility, cost,
   maturity, and lock-in.
7. Select one option. Explain why it wins and why every non-selected option
   loses under current evidence.
8. Record measurable revisit triggers. Do not present a score as proof.

Treat framework documentation as capability evidence, not proof that a
framework fits the project. Verify time-sensitive claims against current
official sources and record the review date.

## Output

Write:

- `.architecture/reviews/<timestamp>-architecture-decision.yaml`;
- `.architecture/reviews/<timestamp>-architecture-decision.md`.

For a portfolio, use `.architecture-portfolio/reviews/`.

Start from `../../resources/templates/architecture-decision.yaml`. Bind the
decision to either the verified review or the Greenfield design brief, and bind
cited knowledge to exact Markdown entry hashes.

For remediation:

```bash
python3 ../../resources/scripts/architecture_tool.py decision-bindings \
  --project <repo> \
  --review <verified-review.yaml> \
  --knowledge-selection <decision-knowledge-selection.yaml>
```

For Greenfield:

```bash
python3 ../../resources/scripts/architecture_tool.py decision-bindings \
  --project <repo> \
  --design-brief <architecture-design-brief.yaml> \
  --knowledge-selection <decision-knowledge-selection.yaml>
```

Use schema 1.2 with only confirmed, non-resolved Finding IDs for remediation.
Use schema 1.3 with `decision_kind: greenfield`, the design-brief path and
SHA-256, and an empty `problem.finding_ids` list for Greenfield. Include at
least three options,
the full declared-quality effects and trade-off scorecard, hard eliminations,
explicit rejection reasons for every nonselected option, known facts,
assumptions, unknowns, compatible implementation or migration slices, rollback,
and validation.

Validate:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-decision \
  <decision.yaml> --review <verified-review.yaml> --project <repo>
```

For Greenfield, replace `--review` with
`--design-brief <architecture-design-brief.yaml>`.

Leave `decision.status: proposed` until an authorized decision maker accepts
it. Do not implement or create a remediation plan in this workflow.
