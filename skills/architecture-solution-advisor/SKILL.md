---
name: architecture-solution-advisor
description: Compares architecture styles, patterns, technologies, and keep-current options for confirmed findings and explicit quality-attribute scenarios. Use after architecture verification when a project needs a target architecture, technology selection, ADR-like decision, tradeoff analysis, or a reasoned choice between monoliths, services, events, workflows, agent runtimes, mobile data models, or shared portfolio capabilities. Produces an architecture decision, not an implementation plan or code change.
---

# Advise an architecture solution

Select the least complex option that satisfies current evidence, quality
attributes, team capability, cost, and migration constraints.

## Load the decision inputs

Read completely:

- `../../resources/references/review-contract.md`;
- `../../resources/references/solution-decision-contract.md`;
- the verified review;
- the project Profile, constraints, and critical flows;
- `../../resources/knowledge/quality-models/core.yaml`;
- `../../resources/knowledge/decision-guides/system-style-selection.yaml`;
- only other catalog files relevant to the decision.

Use `quality-models/core.yaml` to normalize quality attributes and
`decision-guides/system-style-selection.yaml` for mandatory rejection rules.
Load architecture styles, patterns, technology profiles, reference
architectures, migrations, or domain guidance only when the decision needs
them.

Stop when no confirmed unresolved finding, quality scenario, or decision
authority exists. Do not invent scale, team, budget, compliance, or migration
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
decision to the verified review ID and SHA-256 and bind cited knowledge to the
current catalog hashes:

```bash
python3 ../../resources/scripts/architecture_tool.py decision-bindings \
  --project <repo> --review <verified-review.yaml>
```

Use only confirmed, non-resolved Finding IDs. Include at least three options,
the full declared-quality effects and trade-off scorecard, hard eliminations,
and explicit rejection reasons for every nonselected option.

Validate:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-decision \
  <decision.yaml> --review <verified-review.yaml> --project <repo>
```

Leave `decision.status: proposed` until an authorized decision maker accepts
it. Do not implement or create a remediation plan in this workflow.
