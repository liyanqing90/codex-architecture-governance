# Target architecture implementation matrix

This matrix records the 1.0 public-contract implementation and its evidence.

| Phase | Required outcome | Implementation | Evidence |
| --- | --- | --- | --- |
| 0 | Preserve public identity and prior artifacts | One router, eight focused names, readable 0.4 artifacts, no new Skill | compatibility checks and Skill validation |
| 1 | Route design intent | Open, design, specify, constrain, and Chinese equivalents route to `architecture-solution-advisor` | routing corpus and exact public-surface check |
| 2 | Support open and constrained source modes | Brief 1.0 remains legacy open; Brief 1.1 declares open or constrained mode, with typed constraints only in constrained mode; remediation still binds verified Review | Brief/Decision contract validation |
| 3 | Challenge constraints | Required conflicts are challenged, preferred may lose, prohibited options hard-eliminate, inputs do not count as proof | decision-quality and artifact-validity cases |
| 4 | Emit a target architecture | Runtime/deployment units, data ownership, interfaces, trust boundaries, critical flows, operations, constraint assessments, and Knowledge are bound | target-architecture contract and tamper cases |
| 5 | Preserve evolution boundaries | Technology-evolution remains an explicit evidence lens; current official evidence is required and versions are never recalled from memory | decision-quality cases and evolution validation |
| 6 | Plan accepted targets | Remediation Plans retain Finding bindings; Greenfield Plan 1.3 binds Brief/Decision, has no fake Findings, and maps work to units/flows/constraints | planner contract and artifact-validity cases |
| 7 | Release one compatible product | New target artifacts release with Hengmu 1.0.0 and a migration guide; no mixed release of partial contracts | compatibility docs, ADR, changelog, packaging gate |

## Artifact chain

```text
repository-facts + Profile + Brief/constraints + Knowledge selection
        ├── verified Review ── proposed/accepted remediation Decision 1.2
        │                                      └── remediation Plan 1.2
        └── approved Brief 1.0 ─────────────── proposed/accepted Decision 1.3
            approved Brief 1.1 ─────────────── proposed/accepted Decision 1.4
                                                       └── Greenfield Plan 1.3
```

Every edge is checked by exact source hashes, semantic fingerprints, Knowledge
bindings, authorized and signed approval evidence, target references, or
complete evidence-backed coverage. A constraint input is not an evidence edge.
A generated plan is not completion evidence, and a migrated status is not
current verification.

Brief 1.1 approval is itself an edge: authorized identities, SHA-256-bound
repository evidence, and one detached SSH signature per approver are required.
A satisfied constraint is also bound to the
same Brief Knowledge ID and concrete target IDs; it cannot be asserted only by
writing `status: satisfied`.

## Delivery and rollback

The 1.0 change is additive at the workflow boundary. Existing focused Skill
names and readable artifact versions remain available. A consumer that cannot
read Brief 1.1, Decision 1.4, or Plan 1.3 continues using the 1.0/1.2/1.3
open or remediation path. Roll back by retaining the prior artifact chain and
not accepting a new constrained Decision; no existing artifact is rewritten.
