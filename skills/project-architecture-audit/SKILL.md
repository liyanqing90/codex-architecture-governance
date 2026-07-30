---
name: project-architecture-audit
description: Evidence-backed, persistent architecture audit and profile setup for one repository. Use when initializing `.architecture`, onboarding to a codebase, reviewing architecture health, preparing a refactor, investigating structural debt, or assessing module boundaries, ownership, contracts, resilience, security, observability, tests, deployment, and over-design. Automatically initializes missing project governance unless the user explicitly requests read-only work. Produces candidate findings for independent verification, not confirmed conclusions, fixes, or remediation plans.
---

# Audit one project

Diagnose the current architecture against the project's own profile and
constraints. Identify strengths as well as risks. Do not confirm your own
candidates, change production code, or recommend fixes. Use
`architecture-finding-verifier` for confirmation and
`architecture-remediation-planner` only after findings are confirmed.

## Choose the persistence level

Treat an explicit request to run this Skill as a persistent audit. If
`.architecture/` is absent, initialize it before auditing; absence is a
bootstrap condition, never a reason to downgrade the audit. Reuse and validate
an existing control plane without overwriting it.

Operate in Advisory mode only when the user explicitly requests read-only work,
forbids repository changes, or the checkout cannot be written. In Advisory
mode, write no repository artifacts, do not run a Gate, and label conclusions
as observations or candidates in the response. State the write constraint; do
not cite a missing `.architecture/` directory as the reason.

## Load the contract

Read these files completely before auditing:

- `../../resources/references/review-contract.md`
- `../../resources/references/knowledge-contract.md`
- `../../resources/references/project-rules.md`
- `../../resources/rules/project-core.yaml`

Load `.architecture/profile.yaml`, `.architecture/constraints.md`, and
`.architecture/critical-flows.md` after preparation. Treat them as declared
intent, not proof. In explicit Advisory mode, infer a provisional profile in
memory and do not initialize.

## Initialize a project profile

For every persistent audit, read
`../../resources/references/profile-guide.md`, then run:

```bash
python3 ../../resources/scripts/architecture_tool.py prepare-project-audit \
  --repo <repo>
```

The command atomically creates a facts-derived `.architecture/` control plane
when missing. When it already exists, the command validates and reuses it. It
never overwrites an existing or partial directory. After first initialization,
replace provisional owner, constraint, and critical-flow values when repository
evidence supports them; preserve unknowns explicitly and validate:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-project <repo>
```

Use `init-project` directly only when the user supplies explicit initialization
values:

```bash
python3 ../../resources/scripts/architecture_tool.py init-project \
  --repo <repo> \
  --name "<project name>" \
  --type <project-type> \
  --quality <critical-quality> \
  --review project-architecture
```

Add repeated flags for additional types, qualities, rule packs, owners, and
required reviews. The command refuses to overwrite an existing
`.architecture` directory.

## Workflow

### 1. Inspect facts and select knowledge

Set one stable `<run-id>` for the audit. Run the deterministic fact collector
before interpreting architecture and preserve a per-run input instead of
rewriting a prior evidence chain:

```bash
python3 ../../resources/scripts/architecture_tool.py inspect-repository \
  --repo <repo> \
  --output <repo>/.architecture/reviews/inputs/<run-id>-repository-facts.yaml
```

Build a current Profile from those facts while retaining the initialized
Profile as declared intent. Keep detected, declared, and inferred inputs
separate:

```bash
python3 ../../resources/scripts/architecture_tool.py build-profile \
  --facts <repo>/.architecture/reviews/inputs/<run-id>-repository-facts.yaml \
  --declared <repo>/.architecture/profile.yaml \
  --output <repo>/.architecture/reviews/inputs/<run-id>-profile.yaml
```

Select only task-relevant Markdown knowledge and persist the reasons and
exclusions:

```bash
python3 ../../resources/scripts/architecture_tool.py select-knowledge \
  --facts <repo>/.architecture/reviews/inputs/<run-id>-repository-facts.yaml \
  --profile <repo>/.architecture/reviews/inputs/<run-id>-profile.yaml \
  --task "<current audit request>" \
  --skill project-architecture-audit \
  --output <repo>/.architecture/reviews/inputs/<run-id>-knowledge-selection.yaml \
  --context-output <repo>/.architecture/reviews/inputs/<run-id>-knowledge-context.yaml
