---
name: architecture-remediation-planner
description: Converts an accepted architecture decision for confirmed findings into an executable migration roadmap. Use after architecture-finding-verifier and architecture-solution-advisor when a project needs implementation slices, dependencies, compatibility, data migration, deployment sequencing, observability, rollback, stop conditions, effort, and acceptance criteria. Produces a plan only; it does not choose the target architecture or implement changes.
---

# Plan architecture remediation

Turn confirmed findings into an executable, dependency-aware change roadmap without editing code.

## Load the contracts

Read these files completely:

- `../../resources/references/review-contract.md`
- `../../resources/references/remediation-contract.md`

Load a verified review and an accepted architecture decision bound to that
review. Exclude `candidate`, `rejected`, `needs-evidence`, and resolved
findings. Recheck any finding whose fingerprint, evidence commit, or underlying
contract has materially changed. Stop when the decision remains proposed.

## Workflow

1. Group findings by violated invariant and owning boundary. Do not create one project per symptom.
2. Build a dependency graph: prerequisites, findings resolved together, sequencing conflicts, external dependencies, and decisions requiring user authority.
3. Preserve the selected option and desired invariant from the accepted
   decision. Do not reopen technology or architecture selection.
4. For each group, provide:
   - the accepted approach and decision reference;
   - explicit do-nothing consequences;
   - effort size and uncertainty;
   - migration and compatibility risk;
   - ordered implementation slices;
   - test and observability protection;
   - rollback or containment strategy;
   - measurable acceptance criteria and the evidence type that will prove each
     one.
   - exact Finding IDs and fingerprints;
   - Knowledge IDs from the accepted Decision;
   - assumptions that trigger replanning.
5. Order work by risk reduction, dependency, and reversibility—not severity alone.
6. Mark changes involving schemas, persisted data, public contracts, authorization, production infrastructure, or destructive effects as governed/high-risk work.

Do not prescribe a shared service merely because two projects use similar code. Require evidence of stable shared semantics, aligned lifecycle, and acceptable coupling.

## Output

Write:

- `.architecture/reviews/<timestamp>-remediation.yaml`;
- `.architecture/reviews/<timestamp>-remediation-plan.md`.

For portfolio work, use `.architecture-portfolio/reviews/`.

Start from `../../resources/templates/remediation-plan.yaml`; replace every example value and remove unused example entries.
Use Remediation Plan schema 1.2 for new plans. It must bind the trusted 1.2
Review, accepted 1.2 Decision, every Finding fingerprint, and only Knowledge
IDs present in that Decision's selection.

Validate the machine-readable plan and its source chain:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-plan \
  <remediation.yaml> \
  --review <verified-review.yaml> \
  --decision <accepted-decision.yaml> \
  --project <repo>
```

Leave `completion_evidence` empty until evidence exists. A completed item must
bind repository-relative evidence files and hashes for every declared type.
End with the smallest safe first slice and its acceptance evidence. Do not
implement it unless the user separately requests implementation.
