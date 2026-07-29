# Project architecture review — 2026-07-29

## Outcome

The architecture of Codex Architecture Governance at commit
`a290c4632a0974c087fd2dd578238e38a5004e13` is suitable for the v0.4.0
release scope. Independent verification confirmed two V2 architecture
strengths and found no verified architecture risk that requires remediation.

This conclusion is deliberately bounded. It does not claim visibility into a
remote model build, deterministic reproduction of model responses, token or
cost telemetry, or completion of the GitHub-hosted release workflow.

## Scope and inputs

- Repository: `codex-architecture-governance`
- Review workflow: `project-architecture`
- Profile: `.architecture/profile.yaml`
- Repository facts: `.architecture/repository-facts.yaml`
- Rule Packs: `project-core`, `plugin-platform`,
  `test-automation-platform`
- Coverage: 31 rules, 6 critical flows, and 15 selected Knowledge entries
- Candidate artifact:
  `.architecture/reviews/2026-07-29-project-candidates-v4.yaml`
- Trusted artifact:
  `.architecture/reviews/2026-07-29-project-verified.yaml`
- Independent verification:
  `.architecture/reviews/2026-07-29-project-verification-v5.md`

The review inspected public Skills, plugin metadata, Knowledge catalogs and
selection, artifact schemas, deterministic CLI behavior, benchmark fixtures
and results, tests, CI and release definitions, dependency locks, migration
guidance, and packaging controls.

## Architecture summary

The repository is a local-first Codex plugin with eight public workflow Skills.
Workflow instructions remain in Skills, curated architecture Knowledge and
machine Rule Packs remain versioned data, and deterministic inspection,
validation, evidence resolution, decision validation, quality gating,
benchmark scoring, and release packaging remain in Python tooling.
Project-specific context remains under `.architecture/`.

The principal boundaries are coherent for a small-team open-source project:

- candidate analysis is separated from independent verification;
- probabilistic model output cannot directly block a build;
- verified artifacts bind repository identity, commit, Profile, Rule Packs,
  selected Knowledge, evidence, and verifier identity;
- architecture decisions and remediation plans remain separate from findings;
- runtime packaging uses an explicit allowlist and requires no hosted service,
  credential, network access, or telemetry.

## Confirmed strengths

### CAG-EVIDENCE-001 — provenance-bound behavior evidence

The schema 1.4 benchmark contract, runner, scorer, preserved runs, and tamper
tests bind all locally controllable execution evidence:

- source commit and relevant dirty state;
- dependency lock, schemas, Ground Truth, Knowledge and plugin manifests,
  fixture trees, runner, adapter, and literal command template;
- requested and resolved command/model runtimes, executable hashes, version
  arguments, version output, and per-trial exact argv;
- exit status, stdout, stderr, structured observation, and canonical JSONL
  record hashes.

Strict verification re-resolves the current host runtimes and fails on a
mismatch. Git-bound archived verification instead proves the exact run and log
bytes existed at the named artifact commit, preserves every source, command,
log, and observation check, and explicitly reports a current-host mismatch.
Archived verification without a commit also fails closed.

The independent verifier rescored both 30-trial runs at artifact commit
`b6d406a324f294bf29deaf7b3280e8ae7ab22e4c`. Both passed archived
verification while correctly reporting that its current Codex runtime differed
from the recorded runtime. Default strict verification rejected that mismatch.

### CAG-GATE-001 — review freshness and migration authorization

The architecture gate independently checks paths changed after the reviewed
commit, so a historical base range cannot conceal a later change to a critical
or security-sensitive path. A compatible migration exception is accepted only
for an authorized `keep-current` decision whose `migration.affected_paths`
exactly cover all classified migration paths and whose slices, validation, and
rollback are nonempty. Other selected options require an active remediation
plan.

Regression cases cover a governance-only post-review change passing, a
post-review sensitive-path change failing, an incorrect migration path failing,
and a non-`keep-current` decision without a plan failing.

## Model-behavior evidence

Two real Codex model runs executed ten cases three times each, for 60 accepted
trials. Both provenance chains passed. Evidence validity and Knowledge
citation validity were 1.000 for both models; forbidden recommendation hits
and over-design rate were zero.

- Terra precision/recall: 0.943/0.846; required-Knowledge coverage: 0.792;
  recommendation quality: 0.917; decision stability: 0.833.
- Sol precision/recall: 0.868/0.846; required-Knowledge coverage: 0.625;
  recommendation quality: 1.000; decision stability: 1.000.

These measurements are evidence, not a claim of universal model reliability.
The full metrics, environment, logs, and limitations are preserved in
`benchmarks/reports/0.4.0-model-behavior.md` and the corresponding run, score,
and JSONL artifacts.

## Decision and residual risk

No confirmed defect justifies introducing a hosted service, distributed
runtime, or broad internal-module migration for v0.4.0. ADR-CAG-004 therefore
keeps the current local-first plugin architecture. Machine-enforced internal
module boundaries remain a measured future option if change-coupling or
ownership pressure reaches an explicit revisit trigger.

Remaining evidence to obtain during publication:

- GitHub-hosted CI and release workflow results for the final release commit;
- an installation smoke test from the packaged ZIP outside this working tree;
- GitHub artifact provenance and SBOM attestations for the published ZIP.

The accepted decision, exact alternatives, migration compatibility paths,
revisit triggers, and validation requirements are recorded in
`.architecture/reviews/2026-07-29-architecture-decision.yaml`.