```

Before reading model context, validate the sidecar against the exact lock:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-knowledge-context \
  <repo>/.architecture/reviews/inputs/<run-id>-knowledge-context.yaml \
  --selection <repo>/.architecture/reviews/inputs/<run-id>-knowledge-selection.yaml \
  --facts <repo>/.architecture/reviews/inputs/<run-id>-repository-facts.yaml \
  --profile <repo>/.architecture/reviews/inputs/<run-id>-profile.yaml
```

Read `knowledge-context.yaml` only after validation succeeds, then read every
Markdown path it selects
completely. Do not load the full `knowledge-selection.yaml` exclusion ledger
into model context; that lock is for scripts, Reviews, and Gates. Do not load
the full knowledge tree. Treat repository facts as observations, never as risk
conclusions.

### 2. Establish scope and provenance

- Resolve the repository root, requested paths, current commit, dirty-tree state, and active guidance.
- Inventory only source-of-truth inputs relevant to architecture: product and architecture documents, source, migrations, schemas, API or event definitions, deployment configuration, tests, and CI.
- Record missing or inaccessible evidence as `not_assessed`; never turn absence of inspection into a pass.
- Redact secrets and personal data from excerpts.

### 3. Build an architecture evidence map

Map:

- modules and domain boundaries;
- inbound and outbound dependencies;
- data stores, owners, writers, and migration paths;
- synchronous APIs, asynchronous events, background jobs, and critical flows;
- authentication, authorization, trust boundaries, and sensitive data;
- deployment units, configuration sources, telemetry, and test seams.

Trace every declared critical flow end to end. Prefer ownership and runtime paths over directory names.

### 4. Assess the rule set

Assess every machine rule in each Profile `rule_packs` entry and use
`project-rules.md` as investigation guidance. Load additional specialist audits
named by `required_reviews`; do not silently substitute a generic rule for an
AI, mobile, privacy, threat-model, or data-specific review.
Load repository-local Rule Packs from `.architecture/rules/` when selected by
the Profile. Treat them as project policy, validate their schema and review
kind, and never allow them to shadow bundled IDs.

For a large or cross-boundary repository, use up to four read-only specialists when subagent tools are available: boundaries, integration/data, runtime/reliability, and security/quality. Keep scopes non-overlapping and retain synthesis and verification in the main agent. If delegation is unavailable, run the same passes sequentially.

### 5. Form candidate findings

For each candidate:

- name the violated or protected invariant;
- cite the current path, line or symbol, and a concrete observation;
- trace the affected flow and owning boundary;
- state impact, blast radius, confidence, and counter-evidence;
- distinguish repository fact, inference, and unknown;
- record the E1–E5 evidence level, evidence fingerprint, Rule Pack version,
  profile applicability, selected knowledge, and staleness state;
- use a stable finding ID.

Do not infer an architecture flaw from file size, import count, a singleton, SQLite, a framework choice, or a directory name. Metrics are investigation leads only.

### 6. Prepare the verification handoff

Before handing candidates to the verifier:

- ensure every candidate records repository identity, direct evidence path,
  Git commit, blob SHA when available, and the inspected commit;
- state the strongest known benign explanation as counter-evidence;
- remove claims that do not meet the candidate evidence threshold;
- keep category, provisional severity, confidence, scope, and possible
  duplicates explicit;
- leave `verification.status` as `candidate`.

Do not promote a candidate to a final risk. When the user requested a complete
or verified review, continue with `$architecture-finding-verifier` after
persisting the candidate artifact.

### 7. Persist and validate

For every non-Advisory audit, write:

- candidate review: `.architecture/reviews/<timestamp>-project-candidates.yaml`;

Start machine-readable output from `../../resources/templates/review.yaml`; replace every example value and remove unused example entries.

Validate each YAML review:

```bash
python3 ../../resources/scripts/architecture_tool.py validate-review \
  <review.yaml> --project <repo>

python3 ../../resources/scripts/architecture_tool.py validate-coverage \
  --project <repo> --review <review.yaml> --allow-candidates
```

Resolve the script path from this Skill's directory when invoking it from another repository.
Use Review schema 1.2 for new audits. Bind the exact repository-facts and
knowledge-selection files and hashes; enumerate every critical flow and Rule
Pack rule. A candidate may say `not_assessed` with a reason, but must never
silently omit coverage.

## Handoff requirements

Lead with the architecture shape and clearly label all findings as candidates.
Include:

- current architecture and key boundaries;
- candidate strengths worth checking;
- candidate risks ordered by provisional severity;
- affected critical flows and ownership;
- coverage by rule, including `not_applicable` and `not_assessed`;
- hotspots and unanswered evidence questions;
- commit, scope, inspected artifacts, raw candidate count, and limitations.

Do not include remediation options in this audit.
