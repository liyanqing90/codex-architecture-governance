---
name: architecture-remediation-planner
description: Plans remediation for confirmed architecture findings. Use after verification to compare solution options, estimate cost and risk, identify dependencies, sequence migrations, define test protection, rollback conditions, and acceptance criteria. Produces a plan only; it does not implement changes and must not plan from candidate or rejected findings.
---

# Plan architecture remediation

Turn confirmed findings into an executable, dependency-aware change roadmap without editing code.

## Load the contracts

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/remediation-contract.md`

Load a verified review. Exclude `candidate`, `rejected`, `needs-evidence`, and resolved findings. Recheck any finding whose evidence commit or underlying contract has materially changed.

## Workflow

1. Group findings by violated invariant and owning boundary. Do not create one project per symptom.
2. Build a dependency graph: prerequisites, findings resolved together, sequencing conflicts, external dependencies, and decisions requiring user authority.
3. Define the desired boundary or invariant before choosing a technology.
4. For each group, provide:
   - recommended approach and why it best fits current constraints;
   - materially viable alternatives and tradeoffs;
   - explicit do-nothing consequences;
   - effort size and uncertainty;
   - migration and compatibility risk;
   - ordered implementation slices;
   - test and observability protection;
   - rollback or containment strategy;
   - measurable acceptance criteria.
5. Order work by risk reduction, dependency, and reversibility—not severity alone.
6. Mark changes involving schemas, persisted data, public contracts, authorization, production infrastructure, or destructive effects as governed/high-risk work.

Do not prescribe a shared service merely because two projects use similar code. Require evidence of stable shared semantics, aligned lifecycle, and acceptable coupling.

## Output

Write:

- `.architecture/reviews/<timestamp>-remediation.yaml`;
- `.architecture/reviews/<timestamp>-remediation-plan.md`.

For portfolio work, use `.architecture-portfolio/reviews/`.

Start from `../../resources/templates/remediation-plan.yaml`; replace every example value and remove unused example entries.

Validate the machine-readable plan:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-plan <remediation.yaml>
```

End with the smallest safe first slice and its acceptance evidence. Do not implement it unless the user separately requests implementation.
