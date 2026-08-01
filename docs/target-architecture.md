# Target architecture

Version 0.3 separates four concerns that evolve and fail differently:

```text
public workflow Skills
        │
        ├── deterministic repository facts
        ├── declared and inferred project Profile
        └── task-scoped knowledge selection
                         │
                         ▼
candidate Review → verified Review → accepted Decision → remediation Plan
        │                 │                 │                  │
        └──────── exact hashes, fingerprints, coverage, and provenance ───────┘
                                          │
                                          ▼
                              deterministic quality gate
```

## Runtime boundaries

| Boundary | Owns | Must not own |
| --- | --- | --- |
| Public Skills | Workflow routing, evidence questions, artifact handoff | Deterministic validation or timeless product-version claims |
| Repository inspector | Observable files, manifests, detected dependencies, Git state, and scope | Suitability, severity, or architecture recommendations |
| Profile builder | Separation of detected, declared, and inferred context | Treating inference as observed fact |
| Knowledge selector | Reproducible inclusion, exclusion, reasons, and context budget | Selecting a target architecture |
| Knowledge Packs | Sourced reusable decision knowledge and freshness | Repository-specific conclusions |
| Review/Decision/Plan contracts | Provenance and authority transitions | Synthesizing missing verification |
| Quality gate | Deterministic policy over trusted artifacts | Interpreting candidate model prose |
| Maintainer curator | Knowledge lifecycle and release maintenance | End-user product audit or solution authority |

## Public workflow surface

The plugin exposes one stable public routing entry, `hengmu`, plus exactly
eight focused public workflow Skills:

1. project architecture audit;
2. AI-agent architecture audit;
3. mobile architecture audit;
4. portfolio architecture audit;
5. finding verification;
6. architecture solution advice;
7. remediation planning;
8. architecture quality gating.

The `hengmu` entry accepts commands or natural language, shows the complete
menu when invoked without a task, and then hands control to exactly one focused
Skill. It owns no audit, verification, decision, planning, or gate authority.
All focused names remain directly invocable compatibility contracts.

Knowledge curation is intentionally under `maintainer/skills/`. It ships with
the source repository but is not routed as an end-user plugin workflow.

## Project-local state

Each audited repository owns:

```text
.architecture/
├── profile.yaml
├── repository-facts.yaml
├── knowledge-selection.yaml
├── knowledge-context.yaml
├── constraints.md
├── critical-flows.md
├── gate-policy.yaml
├── baseline.yaml
├── risk-acceptances.yaml
├── evidence-providers.yaml
├── evidence/
├── rules/
└── reviews/
```

Facts are observations. The Profile is declared intent plus explicit bounded
inference. A selection is a reproducible context decision. Reviews, Decisions,
and Plans bind exact bytes from those inputs.

## Knowledge architecture

`resources/knowledge/manifest.yaml` registers ten Markdown/frontmatter packs:

- foundations;
- domains;
- decision guides;
- architecture styles;
- patterns;
- technology profiles;
- reference architectures;
- migration guides;
- anti-patterns;
- case studies.

Every entry has a canonical ID, semantic version, kind, domains, triggers,
quality attributes, relationships, source policy, authoritative sources,
review date, and review window. Technology profiles explicitly mark dynamic
facts and require current official confirmation when used.

The 0.2 YAML catalogs remain read-only compatibility data. New decisions bind
the selected Markdown entry versions and SHA-256 values.

## Trust transitions

- A candidate Review may contain `not_assessed` coverage, but never claims
  independent verification.
- A verified Review binds the source candidate, Profile, facts, selection,
  Rule Packs, critical flows, verifier, run, and Finding semantics.
- An accepted Decision binds a verified Review and the exact selected
  knowledge snapshot.
- A Plan binds confirmed Finding fingerprints, accepted Decision knowledge,
  assumptions, migration steps, rollback, and acceptance evidence.
- A gate reads trusted artifacts; it does not promote candidates.

Schema `1.2` adds these bindings without invalidating readable `1.0` or trusted
`1.1` history. Aggregate Portfolio Reviews continue to use the 1.1
system-of-systems contract while binding each registered repository's facts
and selection as evidence.

## Determinism and safety

Runtime scripts use no network, telemetry, credentials, or shell execution.
Repository scope is contained under an explicit root. Outputs refuse overwrite
unless the command exposes and receives an explicit force flag. Packaging is
runtime-only, sorted, timestamp-stable, checksummed, and SBOM-covered.

The accepted boundary decision is
[workflow, knowledge, and script separation](decisions/2026-07-29-adopt-workflow-knowledge-script-separation.md).
