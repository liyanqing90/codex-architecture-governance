# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-07-29

### Added

- Twenty-one curated golden knowledge entries with named options, concrete
  operating mechanisms, failure and exit semantics, claim-to-source mappings,
  and maintainer curation provenance.
- A Greenfield Design Brief contract, template, validator, decision bindings,
  and Architecture Decision schema `1.3` path that does not manufacture a
  source review.
- Solution-decision benchmark observations and scoring for recommendation
  accuracy, over-design, trade-off coverage, knowledge citation validity,
  rejected-option explanations, migration actionability, and stability.
- A read-only Codex benchmark adapter with machine Rule IDs, canonical
  decision vocabulary, structured-output validation, and one bounded
  evidence-only correction that never receives ground truth.
- Benchmark schema `1.4` provenance that binds source, environment,
  dependencies, configuration, plugin manifest and Skill version, fixtures,
  runner and adapter bytes, reconstructible command templates, exact trial
  commands, external runtime fingerprints, and hash-verified execution logs.
- Severity- and stage-aware verification policy: critical V3, high V2,
  medium/low V1, and V4 for risk acceptance and release.

### Changed

- Generated knowledge now defaults to draft and cannot become active without a
  non-generated curation record.
- Knowledge selection uses canonical domain IDs, includes `plugin-platform`,
  labels required/recommended/optional context, performs bounded one-hop
  relation expansion, and downweights generic reference-architecture matches.
- Knowledge validation rejects golden entries that are template-similar,
  omit named option trade-offs, or leave claims without authoritative sources.
- Backend API and web frontend domain guidance now cites relevant HTTP,
  OpenAPI, WCAG, and web-performance sources.
- Adversarial fixture paths and prose are outcome-neutral, with a regression
  test preventing expected decisions from leaking into model-visible inputs.
- Benchmark scores distinguish absent usage telemetry from actual zero
  token/cost consumption.
- Base-commit gates now require re-review only when a classified critical or
  security path changed after the reviewed commit; later governance-only
  records no longer create an impossible review/HEAD self-reference.
- An accepted `keep-current` decision with explicit migration slices,
  rollback, validation, and exact affected-path coverage now satisfies
  compatible migration governance without manufacturing a remediation plan
  for a non-risk Finding.

### Security

- Greenfield decisions bind the exact Design Brief and knowledge-selection
  bytes; remediation decisions retain verified-review provenance.
- Persistent risk acceptance and release evidence can no longer rely on the
  same global V1 verification floor as low-risk findings.

## [0.3.2] - 2026-07-29

### Fixed

- Made the benchmark command-rendering assertion compare against the native
  path representation so the cross-platform safety test passes on Windows
  without weakening its argument-boundary guarantee.

## [0.3.1] - 2026-07-29

### Fixed

- Added the Windows-only `colorama` dependency to the exact development lock
  so hash-enforced CI installation works on every supported runner.
- Bound SBOM generation, attestation, and release upload to one exact artifact
  path instead of passing an unexpanded glob to `actions/attest`.

## [0.3.0] - 2026-07-29

### Added

- Deterministic repository-facts inspection, provisional Profile construction,
  task-scoped knowledge selection, coverage validation, artifact
  fingerprinting, and safe legacy Review migration commands.
- Review, Finding, Architecture Decision, and Remediation Plan schema `1.2`
  bindings for facts, selected knowledge, critical flows, evidence
  fingerprints, finding fingerprints, assumptions, and migration slices.
- Ten Markdown/frontmatter Knowledge Packs containing 205 validated entries:
  foundations, domains, decision guides, architecture styles, patterns,
  technology profiles, reference architectures, migration guides,
  anti-patterns, and case studies.
- Knowledge manifest and entry schemas, relationship validation, source
  policy, freshness windows, stale-entry rejection, and explicit selection
  reasons and exclusions.
- Dedicated routing, knowledge-selection, decision-quality, false-positive,
  and artifact-validity evaluation corpora.
- Target-architecture, knowledge-authoring, 0.3 migration, and implementation
  documentation plus an accepted decision for the workflow/knowledge/script
  separation.

### Changed

- The public surface now contains exactly eight workflow Skills. Knowledge
  curation moved to `maintainer/skills/` because it is a release-maintenance
  role rather than an end-user architecture workflow.
- New project initialization records deterministic repository facts and keeps
  detected, declared, and inferred Profile inputs separate.
- New audits and decisions use schema `1.2`; schema `1.0` and `1.1` remain
  readable and trusted `1.1` artifacts retain their 0.2 compatibility path.
- Architecture knowledge is selected per repository, task, and Skill instead
  of loading every bundled catalog into context.
- Plugin and portable CLI version are now `0.3.0`.

### Security

- Legacy verified Reviews are migrated only as candidates. Migration cannot
  synthesize independent verification, critical-flow coverage, or current
  trust.
- Fact, Profile, selection, knowledge-entry, Finding, Review, Decision, Plan,
  and completion-evidence hashes are checked at their owning boundaries.

## [0.2.0] - 2026-07-28

### Added

- Architecture Solution Advisor and Architecture Knowledge Curator Skills.
- Eight machine-readable quality, style, pattern, technology, reference
  architecture, migration, domain, and decision-guide catalogs with 128
  sourced entries.
- Architecture Decision, Risk Acceptance, Rule Pack, Knowledge, Evidence
  Provider, and Benchmark schemas.
- Verified-review provenance bindings, verification levels, Finding
  fingerprints, Git evidence resolution, repository path containment, and
  machine-complete Rule Pack coverage.
- Contract, Finding, Change, and Release gate stages with exact, ancestor, and
  diff-aware freshness.
- Nineteen bundled core/domain Rule Packs plus validated repository-local
  organization Rule Packs.
- Eleven executable Evidence Provider adapters with shell-free invocation,
  executable/config/output hashing, timeout, safe environment propagation, and
  JSON/SARIF/JUnit structural validation.
- Role separation, human V3–V5 assurance requirements, deterministic evidence
  for V4–V5, and detached SSH review signatures at V5.
- Knowledge-bound three-option architecture decisions, hashed plan completion
  evidence, required-review enforcement, base-commit change classification,
  and review diffing.
- Ten adversarial architecture fixtures, repeated-trial stability, duration
  and optional usage metrics, deterministic benchmark scoring, and a
  caller-supplied forward-test harness.
- Fingerprint-bound baselines and waivers plus separately authorized,
  expiring risk acceptance.
- Fully hashed runtime/development locks, cross-platform checksum verification,
  license allow/deny audit, license-complete SPDX SBOM generation, dependency
  audit, SARIF output, and GitHub provenance/SBOM release attestations.

### Changed

- Trusted enforcement now requires artifact schema `1.1`; schema `1.0`
  remains readable for migration.
- Remediation planning consumes an accepted architecture decision instead of
  selecting technology and target architecture itself.
- CI now covers Python 3.11 and 3.13 on Ubuntu, macOS, and Windows.
- Plugin and portable CLI version are now `0.2.0`.

## [0.1.0] - 2026-07-28

### Added

- Seven focused architecture-governance Skills for project, AI-agent, mobile,
  portfolio, verification, remediation-planning, and quality-gate workflows.
- Versioned review, finding, profile, portfolio, remediation, baseline, and
  policy schemas.
- A portable CLI for initialization, validation, and deterministic policy
  evaluation.
- Repository validation, activation eval corpus, deterministic plugin
  packaging, CI, release automation, and open-source governance documents.
- A dogfooded project architecture profile with explicit constraints and
  critical flows.
