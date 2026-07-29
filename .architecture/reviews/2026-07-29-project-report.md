# Project architecture review — 2026-07-29

## Outcome

The architecture of Codex Architecture Governance at commit
`676ff9daa6931ed87ce8bf2da4f0222f47da14ee` is suitable for the v0.4.0
release scope. The review confirmed one evidence-system strength and found no
verified architecture risk that requires remediation.

This conclusion is intentionally bounded. It does not claim that the evaluated
models are universally reliable, that token or cost telemetry exists, or that
GitHub-hosted CI and a clean-machine installation have already passed.

## Scope and inputs

- Repository: `codex-architecture-governance`
- Review workflow: `project-architecture`
- Profile: `.architecture/profile.yaml`
- Repository facts: `.architecture/repository-facts.yaml`
- Rule Packs: `project-core`, `plugin-platform`,
  `test-automation-platform`
- Coverage: 31 rules, 6 critical flows, and 15 selected Knowledge entries
- Candidate artifact:
  `.architecture/reviews/2026-07-29-project-candidates-v2.yaml`
- Trusted artifact:
  `.architecture/reviews/2026-07-29-project-verified.yaml`
- Independent verification:
  `.architecture/reviews/2026-07-29-project-verification-v3.md`

The review inspected public Skills, plugin metadata, knowledge catalogs and
selection, artifact schemas, the deterministic CLI, benchmark fixtures and
results, tests, CI/release definitions, dependency locks, and packaging
controls.

## Architecture summary

The repository is a local-first Codex plugin with eight public workflow Skills.
Workflow instructions remain in Skills, curated architecture knowledge and
machine Rule Packs remain versioned data, and deterministic inspection,
validation, evidence resolution, decision validation, gating, benchmark
scoring, and release packaging remain in Python tooling. Project-specific
context is kept under `.architecture/`.

The main boundaries are coherent for a single-maintainer open-source tool:

- candidate analysis is separated from independent verification;
- probabilistic model output cannot directly block a build;
- verified artifacts bind repository identity, commit, profile, Rule Packs,
  selected knowledge, evidence, and verifier identity;
- architecture decisions and remediation plans are distinct from findings;
- runtime packaging uses an explicit allowlist and has no required hosted
  service, credential, network, or telemetry dependency.

## Confirmed strength

`CAG-EVIDENCE-001` was independently confirmed at V2. Behavior benchmark
schema 1.3, the runner, the scorer, the tamper tests, and both preserved model
runs form a complete bounded provenance chain:

- source commit and relevant dirty state;
- operating environment and locked dependencies;
- Ground Truth, schemas, Knowledge manifest, fixture trees, runner, adapter,
  and command-template hashes;
- per-trial command, output, observation, and log-record hashes;
- a canonical JSONL log whose count and digest are bound to the run;
- fail-closed scoring for missing, dirty, stale, changed, or inconsistent
  evidence.

The audit trail also records why this matters. The first candidate at commit
`4099c61` was rejected because the then-current result files did not bind code,
environment, configuration, runner, or execution logs. The missing capability
was implemented and tested; the replacement candidate at `676ff9d` was then
independently confirmed. This is evidence of a corrected control, not a
rewritten finding.

## Model-behavior evidence

Two real model runs executed 10 cases three times each, for 60 accepted trials.
Both provenance chains passed. Evidence validity and Knowledge citation
validity were 1.000 for both models, forbidden recommendation hits and
over-design rate were zero, and decision stability was 0.833.

Measured limitations remain part of the release evidence:

- Terra precision/recall were 0.944/0.872; Sol were 0.889/0.821.
- Required-Knowledge coverage was 0.750 for Terra and 0.625 for Sol.
- Both models missed some durable-recovery and tool-authority rules.
- SQLite transaction false positives, severity variance, and an extra AI
  boundary finding occurred in specific trials.
- Some mobile recommendations or required trade-offs were incomplete.
- The Codex surface exposed no token or cost telemetry; null is not zero.

The full metrics, environment, logs, and interpretation are preserved in
`benchmarks/reports/0.4.0-model-behavior.md` and the corresponding result,
score, and JSONL files.

## Decision and residual risk

No confirmed defect justifies introducing a hosted service, distributed
runtime, or broad internal-module migration for v0.4.0. The accepted decision
therefore keeps the current local-first plugin architecture and retains
modular-monolith enforcement or service extraction as measured future options.

Residual evidence still required after publication:

- GitHub-hosted CI and release workflow results for the final release commit;
- a current installation smoke test outside this working tree;
- GitHub artifact provenance/SBOM attestations for the published ZIP.

