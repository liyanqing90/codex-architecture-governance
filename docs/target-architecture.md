# Target architecture

Hengmu 1.0 keeps the evidence and authority chain from 0.4 and adds one
explicit design path: the existing Solution Advisor can produce either an open
target or a constrained target. No public Skill is added.

```text
Profile + facts + Brief + constraints + selected Knowledge
                          │
                          ▼
candidate Review → verified Review → proposed Decision → accepted Decision
       │                                  │                    │
       └── remediation source              └── target architecture ──┘
                                                                  │
                                                                  ▼
                              Plan (remediation or Greenfield) → deterministic gate
```

## Runtime boundaries

| Boundary | Owns | Must not own |
| --- | --- | --- |
| `hengmu` router | Public discovery, language routing, read-only lifecycle navigation | Audit, verification, decision acceptance, planning, or gate authority |
| Eight focused Skills | Workflow questions, source selection, reasoning, and artifact handoff | Deterministic proof or model-memory version claims |
| Repository inspector | Observable files, manifests, dependencies, Git state, and scope | Suitability, severity, or architecture recommendations |
| Profile/Brief context | Declared intent, quality scenarios, and constraint inputs | Treating an input as verified evidence |
| Knowledge selector | Reproducible inclusion, exclusion, reasons, and budgets | Selecting a target architecture |
| Solution Advisor | Open/constrained comparison, target architecture, proposed Decision | Accepting a Decision, creating a Plan, or implementing code |
| Remediation planner | Accepted Decision to ordered plan, for Findings or Greenfield targets | Reopening architecture or inventing Findings |
| Quality gate | Deterministic policy over trusted artifacts | Interpreting candidate prose |

The Greenfield path enters the same CLI through an explicit Decision source:

```bash
python3 resources/scripts/architecture_tool.py gate --project <repo> \
  --decision <greenfield-decision.yaml> --stage change
```

At `change`, the Decision must be accepted by an authorized role and have an
active bound Plan. At `release`, the Plan must be complete and every declared
acceptance evidence type must resolve to repository-contained hashed evidence.

## Public workflow surface

The plugin exposes one stable routing entry, `hengmu`, and exactly eight focused
workflow Skills. The names remain compatibility contracts:

1. project architecture audit;
2. AI-agent architecture audit;
3. mobile architecture audit;
4. portfolio architecture audit;
5. finding verification;
6. architecture solution advice;
7. remediation planning; and
8. architecture quality gating.

`design`, `specify`, and `constrain`, including Chinese equivalents, route to
`architecture-solution-advisor`. They do not create a ninth Skill. The router
only selects a workflow and preserves that Skill's stop conditions and authority.

## Source and artifact modes

| Source | Meaning | Decision | Plan |
| --- | --- | --- | --- |
| Verified Review | Confirmed unresolved Findings require a solution | remediation Decision 1.2 (all Decision artifacts through 1.3 remain readable) | remediation Plan 1.2 |
| Design Brief 1.0 | Open Greenfield quality scenarios and boundaries | Decision 1.3 | Plan 1.3 when accepted |
| Design Brief 1.1 | Current open or constrained Greenfield; constrained mode records required/preferred/prohibited inputs | Decision 1.4 | Plan 1.3 when accepted |

Greenfield Decisions contain no Finding IDs. Greenfield Plans bind the Brief and
Decision directly and map implementation to the target rather than manufacturing
remediation evidence.

## Target architecture contents

A selected target, especially a constrained 1.4 Decision, is not an option title.
It records the following bound model:

- runtime units, responsibilities, and ownership;
- deployment units, environments, rollout, mixed-version behavior, and on-call;
- authoritative data owners, lifecycle, consistency, and recovery;
- interfaces, consumers, schemas, compatibility, and evolution;
- trust boundaries, identities, permissions, secrets, and untrusted inputs;
- critical flow triggers, steps, failures, recovery, and measurable outcomes;
- operations, observability, capacity, backup/restore, and incident controls;
- an assessment for each required, preferred, and prohibited constraint; and
- the selected Knowledge IDs, versions, and hashes.

Required constraints are challenged before they become hard requirements. Every
surviving required constraint must be satisfied. Preferred constraints may lose
with an explicit trade-off. Prohibited constraints hard-eliminate violating
options. None of these inputs proves feasibility or compliance on its own.

## Project-local state and Knowledge

Each audited repository owns facts, Profile, constraints, critical flows,
Knowledge selections, and review history under `.architecture/`. A Greenfield
Brief adds the design objective, quality scenarios, boundaries, data owners,
trust boundaries, critical flows, decision questions, success criteria, and (for
1.1) typed constraint records.

Knowledge is task-scoped Markdown with source, freshness, relationships, and
hashes. It supplies vocabulary, mechanisms, and decision guides. It never
overrides local evidence or proves project fit. Technology-evolution is a narrow
assessment lens for explicit upgrade/replacement questions; versions must be
bound to current official or repository evidence, never recalled from memory.

## Trust transitions

- candidate Reviews are not trusted conclusions;
- verified Reviews bind facts, selection, rules, critical flows, evidence, and
  Finding semantics;
- proposed Decisions bind a verified Review or Brief and Knowledge snapshot;
- accepted Decisions authorize planning but not implementation;
- remediation Plans bind Finding fingerprints, while Greenfield Plans bind the
  Brief and target architecture with empty Finding lists; and
- the gate consumes only schema-valid, hash-bound trusted artifacts.

The accepted boundary is recorded in
[the 1.0 constrained-target ADR](decisions/2026-08-06-add-constrained-target-architecture.md).
